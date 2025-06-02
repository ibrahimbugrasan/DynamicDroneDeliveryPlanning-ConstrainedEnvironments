from drone import Drone, DeliveryPoint, NoFlyZone
from typing import List

def load_drones(filename: str) -> List[Drone]:
    drones = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            drone = Drone(
                id=int(parts[0]),
                max_weight=float(parts[1]),
                battery=int(parts[2]),
                speed=float(parts[3]),
                start_pos=(float(parts[4]), float(parts[5]))
            )
            drones.append(drone)
    return drones

def load_deliveries(filename: str) -> List[DeliveryPoint]:
    deliveries = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            delivery = DeliveryPoint(
                id=int(parts[0]),
                pos=(float(parts[1]), float(parts[2])),
                weight=float(parts[3]),
                priority=int(parts[4]),
                time_window=(parts[5], parts[6])
            )
            deliveries.append(delivery)
    return deliveries

def load_noflyzones(filename: str) -> List[NoFlyZone]:
    noflyzones = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            id = int(parts[0])
            coordinates = [
                (float(parts[1]), float(parts[2])),
                (float(parts[3]), float(parts[4])),
                (float(parts[5]), float(parts[6])),
                (float(parts[7]), float(parts[8]))
            ]
            active_time = (parts[9], parts[10])
            zone = NoFlyZone(id=id, coordinates=coordinates, active_time=active_time)
            noflyzones.append(zone)
    return noflyzones 