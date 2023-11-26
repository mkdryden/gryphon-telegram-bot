FROM python:3.11

WORKDIR /usr/src/app

COPY . .
RUN pip install .

ENV BOT_TOKEN=-1

CMD [ "sh", "-c", "python -m gryphon_telegram_bot.main $BOT_TOKEN /persistence" ]
