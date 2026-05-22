import time
import os
import matplotlib.pyplot as plt
from turinglab.tm_engine import SingleTapeTM
from turinglab.ntm import NonDeterministicTM

print("Makineler yükleniyor...")
single_tm = SingleTapeTM.from_yaml("machines/single_find_11.yaml")
ntm = NonDeterministicTM.from_yaml("machines/ntm_find_11.yaml")

lengths = [10, 20, 30, 40, 50]
single_times = []
ntm_times = []

print("Yarış başlıyor! Lütfen bekleyin...")

for length in lengths:
    
    test_string = "0" * length + "11"
    
    # 1. Single Tape (Klasik) Ölçümü
    start = time.perf_counter()
    single_tm.run(test_string)
    single_times.append(time.perf_counter() - start)
    
    # 2. NTM (Paralel Evrenler) Ölçümü
    start = time.perf_counter()
    ntm.run(test_string)
    ntm_times.append(time.perf_counter() - start)

# Grafik Çizimi
plt.figure(figsize=(10, 6))
plt.plot(lengths, single_times, label="Single-Tape TM (Klasik)", marker='o', linewidth=2, color='blue')
plt.plot(lengths, ntm_times, label="NTM (Paralel Evrenler - BFS)", marker='s', linewidth=2, color='red')

plt.title("Klasik TM vs NTM (Performans Karşılaştırması)", fontsize=14, fontweight='bold')
plt.xlabel("Girdi Uzunluğu (N Harf)", fontsize=12)
plt.ylabel("Çalışma Süresi (Saniye)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# docs klasörüne kaydet
if not os.path.exists("docs"):
    os.makedirs("docs")
    
plt.savefig("docs/comparison.png")
print("\n🎉 Başarılı! Grafik oluşturuldu ve docs/comparison.png olarak kaydedildi.")