from astral.sun import elevation
from astral.geocoder import database, lookup
from .config import Config

def city_fetch(city_name: str):
    return lookup(city_name, database()).observer

class Filter():

    """Decides how much the wallpaper should be darkened. """

    def __init__(self, city: str, min: float, max: float):
        self._city = city
        self._min_elevation = min
        self._max_elevation = max

    def compute_filter_value(self):
        current_elevation = elevation(city_fetch(self._city), with_refraction=True)
        elevation_difference = current_elevation - self._min_elevation
        percentual_difference = elevation_difference / \
                    (self._max_elevation - self._min_elevation)

        return max(0, min(percentual_difference, 1))
