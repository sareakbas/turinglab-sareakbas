# TuringLab — Teknik Proje Raporu

**Öğrenci:** Sare Akbaş  
**Kurum:** Selçuk Üniversitesi, Bilgisayar Mühendisliği  
**Ders:** Hesaplama Kuramı (Otomata Teorisi ve Biçimsel Diller)  
**Tarih:** 22 Mayıs 2026  

---

## 1. Giriş

TuringLab, bilgisayar bilimlerinin ve hesaplama teorisinin en temel matematiksel modeli olan Turing Makinelerini (TM) soyut birer tanım olmaktan çıkarıp çalıştırılabilir, test edilebilir ve analiz edilebilir yazılım artefaktlarına dönüştüren kapsamlı bir Python kütüphanesidir. Proje; standart Deterministik Tek-Şeritli Turing Makinelerinin (DTM) yanı sıra hesaplama kuramının ileri seviye varyantları olan Çok-Şeritli Turing Makinelerini (Multi-Tape TM) ve Non-Deterministik Turing Makinelerini (NTM) simüle edebilecek modüler bir mimariye sahiptir.

Makinelerin durum kümeleri ($Q$), girdi alfabeleri ($\Sigma$), şerit alfabeleri ($\Gamma$) ve en önemlisi geçiş fonksiyonları ($\delta$), insan tarafından okunabilir ve kolayca düzenlenebilir YAML formatındaki yapılandırma dosyalarında tanımlanır. TuringLab motoru, bu bildirimsel yapılandırmaları dinamik olarak ayrıştırarak bellek üzerinde canlı birer otomat nesnesi olarak inşa eder. Kütüphane bünyesinde ayrıca; durum adımlarını kare kare piksellere dökerek hareketli animasyonlar üreten bir görselleştirici modül (`visualizer.py`), deterministik ve non-deterministik hesaplama karmaşıklıklarını süre bazında yarıştıran bir analiz aracı (`benchmark.py`) ve hata ayıklama süreçleri için tasarlanmış detaylı bir canlı takip modu (`verbose`) yer almaktadır.

---

## 2. Mimari ve Yazılım Tasarımı

Proje mimarisi, nesne yönelimli programlama (OOP) prensiplerine sıkı sıkıya bağlı, birbiriyle gevşek bağlı (loosely coupled) ve genişletilebilir bir paket yapısı olan `turinglab/` dizini altında organize edilmiştir. Çekirdek bileşenlerin teknik dökümü şu şekildedir:

### `tm_engine.py` — Çekirdek Deterministik Motor
Deterministik simülasyonun kalbi olan `SingleTapeTM` sınıfı bu dosyada yer alır. Şerit mekanizmasını taklit eden `Tape` yapısı, projenin en kritik kararlarından biri olarak **`dict[int, str]` (Seyrek Sözlük - Sparse Dictionary)** yapısı üzerine kurulmuştur. Motor, yürütme esnasında `verbose=True` bayrağını aldığında, her bir durum değişimini ve kafa hareketini anlık olarak konsola çıktı verir. Bu çıktı mimarisi, şeridin o anki durumunu, kafanın konumunu ve güncel durumu `[durum] girdi_dizgisi` formatında mikro düzeyde izlemeyi mümkün kılar.

### `multi_tape.py` — Çok-Şeritli Simülasyon Motoru (Bonus A)
`MultiTapeTM` sınıfı, tek bir durum kontrol mekanizmasına bağlı olarak eşzamanlı ve birbirinden bağımsız hareket edebilen `num_tapes` adet şerit nesnesini yönetir. Standart motordan farklı olarak bu mimaride geçiş kurallarının `read`, `write` ve `move` parametreleri tek bir karakter yerine şerit sayısı uzunluğunda birer `tuple` (çoklu dizi) olarak işlenir. Sözlük indeksleme anahtarı `(mevcut_durum, (okunan_sembol_1, okunan_sembol_2, ...))` şeklinde çok boyutlu hale getirilmiştir. Bu motor bünyesinde kafanın sağa (`R`) veya sola (`L`) gitmeyip olduğu yerde sabit kalmasını sağlayan **`S` (Stay)** hareketi de tam olarak desteklenmektedir. Örnek uygulama olarak geliştirilen 3-şeritli binary toplama makinesi (`binary_add_multi.yaml`), normalde tek şeritte yüzlerce adım süren karmaşık bir matematiksel işlemi şeritler arası paralel veri taşıma avantajıyla optimize etmiştir.

### `ntm.py` — Non-Deterministik Hesaplama Motoru (Bonus B)
`NonDeterministicTM` sınıfı, hesaplama teorisindeki "aynı anda birden fazla duruma geçebilme" (paralel evrenler) konseptini simüle eder. Bu modülde geçiş fonksiyonu tek bir hedefe değil, bir durum ve sembol çifti için olası tüm geçişlerin listesine (`list[tuple]`) eşlenir. Sonsuz döngülerin ve durdurulamayan dallanmaların motoru çökertmesini engellemek adına yapılandırma dosyasına kurşun geçirmez **`max_branches`** (maksimum dal sayısı) ve **`max_depth`** (maksimum ağaç derinliği) koruma parametreleri entegre edilmiştir. 

Arama algoritması olarak kesinlikle **BFS (Breadth-First Search - Sığ Öncelikli Arama)** tercih edilmiştir ve süreç `collections.deque` kuyruk veri yapısı ile yönetilmektedir. DFS (Derinlik Öncelikli Arama) algoritması, NTM simülasyonlarında sonsuz bir döngü dalına saptığı an tüm programın kilitlenmesine neden olurken; BFS algoritması hesaplama ağacını seviye seviye taradığı için, eğer girdi dili kabul ediyorsa o kabul yolunu (`accepting_paths`) bellekteki diğer dalları tüketmeden bulup çıkarabilmektedir.

### `visualizer.py` — Kare Kare Görselleştirici Modülü (Bonus D)
Görselleştirici modül, hesaplama teorisindeki soyut kafa hareketlerini somut resim karelerine dönüştürür. `Pillow (PIL)` kütüphanesi kullanılarak, makinenin çalıştığı her adımda şeridin güncel durumu için boş bir RGB tuval oluşturulur. Hücre sınırları kare dikdörtgenler halinde çizilir, okuma kafasının bulunduğu indeks hesaplanarak altına kırmızı renkli bir kafa işaretçisi (poligon üçgen) yerleştirilir ve sol üst köşeye güncel durum etiketi basılır. Hesaplama bittiğinde üretilen tüm PNG kareleri `imageio` modülü yardımıyla birleştirilerek `docs/images/tm_animation.gif` animasyon dosyası dinamik olarak oluşturulur.

### `benchmark.py` — Karşılaştırmalı Performans Analizi (Bonus C)
Bu betik, aynı dil problemini ("girdi içerisinde 11 alt dizgisinin aranması") çözen iki farklı mimariyi (`single_find_11.yaml` ve `ntm_find_11.yaml`) doğrusal olarak uzayan girdi boyutlarında ($N=10, 20, 30, 40, 50$) yarıştırır. Her iki motorun yürütme süreleri `time.perf_counter()` ile mikro saniye hassasiyetinde ölçülür. Elde edilen zaman verileri `matplotlib` kütüphanesi aracılığıyla çizgi grafiğe dökülerek `docs/comparison.png` adresine kaydedilir. Grafikte DTM'in doğrusal ($O(n)$) zaman eğrisine karşılık, NTM'in BFS mimarisinden dolayı dallanan arama ağacı maliyetinin yarattığı üstel artış deneysel olarak gözlemlenebilmektedir.

### Kritik Şerit Tasarım Kararı: Neden `dict`?
Şeridin `str` veya `list` yerine `dict[int, str]` olarak tasarlanması projenin en büyük mühendislik kararıdır. Python'da string veri tipleri değiştirilemez (immutable) olduğundan, şeride yazılan her yeni karakter bellekte tüm dizgenin kopyalanmasına ve yeni bir nesne oluşturulmasına sebep olur; bu da $O(n)$ zaman maliyeti demektir. Standart listeler ise negatif indeks aldıklarında Python'ın kendi dizilim mantığı gereği listenin sonuna atlama yaparlar. Oysa Turing makinelerinde başlangıç noktasının soluna geçmek (sol sonsuz şerit) temel bir kuraldır. Seyrek sözlük (sparse dict) tasarımı sayesinde negatif indeksler birer matematiksel koordinat olarak doğrudan key rolü oynamış, bellekte sadece veri yazılan hücreler tutularak hem bellek optimizasyonu sağlanmış hem de tüm okuma/yazma işlemleri $O(1)$ zaman karmaşıklığına indirgenmiştir.

---

## 3. Tasarlanan Turing Makineleri

Proje gereksinimleri doğrultusunda, karmaşıklık seviyeleri basitten zora doğru sıralanan 4 adet özgün Turing makinesi tasarımı yapılmıştır:

### TM-1: Unary → Binary Çevirici (`unary_to_binary.yaml`)
Şeride girilen $n$ adet yan yana `1` karakterinden oluşan tekli (unary) sayı sistemindeki girdi değerini, ikili (binary) sayı sistemine dönüştürür. Makine, girdi alanındaki her bir `1` sembolünü tek tek okuyup kopyalandığını belirtmek adına `X` karakteriyle işaretler. Ardından şeridin sağ tarafında oluşturulan `#` ayracının ötesine geçerek klasik bir ikili sayma (binary increment) ve elde taşıma (carry propagation) algoritması çalıştırır. İlk tasarım aşamasında karşılaşılan en büyük zorluk, ikili sayacın basamak taşırma (overflow) anlarında şeridin soluna doğru yeni ve dinamik bir En Anlamlı Bit (MSB) ekleme mantığının durum geçiş fonksiyonlarında yaratığı karmaşıklık olmuştur.

### TM-2: İki İkili Sayıyı Karşılaştıran TM (`binary_compare.yaml`)
Şeritte `#` karakteri ile birbirinden ayrılmış iki adet pozitif ikili sayıyı ($A \# B$) büyüklük yönünden karşılaştırır. Makine karmaşık bir zig-zag tarama mantığıyla çalışır. İlk sayının en anlamlı bitini (MSB) okur, harfi hafızasında tutmak adına özel bir duruma geçer ve karakteri `X` ile işaretler. Ardından hızla sağa koşarak ikinci sayının karşılık gelen bitini bulur ve karşılaştırır. Eğer $A$ sayısının biti `1`, $B$ sayısının karşılık gelen biti `0` ise $A > B$ olduğu kesinleşir ve makine kabul durumuna yönelir. Tek bir şerit üzerinde kafayı sürekli sola ve sağa yüzlerce kez kaydırmak zorunda kalmak durum sayısını (state) dramatik şekilde artırmış, bu durum projedeki Çok-Şeritli (Multi-tape) motor mimarisine olan ihtiyacı ve motivasyonu teorik olarak doğrulamıştır.

### TM-3: Dizgi Kopyalayıcı (`string_copy.yaml`)
Şerit üzerindeki alfanümerik bir $w$ kelimesini okuyarak, araya bir ayraç koyup `$w \# w$` formuna kopyalar. Makine, girdinin en solundaki karakteri okur; eğer karakter `a` ise bunu geçici olarak durum hafızasında tutmak için `q_copy_a` durumuna geçer ve şeritteki harfi `A` olarak günceller. Şeridin sonundaki boşluğa gidip ilgili harfi yazdıktan sonra tekrar sola dönerek ilk büyük harfli işaretçiyi arar. Tüm harfler kopyalandıktan sonra büyük harflerin tamamı (`A` ve `B` sembolleri) orijinal hallerine (`a` ve `b`) restore edilir. Bu makinedeki en kritik tasarım hatası, başlangıçta boşluk sembolü olarak `B` karakterinin seçilmesiydi; çünkü bu karakter büyük harf kopyalama işareti olan `B` ile çakışarak makineyi sonsuz döngüye sokuyordu. Boşluk sembolünün alt tire (`_`) olarak revize edilmesiyle sorun kökten çözülmüştür.

### TM-4: İkili Sayılarda 4'e Bölünebilme Kontrolü (`student_choice.yaml`)
Öğrenci inisiyatifi ve seçimi kapsamında tasarlanan bu makine, şeride girilen herhangi bir ikili sayının matematiksel olarak 4 ile tam bölünüp bölünemediğini denetler. Dijital mantık ve ikili sayı sisteminin yapısal özellikleri gereği, bir sayının 4'e ($2^2$) tam bölünebilmesi için sayının en sağdaki son iki basamağının kesinlikle `00` olması gerekmektedir. Makine, girdi dizgisinin üzerinden hızla geçerek şeridin en sağına (boşluk sınırına) kadar tarama yapar ($O(n)$). Boşluğa çarptığı an bir adım sola kayarak son biti kontrol eder; eğer bit `0` ise bir adım daha sola kayıp sondan ikinci biti kontrol eder. İki bit de `0` ise makine girdi dizgisini kabul eder, aksi takdirde reddeder. Karşılaşılan en büyük tasarım bug'ı, tek haneli `0` girdisi veya başında sıfır olan kısa girdilerde kafanın sınır dışına taşmasıydı; bu durum durum geçişlerine özel sınır kontrolleri eklenerek başarıyla optimize edilmiştir.

---

## 4. Kavramsal Tartışma

### Modern bir programlama dili (Python) ile Turing Makinesi arasındaki "boşluk" nedir?

Turing Makinesi; sonsuz bir şerit, bu şerit üzerinde hareket eden tek bir okuma/yazma kafası ve sonlu bir durum tablosundan ibaret olan, hesaplama kavramının en yalın ve minimal matematiksel modelidir. Python ise bu soyut matematiksel temelin üzerinde yükselen, donanım mimarilerini, işletim sistemi katmanlarını ve derleyici optimizasyonlarını barındıran yüksek seviyeli, çoklu paradigmalı modern bir programlama dilidir.

Hesaplama gücü (Computational Power) açısından incelendiğinde, modern programlama dilleri ile Turing Makinesi arasında teorik olarak **hiçbir fark yoktur.** Church-Turing tezinin de ortaya koyduğu üzere, modern bir süper bilgisayarla veya Python diliyle yazılabilen, hesaplanabilir her türlü algoritma, yeterli zaman ve şerit verildiğinde ilkel bir Turing makinesi tarafından da birebir çözülebilir. Dolayısıyla aradaki boşluk bir "güç" boşluğu değil, tamamen **"soyutlama seviyesi, ifade konforu ve kaynak yönetimi"** boşluğudur.

1.  **Bellek ve Erişim Modeli Farkı:** Python dili, Von Neumann mimarisinin getirdiği Rastgele Erişimli Bellek (RAM) gücünü arkasına alır. Bir dizinin veya listenin $n.$ elemanına erişmek Python'da `liste[n]` ifadesiyle donanımsal adresleme sayesinde ortalama $O(1)$ sürede tamamlanır. Turing makinesinde ise rastgele erişim yoktur; sıralı (sequential) bellek modeli geçerlidir. Şeridin 500 hücre ilerisindeki bir bit veriye ulaşmak veya onu güncellemek için okuma kafasının fiziksel olarak 500 adım boyunca tek tek sağa kayması gerekir; bu da erişim maliyetini doğrudan $O(n)$ yapar.
2.  **Kontrol Akışı ve İfade Gücü:** Python; `for/while` döngüleri, `if/else` koşullu blokları, fonksiyon çağrıları (call stack yapısı) ve nesneye yönelik soyutlamalar sunarak yazılımcının yalnızca "algoritmik niyete" odaklanmasını sağlar. Turing makinesinde ise bu yüksek seviyeli kontrol yapılarının hiçbiri mevcut değildir. En basit bir döngü veya koşul mekanizması bile, mikro düzeyde durum geçiş tablolarıyla ($\delta$ fonksiyonlarıyla) ve alt seviye şerit işaretçileriyle manuel olarak kurulmak zorundadır. Python yazılımcıya "ne yapılacağını" söyleme konforu sunarken, TM yazılımcıyı "her bir bit adımında donanımın nasıl davranacağını" tasarlamaya mecbur bırakır.

Bu projede geliştirdiğimiz `binary_compare` veya `string_copy` makineleri bu boşluğu somut olarak anlamamı sağladı. Python'da tek bir operatörle (`>`) veya basit bir string eklemesiyle (`w + '#' + w`) tek satırda çözülen problemler, Turing makinesi dünyasına indirgendiğinde onlarca durum, yüzlerce kafa hareketi ve karmaşık şerit işaretleme algoritmaları gerektirmektedir. Turing Makinesi hesaplamanın çıplak ve teorik özünü görünür kılarken, Python bu özü katmanlarca soyutlayarak insan üretkenliğini maksimize eder.

---

## 5. Sınırlar ve İleri Çalışma

TuringLab simülasyon motoru, otomata varyantlarını çalıştırma kabiliyeti açısından oldukça esnek ve kararlı bir yapıya ulaşmış olsa da, teorik ve pratik bazı yapısal sınırları barındırmaktadır:

* **Halting Problemi ve Zaman Aşımı:** Motor, sonsuz döngüye giren deterministik makineleri engellemek adına yapay bir `max_steps` sınırına bağımlıdır. Bir makinenin sonsuz döngüde mi olduğu yoksa gerçekten uzun bir hesaplama mı yaptığı sorusu, Alan Turing'in ünlü *Halting Problem* (Durma Problemi) teoremine dayanır ve bu durum simülatörün teorik sınırlarındandır.
* **NTM Bellek Tüketimi Patlaması:** Non-deterministik motorun kullandığı BFS algoritması, her bir ayrışma anında (branching) mevcut şeridin tam bir kopyasını (`.copy()`) belleğe alır. Girdi uzunluğu ve dallanma katsayısı arttığında bellek tüketimi üstel ($O(b^d)$) olarak büyür. Bu pratik darboğaz `max_branches` korumasıyla dizginlense de, çok katmanlı karmaşık dillerin NTM ile taranmasını sınırlandırır.
* **Görselleştirici Sınırları:** Mevcut görselleştirme modülü (`visualizer.py`), mimari olarak yalnızca tek şeritli makinelerin hareketlerini destekleyecek şekilde tasarlanmıştır. Çok şeritli (Multi-tape) makinelerin aynı anda hareket eden 3 farklı kafasını eşzamanlı olarak tek bir GIF üzerinde render etme yeteneğine sahip değildir.

### İleri Çalışma Önerileri
Projeye gelecekte devam edilmesi durumunda eklenebilecek en vizyoner modül, şüphesiz bir **Evrensel Turing Makinesi (Universal Turing Machine - UTM)** katmanı olacaktır. Mevcut mimaride motorumuz YAML kurallarını okuyan harici bir Python programıdır. UTM modülü geliştirildiği takdirde; herhangi bir Turing makinesinin geçiş tabloları ve kuralları özel bir ikili kodlama şemasıyla (gösterim dizesi) string haline getirilerek, girdi kelimesinin hemen önüne şeridin kendisine yazılacaktır. Motor, yalnızca tek bir evrensel UTM kural dosyasını çalıştıracak; bu evrensel dosya şeridin üzerindeki diğer makinenin kurallarını bizzat "şerit üzerinden okuyarak" simüle edecektir. Bu hamle, projenin meta-hesaplama (yazılımın yazılımı simüle etmesi) noktasındaki en üst teorik aşaması olacaktır.

---

## 6. Kaynakça

- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.
- Çetinkaya, A. (2026). *TuringLab Öğrenci El Kitabı ve Proje Kılavuzu*. Selçuk Üniversitesi Bilgisayar Mühendisliği Bölümü Yayınları.
- Python Software Foundation. (2026). *Python Language Reference and Standard Library (v3.12)*. https://docs.python.org
- Pillow (PIL) Core Development Team. (2026). *Pillow Documentation (v10.2)*. https://pillow.readthedocs.io