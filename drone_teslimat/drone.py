from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Drone:
    id: int
    max_weight: float
    battery: int
    speed: float
    start_pos: Tuple[float, float]

@dataclass
class DeliveryPoint:
    id: int
    pos: Tuple[float, float]
    weight: float
    priority: int
    time_window: Tuple[str, str]

@dataclass
class NoFlyZone:
    id: int
    coordinates: List[Tuple[float, float]]
    active_time: Tuple[str, str] 