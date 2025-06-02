from data_loader import load_drones, load_deliveries, load_noflyzones
from graph_utils import build_graph
from astar import astar
from genetic import genetic_algorithm
from visualize import plot_solution
from data_generator import generate_scenario
import time
import random

def analyze_solution(solution, drones, deliveries, noflyzones):
    from genetic import fitness
    total_delivered = sum(len(route) for route in solution.values())
    total_deliveries = len(deliveries)
    fit = fitness(solution, drones, deliveries, noflyzones)
    print(f"Tamamlanan teslimat: {total_delivered}/{total_deliveries} (%{100*total_delivered/total_deliveries:.1f})")
    print(f"Fitness: {fit}")
    # Kural ve zaman ihlali sayısı
    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}
    from datetime import datetime, timedelta
    kural_ihlali = 0
    zaman_ihlali = 0
    for drone_id, route in solution.items():
        drone = drone_map[drone_id]
        current_pos = drone.start_pos
        current_battery = drone.battery
        current_time = datetime.strptime("09:00", "%H:%M")
        for delivery_id in route:
            delivery = delivery_map[delivery_id]
            from graph_utils import euclidean_distance, edge_crosses_noflyzones
            distance = euclidean_distance(current_pos, delivery.pos)
            travel_time = distance / drone.speed
            if delivery.weight > drone.max_weight or distance > current_battery or edge_crosses_noflyzones(current_pos, delivery.pos, noflyzones):
                kural_ihlali += 1
            arrival_time = current_time + timedelta(hours=travel_time)
            window_start = datetime.strptime(delivery.time_window[0], "%H:%M")
            window_end = datetime.strptime(delivery.time_window[1], "%H:%M")
            if arrival_time < window_start or arrival_time > window_end:
                zaman_ihlali += 1
            current_battery -= distance
            current_time = arrival_time
            current_pos = delivery.pos
    print(f"Kural ihlali sayısı: {kural_ihlali}")
    print(f"Zaman penceresi ihlali: {zaman_ihlali}")

def run_scenario(drones, deliveries, noflyzones, scenario_name, pop_size=30, generations=50):
    """Belirli bir senaryoyu çalıştırır."""
    print(f"\n--- {scenario_name} ---")
    start_time = time.time()
    best_solution, best_fitness = genetic_algorithm(drones, deliveries, noflyzones, pop_size=pop_size, generations=generations)
    elapsed = time.time() - start_time
    print(f"Sonuçlar:")
    analyze_solution(best_solution, drones, deliveries, noflyzones)
    print(f"Çalışma süresi: {elapsed:.2f} sn")
    plot_solution(drones, deliveries, noflyzones, best_solution)
    return best_solution, best_fitness, elapsed

def run_random_scenario():
    """Rastgele bir senaryo oluşturur ve çalıştırır."""
    # Rastgele parametreler
    num_drones = random.randint(5, 10)
    num_deliveries = random.randint(20, 40)
    num_noflyzones = random.randint(2, 5)
    map_size = 100
    
    # Senaryo adı için timestamp kullan
    scenario_name = f"random_{int(time.time())}"
    
    print(f"\n--- Yeni Rastgele Senaryo ---")
    print(f"Parametreler:")
    print(f"- {num_drones} drone")
    print(f"- {num_deliveries} teslimat noktası")
    print(f"- {num_noflyzones} no-fly zone")
    
    # Yeni rastgele senaryo oluştur
    generate_scenario(
        num_drones=num_drones,
        num_deliveries=num_deliveries,
        num_noflyzones=num_noflyzones,
        map_size=map_size,
        scenario_name=scenario_name
    )
    
    # Senaryoyu yükle ve çalıştır
    drones = load_drones(f"data/drones_{scenario_name}.txt")
    deliveries = load_deliveries(f"data/deliveries_{scenario_name}.txt")
    noflyzones = load_noflyzones(f"data/noflyzones_{scenario_name}.txt")
    
    # Genetik algoritma parametreleri
    pop_size = max(30, num_deliveries)
    generations = max(50, num_deliveries * 2)
    
    return run_scenario(drones, deliveries, noflyzones, "Rastgele Senaryo", pop_size, generations)

if __name__ == "__main__":
    # Temel senaryo
    drones = load_drones("data/drones.txt")
    deliveries = load_deliveries("data/deliveries.txt")
    noflyzones = load_noflyzones("data/noflyzones.txt")
    run_scenario(drones, deliveries, noflyzones, "Temel Senaryo", pop_size=20, generations=50)

    # Büyük senaryo
    drones_big = load_drones("data/drones_big.txt")
    deliveries_big = load_deliveries("data/deliveries_big.txt")
    noflyzones_big = load_noflyzones("data/noflyzones_big.txt")
    run_scenario(drones_big, deliveries_big, noflyzones_big, "Büyük Senaryo", pop_size=30, generations=80)

    # Çok büyük senaryo
    drones_large = load_drones("data/drones_large.txt")
    deliveries_large = load_deliveries("data/deliveries_large.txt")
    noflyzones_large = load_noflyzones("data/noflyzones_large.txt")
    run_scenario(drones_large, deliveries_large, noflyzones_large, "Çok Büyük Senaryo", pop_size=50, generations=100)

    # Özel senaryo
    drones_custom = load_drones("data/drones_custom.txt")
    deliveries_custom = load_deliveries("data/deliveries_custom.txt")
    noflyzones_custom = load_noflyzones("data/noflyzones_custom.txt")
    run_scenario(drones_custom, deliveries_custom, noflyzones_custom, "Özel Senaryo", pop_size=40, generations=80)

    # Rastgele senaryo
    run_random_scenario() 