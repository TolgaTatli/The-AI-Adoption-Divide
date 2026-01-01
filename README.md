# The AI Adoption Divide: How Countries Embrace AI Tools

## 🤖 Proje Özeti

Bu proje, yapay zeka araçlarının (ChatGPT, Midjourney, GitHub Copilot vb.) dünya çapında nasıl benimsendiğini ve ekonomik gelişmişlik düzeyi ile ilişkisini inceleyen kapsamlı bir veri bilimi çalışmasıdır.

### Araştırma Sorusu
*"Hangi ülkeler yapay zeka araçlarını daha hızlı benimsiyor ve bu benimseme ekonomik gelişmişlik, eğitim düzeyi ve teknolojik altyapı ile nasıl bir ilişki içinde?"*

## 📊 Proje Yapısı

```
DATASCIENCE/
│
├── data/
│   ├── raw/              # Ham veri (API'den çekilen)
│   ├── processed/        # Temizlenmiş ve işlenmiş veri
│   └── external/         # İklim ve coğrafi ek veriler
│
├── scripts/
│   ├── data_collection.py      # Google Trends API veri çekme
│   ├── data_cleaning.py        # Veri temizleme işlemleri
│   └── visualization.py        # Görselleştirme fonksiyonları
│
├── notebooks/
│   ├── 01_data_collection.ipynb    # Veri toplama süreci
│   ├── 02_data_cleaning.ipynb      # Veri temizleme ve keşif
│   ├── 03_analysis.ipynb           # Ana analiz ve istatistikler
│   └── 04_visualization.ipynb      # Görselleştirmeler
│
├── visualizations/       # Oluşturulan grafikler ve haritalar
├── docs/                 # Proje dokümantasyonu ve poster
└── requirements.txt      # Gerekli Python paketleri
```

## 🔧 Kurulum

### Gereksinimler
- Python 3.8+
- pip paket yöneticisi

### Kurulum Adımları

1. Repository'yi klonlayın veya indirin

2. Sanal ortam oluşturun (önerilen):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### 1. Veri Toplama
The Met Museum API'den enstrüman verilerini çekin:
```bash
python scripts/data_collection.py
```

### 2. Veri Analizi
Jupyter Notebook'ları sırasıyla çalıştırın:
```bash
jupyter notebook notebooks/01_data_collection.ipynb
```

### 3. Görselleştirme
Analiz sonuçlarını görselleştirin:
```bash
python scripts/visualization.py
```

## 📈 Veri Kaynakları

1. **Google Trends API (pytrends)**
   - AI araçlarının arama trendleri (ChatGPT, Midjourney, etc.)
   - Ülke bazında popülerlik verileri
   
2. **World Bank API**
   - GDP per capita (ekonomik gelişmişlik)
   - Eğitim indeksleri
   - İnternet penetrasyon oranları

3. **GitHub API**
   - AI/ML repository sayıları ülke bazında
   - Contributor dağılımları

## 🌍 Örnek Analizler

### Öne Çıkan Bulgular:
- **Gelişmiş Ülkeler**: Erken benimseme, yüksek arama hacmi
- **Gelişmekte Olan Ülkeler**: Hızlı büyüme, mobil odaklı kullanım
- **Ekonomik Korelasyon**: GDP ile AI kullanımı arasında güçlü ilişki
- **Eğitim Etkisi**: Yüksek eğitim = Daha yüksek AI adaptasyonu

## 👥 Proje Ekibi

- [İsim 1]
- [İsim 2]

## 📅 Proje Zaman Çizelgesi

- **Veri Toplama**: Ocak 2026
- **Veri Temizleme ve Analiz**: Ocak 2026
- **Görselleştirme ve Poster**: Ocak-Şubat 2026
- **Sunum**: Şubat 2026

## 📝 Teslim Edilecekler

1. ✅ Tüm kodlar ve notebook'lar
2. ✅ Profesyonel poster (dijital)
3. ✅ Sunum slaytları
4. ✅ Final rapor

## 🔗 Referanslar

- The Metropolitan Museum of Art Collection API
- UNESCO Intangible Cultural Heritage Database
- MIMO - Musical Instrument Museums Online

## 📄 Lisans

Bu proje eğitim amaçlıdır.

---

**Not**: Bu proje, veri bilimi tekniklerinin etnomüzikoloji alanına uygulanmasını göstermektedir. Bulgular, kültürel ve coğrafi faktörlerin müzik teknolojisini nasıl şekillendirdiğine dair değerli içgörüler sunmaktadır.
