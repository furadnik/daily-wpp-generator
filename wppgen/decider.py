import random
import datetime

def refresh_seed():
    random.seed(datetime.date.today().isoformat())

def get_index(number_of_items: int):
    refresh_seed()
    return random.randrange(number_of_items)
