import numpy
import datetime


def get_seed():
    return numpy.random.RandomState(hash(datetime.date.today().isoformat()) % 10**9)


def get_index(number_of_items: int):
    return get_seed().randint(number_of_items)
