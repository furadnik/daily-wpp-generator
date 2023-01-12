import numpy
import datetime


def get_seed():
    return numpy.random.RandomState(datetime.date.today().isoformat())


def get_index(number_of_items: int):
    return get_seed().randint(number_of_items)
