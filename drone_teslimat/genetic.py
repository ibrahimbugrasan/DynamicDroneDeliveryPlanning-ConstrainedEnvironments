import random
from typing import List, Dict, Tuple
from drone import Drone, DeliveryPoint, NoFlyZone
from graph_utils import euclidean_distance, edge_crosses_noflyzones
from datetime import datetime, timedelta

def create_random_chromosome(drones: List[Drone], deliveries: List[DeliveryPoint]) -> Dict[int, List[int]]:
    """
    Her drone'a rastgele teslimat atayan bir kromozom üretir.
    Dönüş: {drone_id: [teslimat_id, ...], ...}
    """
    chromosome = {drone.id: [] for drone in drones}
    delivery_ids = [d.id for d in deliveries]
    random.shuffle(delivery_ids)
    for i, delivery_id in enumerate(delivery_ids):
        drone = drones[i % len(drones)]
        chromosome[drone.id].append(delivery_id)
    return chromosome

def create_initial_population(pop_size: int, drones: List[Drone], deliveries: List[DeliveryPoint]) -> List[Dict[int, List[int]]]:
    return [create_random_chromosome(drones, deliveries) for _ in range(pop_size)]

def parse_time(timestr):
    return datetime.strptime(timestr, "%H:%M")

def fitness(chromosome: Dict[int, List[int]], drones: List[Drone], deliveries: List[DeliveryPoint], noflyzones: List[NoFlyZone], nofly_penalty: float = 1000.0, time_penalty: float = 500.0) -> float:
    """
    Fitness = teslimat sayısı × 50 – (toplam enerji × 0.1) – (ihlal edilen kısıt × 1000) – (zaman penceresi ihlali × 500)
    """
    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}
    total_energy = 0.0
    total_delivered = 0
    total_violations = 0
    total_time_violations = 0
    for drone_id, route in chromosome.items():
        drone = drone_map[drone_id]
        current_pos = drone.start_pos
        current_battery = drone.battery
        current_time = parse_time("09:00")  # Her drone 09:00'da başlıyor varsayalım
        for delivery_id in route:
            delivery = delivery_map[delivery_id]
            distance = euclidean_distance(current_pos, delivery.pos)
            travel_time = distance / drone.speed  # saat cinsinden
            # Kapasite kontrolü
            if delivery.weight > drone.max_weight:
                total_violations += 1
                continue
            # Batarya kontrolü
            if distance > current_battery:
                total_violations += 1
                continue
            # No-fly zone kontrolü
            if edge_crosses_noflyzones(current_pos, delivery.pos, noflyzones):
                total_violations += 1
                total_energy += distance
                current_battery -= distance
                current_time = current_time  # zaman ilerlemesin
                current_pos = delivery.pos
                continue
            # Zaman penceresi kontrolü
            arrival_time = current_time + timedelta(hours=travel_time)
            window_start = parse_time(delivery.time_window[0])
            window_end = parse_time(delivery.time_window[1])
            if arrival_time < window_start or arrival_time > window_end:
                total_time_violations += 1
            # Başarılı teslimat
            total_delivered += 1
            total_energy += distance
            current_battery -= distance
            current_time = arrival_time
            current_pos = delivery.pos
    return (total_delivered * 50) - (total_energy * 0.1) - (total_violations * 1000) - (total_time_violations * time_penalty)

def crossover(parent1: Dict[int, List[int]], parent2: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """
    İki ebeveyn kromozomdan yeni bir çocuk kromozom üretir.
    Her teslimat rastgele bir ebeveynden alınır.
    """
    child = {drone_id: [] for drone_id in parent1}
    all_deliveries = set()
    for drone_id in parent1:
        all_deliveries.update(parent1[drone_id])
        all_deliveries.update(parent2[drone_id])
    all_deliveries = list(all_deliveries)
    random.shuffle(all_deliveries)
    for delivery_id in all_deliveries:
        chosen_parent = parent1 if random.random() < 0.5 else parent2
        for drone_id in chosen_parent:
            if delivery_id in chosen_parent[drone_id]:
                child[drone_id].append(delivery_id)
                break
    return child

def mutate(chromosome: Dict[int, List[int]], drones: List[Drone]) -> Dict[int, List[int]]:
    """
    Rastgele bir teslimatı başka bir drone'a veya rotada başka bir yere atar.
    """
    mutant = {k: v[:] for k, v in chromosome.items()}
    drone_ids = list(mutant.keys())
    # Tüm teslimatları tek listede topla
    all_deliveries = [(drone_id, i, delivery_id)
                      for drone_id in drone_ids
                      for i, delivery_id in enumerate(mutant[drone_id])]
    if not all_deliveries:
        return mutant
    # Rastgele bir teslimat seç
    drone_id, idx, delivery_id = random.choice(all_deliveries)
    # O teslimatı çıkar
    mutant[drone_id].pop(idx)
    # Başka bir drone'a veya aynı drone'da başka bir yere ekle
    new_drone_id = random.choice(drone_ids)
    insert_pos = random.randint(0, len(mutant[new_drone_id]))
    mutant[new_drone_id].insert(insert_pos, delivery_id)
    return mutant

def genetic_algorithm(drones: List[Drone], deliveries: List[DeliveryPoint], noflyzones: List[NoFlyZone], pop_size=20, generations=50, crossover_rate=0.7, mutation_rate=0.2):
    population = create_initial_population(pop_size, drones, deliveries)
    best_solution = None
    best_fitness = float('-inf')
    for gen in range(generations):
        scored = [(fitness(chrom, drones, deliveries, noflyzones), chrom) for chrom in population]
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored[0][0] > best_fitness:
            best_fitness = scored[0][0]
            best_solution = scored[0][1]
        # Elitizm: en iyi %10'u koru
        next_gen = [chrom for _, chrom in scored[:max(1, pop_size//10)]]
        # Yeni nesil üret
        while len(next_gen) < pop_size:
            if random.random() < crossover_rate:
                p1 = random.choice(population)
                p2 = random.choice(population)
                child = crossover(p1, p2)
            else:
                child = random.choice(population)
            if random.random() < mutation_rate:
                child = mutate(child, drones)
            next_gen.append(child)
        population = next_gen
    return best_solution, best_fitness 