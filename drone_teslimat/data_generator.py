import random
from typing import List, Tuple, Dict
import datetime

def generate_random_drones(num_drones: int, 
                         min_weight: float = 2.0,
                         max_weight: float = 6.0,
                         min_battery: int = 8000,
                         max_battery: int = 20000,
                         min_speed: float = 5.0,
                         max_speed: float = 12.0,
                         map_size: int = 100) -> List[Dict]:
    """Rastgele drone'lar üretir."""
    drones = []
    for i in range(num_drones):
        drone = {
            "id": i + 1,
            "max_weight": round(random.uniform(min_weight, max_weight), 1),
            "battery": random.randint(min_battery, max_battery),
            "speed": round(random.uniform(min_speed, max_speed), 1),
            "start_pos": (random.randint(0, map_size), random.randint(0, map_size))
        }
        drones.append(drone)
    return drones

def generate_random_deliveries(num_deliveries: int,
                             min_weight: float = 0.5,
                             max_weight: float = 5.0,
                             map_size: int = 100,
                             time_window_minutes: int = 60) -> List[Dict]:
    """Rastgele teslimat noktaları üretir."""
    deliveries = []
    base_time = datetime.datetime.strptime("09:00", "%H:%M")
    
    for i in range(num_deliveries):
        # Rastgele başlangıç zamanı (09:00 ile 10:00 arası)
        start_minutes = random.randint(0, 60)
        start_time = base_time + datetime.timedelta(minutes=start_minutes)
        end_time = start_time + datetime.timedelta(minutes=time_window_minutes)
        
        delivery = {
            "id": i + 1,
            "pos": (random.randint(0, map_size), random.randint(0, map_size)),
            "weight": round(random.uniform(min_weight, max_weight), 1),
            "priority": random.randint(1, 5),
            "time_window": (start_time.strftime("%H:%M"), end_time.strftime("%H:%M"))
        }
        deliveries.append(delivery)
    return deliveries

def generate_random_noflyzones(num_zones: int,
                             min_size: int = 10,
                             max_size: int = 30,
                             map_size: int = 100,
                             time_window_minutes: int = 60) -> List[Dict]:
    """Rastgele no-fly zone'lar üretir."""
    zones = []
    base_time = datetime.datetime.strptime("09:00", "%H:%M")
    
    for i in range(num_zones):
        # Rastgele başlangıç zamanı (09:00 ile 10:00 arası)
        start_minutes = random.randint(0, 60)
        start_time = base_time + datetime.timedelta(minutes=start_minutes)
        end_time = start_time + datetime.timedelta(minutes=time_window_minutes)
        
        # Rastgele merkez nokta
        center_x = random.randint(min_size, map_size - min_size)
        center_y = random.randint(min_size, map_size - min_size)
        
        # Rastgele boyut
        size = random.randint(min_size, max_size)
        
        # Dikdörtgen köşeleri
        x1 = center_x - size//2
        y1 = center_y - size//2
        x2 = center_x + size//2
        y2 = center_y - size//2
        x3 = center_x + size//2
        y3 = center_y + size//2
        x4 = center_x - size//2
        y4 = center_y + size//2
        
        zone = {
            "id": i + 1,
            "coordinates": [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
            "active_time": (start_time.strftime("%H:%M"), end_time.strftime("%H:%M"))
        }
        zones.append(zone)
    return zones

def save_to_file(data: List[Dict], filename: str, data_type: str):
    """Veriyi dosyaya kaydeder."""
    with open(filename, 'w') as f:
        if data_type == "drone":
            f.write("# id,max_weight,battery,speed,start_x,start_y\n")
            for item in data:
                f.write(f"{item['id']},{item['max_weight']},{item['battery']},{item['speed']},{item['start_pos'][0]},{item['start_pos'][1]}\n")
        elif data_type == "delivery":
            f.write("# id,x,y,weight,priority,time_start,time_end\n")
            for item in data:
                f.write(f"{item['id']},{item['pos'][0]},{item['pos'][1]},{item['weight']},{item['priority']},{item['time_window'][0]},{item['time_window'][1]}\n")
        elif data_type == "noflyzone":
            f.write("# id,x1,y1,x2,y2,x3,y3,x4,y4,active_start,active_end\n")
            for item in data:
                coords = item['coordinates']
                f.write(f"{item['id']},{coords[0][0]},{coords[0][1]},{coords[1][0]},{coords[1][1]},{coords[2][0]},{coords[2][1]},{coords[3][0]},{coords[3][1]},{item['active_time'][0]},{item['active_time'][1]}\n")

def generate_scenario(num_drones: int = 5,
                     num_deliveries: int = 20,
                     num_noflyzones: int = 3,
                     map_size: int = 100,
                     scenario_name: str = "random"):
    """Belirtilen parametrelerle yeni bir senaryo üretir."""
    # Rastgele veri üret
    drones = generate_random_drones(num_drones, map_size=map_size)
    deliveries = generate_random_deliveries(num_deliveries, map_size=map_size)
    noflyzones = generate_random_noflyzones(num_noflyzones, map_size=map_size)
    
    # Dosyalara kaydet
    save_to_file(drones, f"data/drones_{scenario_name}.txt", "drone")
    save_to_file(deliveries, f"data/deliveries_{scenario_name}.txt", "delivery")
    save_to_file(noflyzones, f"data/noflyzones_{scenario_name}.txt", "noflyzone")
    
    print(f"Senaryo '{scenario_name}' başarıyla oluşturuldu!")
    print(f"- {num_drones} drone")
    print(f"- {num_deliveries} teslimat noktası")
    print(f"- {num_noflyzones} no-fly zone")

if __name__ == "__main__":
    # Örnek kullanım
    generate_scenario(num_drones=5, 
                     num_deliveries=20, 
                     num_noflyzones=3, 
                     scenario_name="random_test") 