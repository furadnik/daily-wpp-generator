from typing import Protocol
import random
import datetime

class Choice(Protocol):

    def choose(self):
        pass

    @property
    def length(self, arg1):
        pass


class Chooser(object):
    """Implements a random choice that is the same for a given date, since it chooses the seed"""

    def __init__(self, choices: list[Choice]):
        self._choices = choices

    def generate_random(self):
        today = datetime.date.today()
        rnd = random.seed(str(today.day) + str(today.month) + str(today.year))

        for item in self._choices:
            item.choose(random.randrange(item.length))

        
