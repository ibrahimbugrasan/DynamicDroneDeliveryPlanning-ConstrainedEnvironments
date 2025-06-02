import matplotlib.pyplot as plt
from drone import Drone, DeliveryPoint, NoFlyZone
from typing import Dict, List

def plot_solution(drones: List[Drone], deliveries: List[DeliveryPoint], noflyzones: List[NoFlyZone], solution: Dict[int, List[int]]):
    delivery_map = {d.id: d for d in deliveries}
    # Noktaları çiz
    for drone in drones:
        plt.scatter(*drone.start_pos, c='blue', marker='s', s=100, label='Drone Start' if drone.id == drones[0].id else "")
    for delivery in deliveries:
        plt.scatter(*delivery.pos, c='green', marker='o', s=80, label='Delivery' if delivery.id == deliveries[0].id else "")
    # No-fly zone'ları çiz
    for i, zone in enumerate(noflyzones):
        coords = zone.coordinates + [zone.coordinates[0]]
        xs, ys = zip(*coords)
        plt.plot(xs, ys, 'r--', label='No-Fly Zone' if i == 0 else "")
    # Rotaları çiz
    colors = ['orange', 'purple', 'brown', 'cyan', 'magenta', 'black']
    for idx, (drone_id, route) in enumerate(solution.items()):
        if not route:
            continue
        drone = next(d for d in drones if d.id == drone_id)
        x, y = drone.start_pos
        for delivery_id in route:
            delivery = delivery_map[delivery_id]
            plt.plot([x, delivery.pos[0]], [y, delivery.pos[1]], '-', color=colors[idx % len(colors)], linewidth=2, label=f"Drone {drone_id} Route" if delivery_id == route[0] else "")
            x, y = delivery.pos
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Drone Teslimat Rotaları ve No-Fly Zone Görselleştirmesi')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.grid(True)
    plt.axis('equal')
    plt.show() 