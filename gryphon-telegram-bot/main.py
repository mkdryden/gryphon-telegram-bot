from __future__ import annotations

import logging
from typing import Union, Mapping

import typer
from typing_extensions import Annotated
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from .gryphon import Gryphon

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


async def get_last_gryphon(context: ContextTypes.DEFAULT_TYPE) -> Union[Gryphon, None]:
    """Setup gryphon"""
    try:
        return context.chat_data["gryphons"][-1]
    except KeyError:
        return None


async def new_gryphon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    previous_gryphon = await get_last_gryphon(context)
    if not previous_gryphon:
        context.chat_data["gryphons"] = [Gryphon()]
    else:
        context.chat_data["gryphons"].append(Gryphon())
    gryphon = await get_last_gryphon(context)

    await query.answer(text="Summoning a new gryphon...")

    if previous_gryphon:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Farewell, {previous_gryphon.name}.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=gryphon.birth())

    return ConversationHandler.END


async def gryphon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    gryphon = await get_last_gryphon(context)

    if not gryphon:
        msg = "There is no gryphon in this chat yet."
        keyboard = [[InlineKeyboardButton("Summon a new gryphon!", callback_data='new_gryphon')]]
        next_state = 'new_gryphon'
    elif gryphon.state == "dead":
        msg = f"Your gryphon {gryphon.name} is dead."
        keyboard = [[InlineKeyboardButton("Summon a new gryphon!", callback_data='new_gryphon')]]
        next_state = 'new_gryphon'
    else:
        msg = f"Your gryphon is called {gryphon.name}."
        keyboard = [[InlineKeyboardButton(data[0], callback_data=f'gryphon_action.{command}')]
                    for command, data in gryphon.commands.items()]

        next_state = 'gryphon_action'

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)

    return next_state


async def gryphon_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | str:
    query = update.callback_query
    gryphon = await get_last_gryphon(context)
    _, _, action = query.data.partition('.')

    if action in gryphon.commands.keys():
        if not gryphon.commands[action][1]:
            await query.answer()
            await query.edit_message_text(text=getattr(gryphon, action)())
            return ConversationHandler.END
        else:
            await query.answer()

            buttons = {label: InlineKeyboardButton(label, callback_data=f'gryphon_action.{action}-{parameter}')
                       for label, parameter in gryphon.commands[action][1].items()}

            max_len = max(len(label) for label in buttons.keys())
            if max_len < 5:
                n = 3
                keyboard = [list(buttons.values())[i:i + n] for i in range(0, len(buttons), n)]
            elif max_len < 10:
                n = 2
                keyboard = [list(buttons.values())[i:i + n] for i in range(0, len(buttons), n)]
            else:
                keyboard = [[button] for button in buttons.values()]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"Select a parameter:", reply_markup=reply_markup)
            return 'gryphon_action'
    return ConversationHandler.END


async def gryphon_action_parameter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    gryphon = await get_last_gryphon(context)
    _, _, action = query.data.partition('.')
    action, _, parameter = action.partition('-')

    if action in gryphon.commands.keys():
        await query.answer()
        await query.edit_message_text(text=getattr(gryphon, action)(parameter))
        return ConversationHandler.END
    return ConversationHandler.END


async def update_gryphon(context: ContextTypes.DEFAULT_TYPE):
    for chat in context.job.data:
        try:
            gryphon = context.job.data[chat]['gryphons'][-1]
            if gryphon:
                event, msg = gryphon.update()
                if event:
                    await context.bot.send_message(chat_id=chat, text=msg)
        except KeyError:
            pass


states = {'new_gryphon': [CallbackQueryHandler(new_gryphon, pattern=r"^new_gryphon$")],
          'gryphon_action': [CallbackQueryHandler(gryphon_action, pattern=r"^gryphon_action\.([^-]+)$"),
                             CallbackQueryHandler(gryphon_action_parameter,
                                                  pattern=r"^gryphon_action\.([^-]+)-([^-]+)$")],
          }


def main(token: Annotated[str, typer.Argument(help='Telegram bot token')]) -> None:
    """Run the bot."""
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        per_user=True, per_message=False,
        entry_points=[CommandHandler('gryphon', gryphon),
                      CommandHandler('gryph', gryphon)],
        states=states,
        fallbacks=[CommandHandler('gryphon', gryphon)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Add a job queue to the application
    job_queue = application.job_queue
    update_gryphons_job = job_queue.run_repeating(update_gryphon, interval=3, first=5, data=application.chat_data)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    typer.run(main)
