import heapq
from typing import Dict, Tuple, List, Optional
from graph_utils import euclidean_distance

def astar(graph: Dict[int, List[Tuple[int, float]]], nodes_pos: Dict[int, Tuple[float, float]], start: int, goal: int) -> Optional[List[int]]:
    """
    Komşuluk listesi grafında A* algoritması ile en düşük maliyetli rotayı bulur.
    nodes_pos: düğüm id -> (x, y) koordinatı
    start: başlangıç düğüm id
    goal: hedef düğüm id
    Dönüş: düğüm id'lerinden oluşan yol listesi veya None
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: euclidean_distance(nodes_pos[start], nodes_pos[goal])}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # Yol oluştur
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        for neighbor, cost in graph.get(current, []):
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean_distance(nodes_pos[neighbor], nodes_pos[goal])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None 