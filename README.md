# Drone Delivery Optimization System

# 🚁 Drone Teslimat Rota Optimizasyonu

Bu proje, enerji limitleri ve uçuş yasağı bölgeleri (no-fly zone) gibi dinamik kısıtlar altında çalışan drone'lar için en uygun teslimat rotalarının belirlenmesini sağlayan bir algoritma sistemidir. A* algoritması ve Genetik Algoritma kullanarak çoklu drone filo yönetimi için yenilikçi ve uyarlanabilir bir çözüm sunar.

## 🎯 Proje Amacı

Teslimat hizmeti sunan lojistik firmaları için:

- Farklı ağırlık ve öncelik seviyelerine sahip paketleri
- Çok sayıda drone ile kısa sürede ve verimli bir şekilde
- Enerji kısıtları, uçuş yasağı bölgeleri ve dinamik değişkenler altında
- En uygun rota planlaması yapan algoritma geliştirmek

## ✨ Özellikler

### 🔧 Algoritma Özellikleri

- **A* Algoritması**: En kısa yol bulma için heuristik arama
- **Genetik Algoritma**: Çoklu drone optimizasyonu için evrimsel yaklaşım
- **CSP (Constraint Satisfaction Problem)**: Dinamik kısıt yönetimi
- **Graf Tabanlı Modelleme**: Komşuluk listesi ile verimli hesaplama

### 🚫 Kısıt Yönetimi

- **Enerji Limitleri**: Drone batarya kapasitesi kontrolü
- **Ağırlık Kapasitesi**: Maksimum taşıma ağırlığı kısıtları
- **No-Fly Zone'lar**: Dinamik uçuş yasağı bölgeleri
- **Zaman Pencereleri**: Teslimat zaman aralığı kısıtları
- **Öncelik Seviyeleri**: Acil teslimatlar için önceliklendirme

### 📊 Analiz ve Görselleştirme

- **Performans Metrikleri**: Teslimat oranı, enerji tüketimi, çalışma süresi
- **Görsel Haritalar**: Matplotlib ile rota görselleştirmesi
- **Karşılaştırmalı Analiz**: A* vs Genetik Algoritma performansı

## 🚀 Kurulum

### Gereksinimler

```bash
Python 3.8+
matplotlib
numpy (opsiyonel, performans için)
```

## Kurulum Adımları

### Projeyi klonlayın
```bash
git clone https://github.com/kullaniciadi/drone-delivery-optimization.git
cd drone-delivery-optimization
```

### Gerekli paketleri yükleyin
```bash
pip install matplotlib numpy
```

### Veri klasörünü oluşturun
```bash
mkdir data
```

## 📁 Proje Yapısı

```bash
drone-delivery-optimization/
├── README.md
├── requirements.txt
├── main.py                 # Ana çalıştırma dosyası
├── drone.py               # Veri sınıfları (Drone, DeliveryPoint, NoFlyZone)
├── data_generator.py      # Rastgele test verisi üretici
├── data_loader.py         # Veri dosyalarını yükleme modülü
├── graph_utils.py         # Graf işlemleri ve yardımcı fonksiyonlar
├── astar.py              # A* algoritması implementasyonu
├── genetic.py            # Genetik algoritma implementasyonu
├── visualize.py          # Sonuçları görselleştirme modülü
└── data/                 # Veri dosyaları klasörü
    ├── drones.txt
    ├── deliveries.txt
    └── noflyzones.txt
```

## 🎮 Kullanım
### Temel Kullanım
```bash
from main import run_scenario
from data_loader import load_drones, load_deliveries, load_noflyzones
```

### Veriyi yükle
```bash
drones = load_drones("data/drones.txt")
deliveries = load_deliveries("data/deliveries.txt")
noflyzones = load_noflyzones("data/noflyzones.txt")
```

### Senaryoyu çalıştır
```bash
solution, fitness, time = run_scenario(drones, deliveries, noflyzones, "Test Senaryosu")
```

### Rastgele Senaryo Üretimi
```bash
from data_generator import generate_scenario

# 5 drone, 20 teslimat, 3 no-fly zone ile senaryo oluştur
generate_scenario(
    num_drones=5,
    num_deliveries=20,
    num_noflyzones=3,
    scenario_name="test_scenario"
)
```

### Ana Programı Çalıştırma
```bash
python main.py
```



## 📋 Veri Formatları

### Drone Verisi (drones.txt)
```
# id,max_weight,battery,speed,start_x,start_y
1,5.0,15000,8.5,10,20
2,3.5,12000,7.2,15,25
```

### Teslimat Verisi (deliveries.txt)
```
# id,x,y,weight,priority,time_start,time_end
1,50,60,2.5,3,09:30,10:30
2,80,40,1.8,5,09:00,10:00
```

### No-Fly Zone Verisi (noflyzones.txt)
```
# id,x1,y1,x2,y2,x3,y3,x4,y4,active_start,active_end
1,30,30,40,30,40,40,30,40,09:30,11:00
```

## 🧮 Algoritma Detayları

### A* Algoritması
- **Maliyet Fonksiyonu**: Cost(distance, weight) = distance × weight + (priority × 100)
- **Heuristik**: h(n) = euclidean_distance(n, goal) + no_fly_zone_penalty
- **Kısıt Kontrolü**: Kapasite ve batarya limitleri

### Genetik Algoritma
- **Fitness Fonksiyonu**: Fitness = (teslimat_sayısı × 50) - (enerji × 0.1) - (ihlal × 1000)
- **Çaprazlama**: İki ebeveyn rotadan yeni rota üretimi
- **Mutasyon**: Rastgele teslimat noktası değişimi
- **Elitizm**: En iyi %10'u koruma

## 📊 Performans Metrikleri
- Tamamlanan Teslimat Yüzdesi: Başarılı teslimat oranı
- Ortalama Enerji Tüketimi: Toplam batarya kullanımı
- Algoritma Çalışma Süresi: Hesaplama performansı
- Kısıt İhlal Sayısı: Kural dışı operasyon sayısı

## 🧪 Test Senaryoları

### Senaryo 1: Küçük Ölçek
- 5 drone, 20 teslimat, 2 no-fly zone
- Hedef: < 10 saniye çalışma süresi

### Senaryo 2: Orta Ölçek
- 10 drone, 50 teslimat, 5 dinamik no-fly zone
- Hedef: < 30 saniye çalışma süresi

### Senaryo 3: Büyük Ölçek
- 15+ drone, 100+ teslimat, 10+ no-fly zone
- Hedef: < 60 saniye çalışma süresi

## 🔧 Konfigürasyon

### Genetik Algoritma Parametreleri
```python
# genetic.py içinde ayarlanabilir
pop_size = 30        # Popülasyon boyutu
generations = 50     # Nesil sayısı
crossover_rate = 0.7 # Çaprazlama oranı
mutation_rate = 0.2  # Mutasyon oranı
```

### Ceza Parametreleri
```python
# graph_utils.py içinde ayarlanabilir
nofly_penalty = 1000.0    # No-fly zone cezası
time_penalty = 500.0      # Zaman penceresi cezası
```

## 🤝 Katkıda Bulunma
1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## Geliştirme Alanları
- Daha gelişmiş heuristik fonksiyonlar
- Paralel işleme desteği
- Web tabanlı görselleştirme
- Gerçek zamanlı veri entegrasyonu
- Machine Learning tabanlı optimizasyon

## 📈 Gelecek Planları
- **v2.0**: Web arayüzü ve REST API
- **v2.1**: Gerçek zamanlı hava durumu entegrasyonu
- **v2.2**: 3D görselleştirme desteği
- **v3.0**: Multi-objective optimization

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

## 👥 Yazarlar
* Proje Ekibi
- İbrahim Buğra San
- Esat Berat Uzunca
- Yunus Emre Yılmaz

## 🙏 Teşekkürler
- Algoritma tasarımında ilham veren akademik çalışmalar
- Test verilerinin oluşturulmasında yardımcı olan topluluk
- Açık kaynak Python kütüphaneleri

## 📞 İletişim
Proje hakkında sorularınız için:
- GitHub Issues: Sorun bildirin
- Email: ibugrasan@gmail.com

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 

[ENGLISH]

# 🚁 Drone Delivery Route Optimization

This project is an algorithmic system that determines optimal delivery routes for drones operating under dynamic constraints such as energy limits and no-fly zones. It provides an innovative and adaptable solution for multi-drone fleet management using A* algorithm and Genetic Algorithm.

## 🎯 Project Objective

For logistics companies providing delivery services:

- Packages with different weights and priority levels
- Efficient and timely delivery with multiple drones
- Optimal route planning under energy constraints, no-fly zones, and dynamic variables
- Algorithm development for optimal route planning

## ✨ Features

### 🔧 Algorithm Features

- **A* Algorithm**: Heuristic search for shortest path finding
- **Genetic Algorithm**: Evolutionary approach for multi-drone optimization
- **CSP (Constraint Satisfaction Problem)**: Dynamic constraint management
- **Graph-Based Modeling**: Efficient computation with adjacency lists

### 🚫 Constraint Management

- **Energy Limits**: Drone battery capacity control
- **Weight Capacity**: Maximum carrying weight constraints
- **No-Fly Zones**: Dynamic flight restriction areas
- **Time Windows**: Delivery time range constraints
- **Priority Levels**: Prioritization for urgent deliveries

### 📊 Analysis and Visualization

- **Performance Metrics**: Delivery rate, energy consumption, runtime
- **Visual Maps**: Route visualization with Matplotlib
- **Comparative Analysis**: A* vs Genetic Algorithm performance

## 🚀 Installation

### Requirements

```bash
Python 3.8+
matplotlib
numpy (optional, for performance)
```

## Installation Steps

### Clone the project
```bash
git clone https://github.com/username/drone-delivery-optimization.git
cd drone-delivery-optimization
```

### Install required packages
```bash
pip install matplotlib numpy
```

### Create data directory
```bash
mkdir data
```

## 📁 Project Structure

```bash
drone-delivery-optimization/
├── README.md
├── requirements.txt
├── main.py                 # Main execution file
├── drone.py               # Data classes (Drone, DeliveryPoint, NoFlyZone)
├── data_generator.py      # Random test data generator
├── data_loader.py         # Data file loading module
├── graph_utils.py         # Graph operations and helper functions
├── astar.py              # A* algorithm implementation
├── genetic.py            # Genetic algorithm implementation
├── visualize.py          # Results visualization module
└── data/                 # Data files directory
    ├── drones.txt
    ├── deliveries.txt
    └── noflyzones.txt
```

## 🎮 Usage
### Basic Usage
```bash
from main import run_scenario
from data_loader import load_drones, load_deliveries, load_noflyzones
```

### Load data
```bash
drones = load_drones("data/drones.txt")
deliveries = load_deliveries("data/deliveries.txt")
noflyzones = load_noflyzones("data/noflyzones.txt")
```

### Run scenario
```bash
solution, fitness, time = run_scenario(drones, deliveries, noflyzones, "Test Scenario")
```

### Random Scenario Generation
```bash
from data_generator import generate_scenario

# Create scenario with 5 drones, 20 deliveries, 3 no-fly zones
generate_scenario(
    num_drones=5,
    num_deliveries=20,
    num_noflyzones=3,
    scenario_name="test_scenario"
)
```

### Run Main Program
```bash
python main.py
```

## 📋 Data Formats

### Drone Data (drones.txt)
```
# id,max_weight,battery,speed,start_x,start_y
1,5.0,15000,8.5,10,20
2,3.5,12000,7.2,15,25
```

### Delivery Data (deliveries.txt)
```
# id,x,y,weight,priority,time_start,time_end
1,50,60,2.5,3,09:30,10:30
2,80,40,1.8,5,09:00,10:00
```

### No-Fly Zone Data (noflyzones.txt)
```
# id,x1,y1,x2,y2,x3,y3,x4,y4,active_start,active_end
1,30,30,40,30,40,40,30,40,09:30,11:00
```

## 🧮 Algorithm Details

### A* Algorithm
- **Cost Function**: Cost(distance, weight) = distance × weight + (priority × 100)
- **Heuristic**: h(n) = euclidean_distance(n, goal) + no_fly_zone_penalty
- **Constraint Check**: Capacity and battery limits

### Genetic Algorithm
- **Fitness Function**: Fitness = (delivery_count × 50) - (energy × 0.1) - (violation × 1000)
- **Crossover**: New route generation from two parent routes
- **Mutation**: Random delivery point change
- **Elitism**: Preserving top 10%

## 📊 Performance Metrics
- Completed Delivery Percentage: Successful delivery rate
- Average Energy Consumption: Total battery usage
- Algorithm Runtime: Computational performance
- Constraint Violation Count: Number of rule violations

## 🧪 Test Scenarios

### Scenario 1: Small Scale
- 5 drones, 20 deliveries, 2 no-fly zones
- Target: < 10 seconds runtime

### Scenario 2: Medium Scale
- 10 drones, 50 deliveries, 5 dynamic no-fly zones
- Target: < 30 seconds runtime

### Scenario 3: Large Scale
- 15+ drones, 100+ deliveries, 10+ no-fly zones
- Target: < 60 seconds runtime

## 🔧 Configuration

### Genetic Algorithm Parameters
```python
# configurable in genetic.py
pop_size = 30        # Population size
generations = 50     # Number of generations
crossover_rate = 0.7 # Crossover rate
mutation_rate = 0.2  # Mutation rate
```

### Penalty Parameters
```python
# configurable in graph_utils.py
nofly_penalty = 1000.0    # No-fly zone penalty
time_penalty = 500.0      # Time window penalty
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Areas
- More advanced heuristic functions
- Parallel processing support
- Web-based visualization
- Real-time data integration
- Machine Learning-based optimization

## 📈 Future Plans
- **v2.0**: Web interface and REST API
- **v2.1**: Real-time weather integration
- **v2.2**: 3D visualization support
- **v3.0**: Multi-objective optimization

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors
* Project Team
- İbrahim Buğra San
- Esat Berat Uzunca
- Yunus Emre Yılmaz

## 🙏 Acknowledgments
- Academic studies that inspired the algorithm design
- Community that helped in test data generation
- Open source Python libraries

## 📞 Contact
For questions about the project:
- GitHub Issues: Report issues
- Email: ibugrasan@gmail.com

⭐ Don't forget to star this project if you like it!
