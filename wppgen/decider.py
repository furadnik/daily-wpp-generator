import random
import datetime

random.seed(datetime.date.today().isoformat())

def get_index(number_of_items: int):
    return random.randrange(number_of_items)
