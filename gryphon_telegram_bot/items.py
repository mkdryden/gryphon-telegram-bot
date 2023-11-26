import logging
from abc import ABC


class BaseItem(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

    def __repr__(self):
        return f"{self.name}: {self.description}"