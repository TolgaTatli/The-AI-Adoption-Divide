# Proje Dokümantasyonu
## How Landscapes and Climate Shape Global Musical Tools

### Proje Yapısı Rehberi

#### 1. Veri Toplama (`scripts/data_collection.py`)
- The Met Museum API'den veri çeker
- Ham veriyi `data/raw/` klasörüne kaydeder
- JSON ve CSV formatlarında çıktı verir

#### 2. Veri Temizleme (`notebooks/02_data_cleaning.ipynb`)
- Eksik verileri analiz eder
- Coğrafi bilgileri standardize eder
- Malzeme bilgilerini parse eder
- Temiz veriyi `data/processed/` klasörüne kaydeder

#### 3. Ana Analiz (`notebooks/03_analysis.ipynb`)
- Coğrafi dağılım analizi
- Malzeme-coğrafya ilişkisi
- İstatistiksel testler
- Enstrüman ailesi analizleri

#### 4. Görselleştirme (`scripts/visualization.py`)
- İnteraktif dünya haritaları
- Choropleth haritalar
- Malzeme ve enstrüman ailesi dağılımları

### Çalıştırma Sırası

```bash
# 1. Sanal ortam oluştur ve aktifleştir
python -m venv venv
venv\Scripts\activate

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. Veri topla
python scripts/data_collection.py

# 4. Jupyter notebook'ları çalıştır
jupyter notebook notebooks/02_data_cleaning.ipynb
jupyter notebook notebooks/03_analysis.ipynb

# 5. Görselleştirmeleri oluştur
python scripts/visualization.py
```

### Önemli Notlar

#### API Kullanımı
- The Met Museum API ücretsizdir
- Rate limiting: İstekler arasında 0.5 saniye bekleme
- Toplam ~5000 enstrüman verisi mevcut

#### Veri Kalitesi
- Bazı enstrümanların coğrafi bilgisi eksik olabilir
- Malzeme bilgileri metin olarak gelir, parsing gerekir
- Tarih bilgileri aralık olarak verilir

#### Görselleştirme
- Plotly ile interaktif HTML haritalar oluşturulur
- Matplotlib/Seaborn ile statik grafikler
- Tüm görseller `visualizations/` klasöründe saklanır

### Poster ve Sunum İçin Öneriler

1. **Ana Bulgular**
   - En yaygın malzemeler ve coğrafi dağılımları
   - İstatistiksel olarak anlamlı ilişkiler
   - Çarpıcı örnekler (Didgeridoo, Morin Khuur vb.)

2. **Görselleştirmeler**
   - Dünya haritası (ana görsel)
   - Isı haritaları (malzeme-kıta ilişkisi)
   - Zaman çizelgesi (malzeme evrimi)

3. **Hikaye Akışı**
   - Giriş: Araştırma sorusu
   - Yöntem: Veri toplama ve temizleme
   - Bulgular: Ana analizler
   - Sonuç: Coğrafyanın müziğe etkisi

### İletişim

Sorularınız için:
- Proje ekibi: [İsim 1], [İsim 2]
- Email: [email]
- GitHub: [repo link]

### Referanslar

1. The Metropolitan Museum of Art Collection API
   - https://metmuseum.github.io/

2. MIMO - Musical Instrument Museums Online
   - http://www.mimo-international.com/

3. UNESCO Intangible Cultural Heritage
   - https://ich.unesco.org/

4. Etnomüzikoloji kaynakları:
   - [Eklenecek]

---

**Son Güncelleme**: Ocak 2026
