# TuringLab 🚀

**Geliştirici:** Sare Akbaş  
**Kurum:** Selçuk Üniversitesi, Bilgisayar Mühendisliği  
**Ders:** Hesaplama Kuramı (Otomata Teorisi ve Biçimsel Diller)  
**Tarih:** Mayıs 2026  

TuringLab, Turing makinelerinin (TM) teorik altyapısını çalıştırılabilir Python kodlarına dönüştüren modüler bir simülasyon motorudur. Deterministik tek-şeritli makinelerin yanı sıra, Çok-Şeritli (Multi-tape) ve Non-Deterministik (NTM) mimarileri de desteklemektedir.

---

## 🎬 Demo Videosu
Projenin mimari detaylarını, canlı simülasyon çıktılarını ve tasarım kararlarını anlattığım sunum videoma aşağıdan ulaşabilirsiniz:

👉 **[Demo Videosunu İzlemek İçin Tıklayın](https://youtu.be/NXgKvMFuwKk)** *(Not: Alternatif olarak video dosyası `docs/demo_video.mp4` konumunda da bulunmaktadır.)*

---

## ✨ Özellikler ve Geliştirilen Bonuslar
* **Temel TM Motoru (`tm_engine.py`):** YAML tabanlı kuralları dinamik olarak ayrıştırır ve `verbose=True` moduyla detaylı şerit takibi yapar.
* **4 Özgün TM Tasarımı:** `unary_to_binary.yaml`, `binary_compare.yaml`, `string_copy.yaml` ve öğrenci seçimi olan 4'e bölünebilme kontrolü (`student_choice.yaml`).
* **Bonus A (Çok-Şeritli TM - `multi_tape.py`):** Eşzamanlı okuma/yazma kafalarına ve `S` (Stay) hareketine sahip, 3-şeritli ikili toplama makinesi tasarımı.
* **Bonus B (Non-Deterministic TM - `ntm.py`):** Olasılık ağaçlarını BFS (Sığ Öncelikli Arama) algoritması ve `collections.deque` kuyruk yapısıyla çözen, sonsuz döngü korumalı NTM motoru.
* **Bonus C (Karşılaştırmalı Analiz - `benchmark.py`):** Klasik DTM ile NTM motorlarının çalışma sürelerini karşılaştıran ve `matplotlib` ile üretilen performans grafiği (`docs/comparison.png`).
* **Bonus D (Kare Kare Görselleştirici - `visualizer.py`):** TM adımlarını piksellere döküp Pillow kullanarak hareketli GIF üreten görüntü işleme modülü (`docs/images/tm_animation.gif`).

---

## 🚀 Kurulum ve Bağımlılıklar

Proje Python 3.10+ sürümü gerektirmektedir. Gerekli kütüphaneleri kurmak için terminalde şu komut çalıştırılır:

```bash
pip install -r requirements.txt