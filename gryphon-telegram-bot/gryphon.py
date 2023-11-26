from __future__ import annotations

import asyncio
from collections import deque
from pathlib import Path
import logging
from random import choice
from time import time
from typing import Union

from .food import foods


def load_data(path: Path) -> list[str]:
    with open(path, 'r') as f:
        data = f.readlines()
    return [i.rstrip() for i in data]


class Gryphon(object):
    riddles = load_data(Path(__file__).parent / 'data/riddles.txt')
    states = ["sleeping", "hunting", "flying", "idle", "dead"]
    commands = {'screech': ('Screech', None),
                'nap': ('Nap', None),
                'fly': ('Fly', None),
                'hunt': ('Hunt', {i: i for i in foods.categories}),
                'tell_riddle': ('Riddle', None),
                'status': ('Status', None),
                'change_feather_colour': ("Change Feather Colour",
                                          {'🟥': 'red', '🟧': 'orange', '🟨': 'yellow',
                                           '🟩': 'green', '🟦': 'blue', '🟪': 'violet',
                                           '🟫': 'brown', '⬛': 'red', '⬜': 'white'}),
                }
    names = load_data(Path(__file__).parent / 'data/names.txt')
    last_names = deque(maxlen=len(names) // 2)

    def __init__(self):
        self.last_riddles = deque(maxlen=len(self.riddles) // 2)
        self.feather_colour = "white"

        while True:
            self.name = choice(self.names)
            if self.name not in self.last_names:
                break
        self.last_names.append(self.name)

        self.birthday = time()
        self.deathday: Union[None, float] = None

        self.event_done_time: Union[None, float] = None
        self.event_done_callback: Union[None, callable] = None
        self.event_done_callback_args: Union[None, tuple] = None

        self._state = "idle"

    @property
    def age(self) -> str:
        """Returns the age of the gryphon as a formatted string."""
        if self.deathday is not None:
            age = self.deathday - self.birthday
        else:
            age = time() - self.birthday

        if age < 60:
            return f"{age:.0f} seconds old"
        elif age < 3600:
            return f"{age / 60:.0f} minutes old"
        elif age < 86400:
            return f"{age / 3600:.0f} hours old"
        elif age < 604800:
            return f"{age / 86400:.0f} days old"
        elif age < 2419200:
            return f"{age / 604800:.0f} weeks old"
        elif age < 29030400:
            return f"{age / 2419200:.0f} months old"
        else:
            return f"{age / 29030400:.0f} years old"

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: str):
        if new_state in self.states:
            self._state = new_state
        else:
            raise ValueError(f"Invalid state {new_state}")

    def birth(self):
        return f"Screech! I'm {self.name} the gryphon!"

    def status(self):
        if self.state == "dead":
            return f"{self.name} the gryphon is currently dead and possibly a dragon snack."
        return f"Screech! I'm {self.name} the gryphon! My feathers are {self.feather_colour} " + \
            f"and I'm {self.age}. I am currently {self.state}."

    def is_busy(self, requested_state: str = None) -> tuple[bool, str]:
        if self.state == "dead":
            return True, "She's dead, Jim."
        if requested_state == self.state:
            return True, "I'm already doing that!"
        if self.state == "sleeping":
            return True, "Screech! I'm trying to sleep!"
        if self.state == "hunting":
            return True, "I'm busy hunting!"
        if self.state == "flying":
            return True, "I'm busy flying!"
        return False, ""

    def screech(self):
        busy, msg = self.is_busy()
        if busy:
            return msg
        return "SCREECH!!!"

    def nap(self):
        busy, msg = self.is_busy()
        if busy:
            return msg

        self.state = "sleeping"
        self.event_done_time = time() + 60
        return f"{self.name} is now napping."

    def change_feather_colour(self, colour: str):
        self.feather_colour = colour
        if self.state == "dead":
            return f"You spray painted the dead gryphon {colour}!"
        return f"You spray painted the gryphon {colour}!"

    def fly(self):
        busy, msg = self.is_busy()
        if busy:
            return msg

        self.state = "flying"
        self.event_done_time = time() + 30
        return f"{self.name} heads out for a flight."

    def hunt(self, category: str) -> str:
        busy, msg = self.is_busy()
        if busy:
            return msg

        self.state = "hunting"
        self.event_done_time = time() + 2
        self.event_done_callback = self._hunt_callback
        self.event_done_callback_args = (category,)
        return f"{self.name} is now hunting for {category}!"

    def _hunt_callback(self, category: str):
        died, msg = foods.get_food(category).hunt(self.name)
        if died:
            self.state = "dead"
        return msg

    def tell_riddle(self) -> str:
        if self.state == "dead":
            return "A dead gryphon tells no tales."
        busy, msg = self.is_busy()
        if busy:
            return msg
        while True:
            riddle = choice(self.riddles)
            if riddle not in self.last_riddles:
                break
        self.last_riddles.append(riddle)
        return riddle

    def update(self) -> tuple[bool, str | None]:
        if self.event_done_time is not None:
            if time() > self.event_done_time:
                self.event_done_time = None
                self.state = "idle"
                msg = None
                if self.event_done_callback is not None:
                    try:
                        msg = self.event_done_callback(*self.event_done_callback_args)
                    except TypeError:
                        msg = self.event_done_callback()
                    self.event_done_callback = None
                return True, msg
        return False, None
