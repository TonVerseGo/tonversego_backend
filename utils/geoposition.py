from geopy.distance import geodesic
from typing import Tuple

class Geoposition:
    @classmethod
    def get_distance(cls, obj1: Tuple[float, float], obj2: Tuple[float, float]):
        return geodesic(obj1, obj2).meters

    @classmethod
    def get_direction(cls, obj1: Tuple[float, float], obj2: Tuple[float, float]) -> str:
        lat1, lon1 = obj1
        lat2, lon2 = obj2

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        if abs(dlat) > abs(dlon):
            return "north" if dlat > 0 else "south"
        else:
            return "east" if dlon > 0 else "west"