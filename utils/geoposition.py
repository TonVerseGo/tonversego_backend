from geopy.distance import geodesic
from typing import Tuple

class Geoposition:
    @classmethod
    def get_distance(cls, obj1: Tuple[float, float], obj2: Tuple[float, float]):
        return geodesic(obj1, obj2).meters