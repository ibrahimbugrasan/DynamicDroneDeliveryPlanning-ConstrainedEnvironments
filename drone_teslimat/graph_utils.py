import math
from drone import DeliveryPoint, Drone, NoFlyZone
from typing import Dict, Tuple, List

def euclidean_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def cost_function(distance: float, weight: float, priority: int, nofly_penalty: float = 0.0) -> float:
    return distance * weight + (priority * 100) + nofly_penalty

def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def segments_intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def edge_crosses_noflyzones(start: Tuple[float, float], end: Tuple[float, float], noflyzones: List[NoFlyZone]) -> bool:
    for zone in noflyzones:
        coords = zone.coordinates
        n = len(coords)
        for i in range(n):
            if segments_intersect(start, end, coords[i], coords[(i+1)%n]):
                return True
    return False

def build_graph(deliveries: List[DeliveryPoint], drones: List[Drone], noflyzones: List[NoFlyZone], nofly_penalty: float = 1000.0) -> Dict[int, List[Tuple[int, float]]]:
    """
    Komşuluk listesi olarak graf döndürür.
    Her düğümün (teslimat noktası ve drone başlangıç noktası) komşularını ve maliyetlerini içerir.
    No-fly zone cezası ve kapasite/batarya kısıtları eklenir.
    """
    nodes = {d.id: d.pos for d in deliveries}
    drone_id_map = {}
    for i, drone in enumerate(drones):
        drone_id = -(i+1)
        nodes[drone_id] = drone.start_pos
        drone_id_map[drone_id] = drone

    graph = {node_id: [] for node_id in nodes}
    for src_id, src_pos in nodes.items():
        for dst_id, dst_pos in nodes.items():
            if src_id == dst_id:
                continue
            if dst_id > 0:
                delivery = next(d for d in deliveries if d.id == dst_id)
                distance = euclidean_distance(src_pos, dst_pos)
                penalty = nofly_penalty if edge_crosses_noflyzones(src_pos, dst_pos, noflyzones) else 0.0
                # Kapasite ve batarya kısıtları sadece drone'dan teslimata giden kenarlarda kontrol edilir
                if src_id < 0:
                    drone = drone_id_map[src_id]
                    if delivery.weight > drone.max_weight:
                        continue  # Kapasiteyi aşan teslimat
                    if distance > drone.battery:  # Basit model: batarya kapasitesi mesafeye eşit
                        continue  # Batarya yetmiyor
                cost = cost_function(distance, delivery.weight, delivery.priority, penalty)
                graph[src_id].append((dst_id, cost))
    return graph 