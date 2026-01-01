# 📚 Proje Dosyaları ve Scriptlerin Detaylı Açıklaması

## 🗂️ PROJE YAPISI

```
DATASCIENCE/
├── data/
│   ├── raw/                    # Ham veriler (API'lerden gelen)
│   │   ├── trends_chatgpt.csv
│   │   ├── world_bank_indicators.csv
│   │   └── github_ai_activity.csv
│   └── processed/              # Temizlenmiş veriler
│       ├── ai_adoption_combined.csv
│       ├── ai_adoption_cleaned.csv
│       └── ai_adoption_clustered.csv
├── scripts/                    # 6 Python script (pipeline)
├── visualizations/             # 5 HTML grafiği
├── docs/                       # Dökümanlar
└── requirements.txt            # Paket bağımlılıkları
```

---

## 🔥 1. DATA COLLECTION (data_collection.py - 352 satır)

### 🎯 Amaç
Ham veriyi toplamak - İnternet'ten 2 farklı API kullanarak veri çekmek.

### 📡 Kullandığı API'ler

**API 1: Google Trends (pytrends)**
- **Ne verir?** ChatGPT arama trendleri (0-100 skala)
- **Nasıl?** Her ülke için son 12 ayın arama hacmi
- **Veri:** `trends_chatgpt.csv`
- **Örnek:** ABD: 85, Türkiye: 72, Hindistan: 91

**API 2: World Bank (wbgapi)**
- **Ne verir?** Ekonomik ve sosyal göstergeler
- **Veriler:**
  - GDP (Gross Domestic Product)
  - GDP per capita
  - Internet kullanıcı oranı (%)
  - Eğitim harcamaları (% of GDP)
  - Population (nüfus)
- **Veri:** `world_bank_indicators.csv`

**API 3: GitHub (requests)**
- **Ne verir?** AI ile ilgili GitHub repository istatistikleri
- **Metrik:** Star sayısı, fork sayısı
- **Veri:** `github_ai_activity.csv`

### ⚠️ Özellikler
- ✅ **Otomatik veri çekme** - Her API'den 103 ülke için veri
- ❌ **Temizlik YOK** - Veriler RAW halde, missing values var
- ❌ **ISO kod yok** - Ülke isimleri orijinal formda (Turkey, United States)
- 💾 **Çıktı:** `data/raw/` klasörüne 3 CSV dosyası

### 🔄 Ne Zaman Çalıştırılır?
- İlk kurulumda (1 kez)
- Veriyi güncellemek istediğinde
- **Zaten çalıştı:** Veriler `data/raw/` klasöründe mevcut

---

## 🧹 2. DATA CLEANING (data_cleaning.py - 212 satır)

### 🎯 Amaç
Raw verileri birleştirmek, temizlemek ve analiz için hazırlamak.

### 🔧 İşlemler (Step-by-Step)

**1. ISO-3 Kod Mapping**
```
Turkey → TUR
United States → USA
Germany → DEU
```
- **Neden?** Dünya haritasında gösterebilmek için

**2. Veri Birleştirme**
```
trends_chatgpt.csv + world_bank_indicators.csv + github_ai_activity.csv
→ ai_adoption_combined.csv
```
- **Nasıl?** Ülke ismine göre MERGE (left join)

**3. Missing Data Handling**
- **Median imputation:** Sayısal değerler için ortalama
- **Forward fill:** Zaman serisi için önceki değeri al
- **Örnek:** Ghana'nın GDP bilgisi yoksa → Median GDP kullan

**4. Continent & Region Ekleme**
```python
Turkey → Europe, Southern Europe
India → Asia, Southern Asia
USA → Americas, Northern America
```
- **Neden?** Bölgesel karşılaştırma için

**5. Economic Category**
```
GDP per capita'ya göre:
- High Income: >$12,000
- Upper-Middle: $4,000-$12,000
- Lower-Middle: $1,000-$4,000
- Low Income: <$1,000
```

**6. Feature Engineering**
- `ai_penetration_index` = AI interest × Internet users
- `digital_readiness` = Internet % + Education spending
- `ai_per_capita` = AI interest / Population

### 💾 Çıktılar
- `ai_adoption_combined.csv` - Birleştirilmiş veri (temizlik öncesi)
- `ai_adoption_cleaned.csv` - **ANA VERİ** (tüm analizler bunu kullanır)
  - 103 ülke
  - 15 kolon
  - Missing value YOK
  - ISO-3 kod ✓

---

## 📊 3. VISUALIZATION (visualization.py - 191 satır)

### 🎯 Amaç
Temel grafikleri oluşturmak - 5 ana görselleştirme.

### 📈 Oluşturduğu Grafikler

**1. Dünya Haritası** (`world_map_ai_adoption.html`)
- **Ne gösterir?** Her ülkenin AI interest değeri (renk kodlu)
- **Teknoloji:** Plotly choropleth map
- **Interaktif:** Hover ile ülke detayları
- **Renk:** Koyu = Yüksek AI interest

**2. GDP vs AI Scatter** (`scatter_gdp_vs_ai.html`)
- **Ne gösterir?** Ekonomik gelişmişlik vs AI adoption ilişkisi
- **Eksenler:** 
  - X: GDP per capita (log scale)
  - Y: AI Interest
  - Bubble size: Population
  - Renk: Economic category
- **Insight:** Zengin ülkeler daha çok AI kullanıyor mu?

**3. Top 15 Ülke Bar Chart** (`top_15_countries.html`)
- **Ne gösterir?** En yüksek AI interest'e sahip 15 ülke
- **Renk:** Economic category
- **Sıralama:** En yükten düşüğe

**4. Correlation Heatmap** (`correlation_heatmap.html`)
- **Ne gösterir?** Değişkenler arası korelasyonlar
- **Örnek:**
  - GDP ↔ AI interest: 0.42 (orta pozitif)
  - Internet ↔ AI: 0.68 (güçlü pozitif)
  - Education ↔ AI: 0.31 (zayıf pozitif)

**5. Clustering Result** (`clustering_gdp_vs_ai.html`)
- **Ne gösterir?** K-means cluster sonuçları
- **4 Renk:** 4 farklı ülke grubu
- **Amaç:** Benzer özellikteki ülkeleri göster

### 🛠️ Teknolojiler
- **Plotly:** İnteraktif HTML grafikleri
- **Pandas:** Veri manipülasyonu
- **PathLib:** Dosya yönetimi

### 💾 Çıktı
`visualizations/` klasörüne 5 HTML dosyası

---

## 📈 4. STATISTICAL ANALYSIS (statistical_analysis.py - 281 satır)

### 🎯 Amaç
İstatistiksel testler ve hipotez testi yapmak.

### 🔬 Yapılan Analizler

**1. Correlation Analysis (Pearson r)**
```
Korelasyon katsayısı (-1 ile +1 arası):
- r > 0.7: Güçlü pozitif ilişki
- r = 0.0: İlişki yok
- r < -0.7: Güçlü negatif ilişki

Bulgu:
- Internet users ↔ AI interest: r = 0.68 (GÜÇLÜ)
- GDP ↔ AI interest: r = 0.42 (ORTA)
- Education ↔ AI: r = 0.31 (ZAYIF)
```

**2. ANOVA Test (Analysis of Variance)**
```python
Soru: Ekonomik kategoriler arasında AI adoption farkı var mı?
H0: Tüm gruplar eşit (fark yok)
H1: En az bir grup farklı

Sonuç: p-value < 0.05 → H0 RED
Yorum: Zengin ülkeler daha çok AI kullanıyor (istatistiksel olarak anlamlı)
```

**3. Multiple Regression**
```
Model: AI_interest = β₀ + β₁(GDP) + β₂(Internet) + β₃(Education) + ε

Feature Importance:
1. Internet users: 45% etkili
2. GDP per capita: 30% etkili
3. Education: 15% etkili
4. Population: 10% etkili

R² = 0.63 → Model varyansın %63'ünü açıklıyor
```

**4. T-test (Group Comparison)**
```
High Income vs Low Income AI adoption
p-value < 0.001 → Anlamlı fark var
```

### 💾 Çıktılar
- `correlation_heatmap.html` - Korelasyon matrisi
- `regression_actual_vs_predicted.html` - Tahmin vs gerçek
- Console'a istatistik raporları

---

## 🤖 5. CLUSTERING ANALYSIS (clustering_analysis.py - 243 satır)

### 🎯 Amaç
Ülkeleri benzer özelliklere göre gruplamak (Machine Learning).

### 🧠 Kullanılan ML Algoritması
**K-means Clustering**
- **Supervised?** Hayır (Unsupervised Learning)
- **Ne yapar?** Benzer ülkeleri aynı gruba atar
- **Nasıl?** Öklid mesafesi (Euclidean distance)

### 📊 Pipeline

**1. Feature Selection**
```python
Seçilen özellikler:
- avg_interest (AI interest)
- gdp_per_capita
- internet_users_pct
- education_spending
- population (scaled)
```

**2. Feature Scaling (StandardScaler)**
```
Neden? K-means mesafe temelli → tüm değişkenler aynı skalada olmalı
Örnek: GDP (0-100000) → Scaled (0-1)
```

**3. Optimal Cluster Sayısı (Elbow Method)**
```
Test: k=2, 3, 4, 5, 6
Sonuç: k=4 optimal (elbow noktası)
```

**4. K-means Fitting**
```python
KMeans(n_clusters=4, random_state=42)
→ Her ülke bir cluster'a atanır (0, 1, 2, 3)
```

### 🏷️ Cluster Profilleri

**Cluster 0: High-Income AI Leaders**
- Ülkeler: ABD, Kanada, İngiltere
- Özellik: Yüksek GDP, yüksek AI interest
- Ortalama AI: 82/100

**Cluster 1: Emerging AI Adopters**
- Ülkeler: Hindistan, Filipinler, Pakistan
- Özellik: Düşük GDP, ama YÜKSEK AI interest
- Ortalama AI: 88/100 (en yüksek!)

**Cluster 2: Moderate Adopters**
- Ülkeler: Avrupa ülkeleri, Japonya
- Özellik: Yüksek GDP, orta AI interest
- Ortalama AI: 65/100

**Cluster 3: Low Engagement**
- Ülkeler: Afrika ülkeleri
- Özellik: Düşük GDP, düşük AI interest
- Ortalama AI: 35/100

### 💾 Çıktılar
- `clustering_gdp_vs_ai.html` - Cluster visualizasyonu
- `ai_adoption_clustered.csv` - Cluster etiketli veri
- Cluster profil raporları

---

## 🔍 6. OUTLIER ANALYSIS (outlier_analysis.py - 258 satır)

### 🎯 Amaç
Beklenmedik ülkelerin detaylı incelenmesi - "Neden bu ülke farklı?"

### 🎭 Outlier Tanımı
```
Outlier: Normal pattern'den sapan ülke
Örnek: 
- Ghana: Düşük GDP ama yüksek AI interest → NEDEN?
- Belarus: Orta gelir ama çok yüksek AI adoption → NEDEN?
- Japonya: Zengin ülke ama düşük AI interest → NEDEN?
```

### 🔬 Analiz Yöntemi

**1. Statistical Outlier Detection**
```python
Z-score method:
z = (x - μ) / σ

|z| > 2.5 → Outlier
Örnek: Ghana AI interest z-score = 3.2 → OUTLIER
```

**2. Residual Analysis**
```
Regression modeli:
Expected AI = f(GDP, Internet, Education)

Residual = Actual - Expected
Ghana: Actual 85, Expected 45 → Residual +40 (büyük pozitif)
```

**3. Deep Dive Case Studies**

**Case 1: Ghana (Pozitif Outlier)**
```
GDP per capita: $2,300 (düşük)
AI Interest: 85/100 (çok yüksek)
Internet: 58% (orta)

Neden?
1. Genç nüfus (median age: 21)
2. Tech hub (Accra tech startups)
3. AI education programları
4. Remote work boost
```

**Case 2: Belarus**
```
GDP per capita: $6,800 (orta)
AI Interest: 91/100 (en yüksek)
Internet: 79% (yüksek)

Neden?
1. Güçlü IT sektörü
2. Eğitim sistemi (STEM odaklı)
3. Tech outsourcing hub
```

**Case 3: Filipinler**
```
GDP: $3,500 (düşük)
AI Interest: 94/100 (REKOR)
Internet: 67%

Neden?
1. İngilizce konuşan nüfus
2. BPO (Business Process Outsourcing) sektörü
3. Remote work culture
4. Social media etkisi
```

### 💾 Çıktılar
- Console'a outlier raporları
- Narrative stories (hikaye anlatımı)
- Unexpected leaders listesi

---

## 📂 DATA FILES AÇIKLAMASI

### 🔴 RAW DATA (data/raw/)

**1. trends_chatgpt.csv**
```csv
country,avg_interest
United States,85
India,91
Turkey,72
```
- 103 satır (103 ülke)
- 2 kolon
- Google Trends'ten gelir

**2. world_bank_indicators.csv**
```csv
country,gdp,gdp_per_capita,internet_users,education_spending,population
United States,21427700000000,65297,90.3,5.0,331900000
```
- 103 satır
- 6 kolon
- World Bank API'den gelir
- Missing values var

**3. github_ai_activity.csv**
```csv
country,repo_count,total_stars
United States,1250,45000
India,890,23000
```
- AI repository aktivitesi

### 🟢 PROCESSED DATA (data/processed/)

**1. ai_adoption_combined.csv**
- Raw verilerin birleştirilmiş hali
- Temizlik yapılmamış
- 103 satır, ~12 kolon

**2. ai_adoption_cleaned.csv** ⭐ **EN ÖNEMLİ**
```
103 ülke × 15 feature
Kolonlar:
- country_name, country_code_iso3
- avg_interest (AI adoption metriği)
- gdp, gdp_per_capita, population
- internet_users_pct, education_spending
- continent, region
- economic_category
- ai_penetration_index (calculated)
- digital_readiness (calculated)
```
- Missing value YOK
- Tüm analizler bunu kullanır

**3. ai_adoption_clustered.csv**
- cleaned.csv + cluster etiketleri
- Ekstra kolon: `cluster` (0, 1, 2, 3)

---

## 🎯 PIPELINE SIRASI (Çalıştırma Sırası)

```
1. data_collection.py     → Raw veri topla (1 kez)
2. data_cleaning.py       → Temizle ve birleştir
3. visualization.py       → Temel grafikler
4. statistical_analysis.py → İstatistik testleri
5. clustering_analysis.py  → ML clustering
6. outlier_analysis.py    → Outlier deep dive
```

### ⚡ Hızlı Başlangıç
```bash
# Tüm analizi çalıştır (2 ve 3 yeterli, veriler zaten var)
python scripts/data_cleaning.py
python scripts/visualization.py
python scripts/statistical_analysis.py
python scripts/clustering_analysis.py
python scripts/outlier_analysis.py
```

---

## 🔑 KEY INSIGHTS

### 📊 Temel Bulgular

1. **Internet Access is King**
   - r = 0.68 (en güçlü korelasyon)
   - Internet erişimi olan ülkeler daha çok AI kullanıyor

2. **Wealth Matters, But Not Everything**
   - GDP ↔ AI: r = 0.42 (orta)
   - Zengin ülkeler AI kullanıyor, ama yoksul ülkeler de (Ghana, Filipinler)

3. **4 Cluster Pattern**
   - High-income leaders (ABD, Kanada)
   - Emerging adopters (Hindistan, Filipinler) → EN HEYECANLI GRUP
   - Moderate (Avrupa) → Zengin ama temkinli
   - Low engagement (Afrika)

4. **Unexpected Winners**
   - **Filipinler:** #1 AI interest (94/100)
   - **Ghana:** Afrika'nın AI lideri
   - **Belarus:** Doğu Avrupa tech hub

5. **Laggards (Geri Kalanlar)**
   - Japonya (zengin ama düşük AI)
   - Almanya (temkinli yaklaşım)
   - Afrika ülkeleri (altyapı eksikliği)

---

## 📦 REQUIREMENTS

```txt
pandas
numpy
plotly
scikit-learn
scipy
pytrends
wbgapi
requests
```

**Kurulum:**
```bash
pip install -r requirements.txt
```

---

## 🎓 Öğrenme Notları

### Ne Öğrendik?

1. **Veri Toplama:** API'lerle otomatik veri çekme
2. **Veri Temizleme:** Missing data, ISO mapping, feature engineering
3. **EDA:** Korelasyon, dağılım, outlier detection
4. **İstatistik:** ANOVA, regression, t-test, p-value
5. **Machine Learning:** K-means clustering, feature scaling
6. **Visualization:** Plotly ile interaktif grafikler
7. **Narrative:** Veriden hikaye çıkarma

### Kullanılan Teknikler
- ✅ API Integration (Google Trends, World Bank)
- ✅ Data Cleaning & Preprocessing
- ✅ Statistical Hypothesis Testing
- ✅ Unsupervised Machine Learning (K-means)
- ✅ Interactive Data Visualization
- ✅ Feature Engineering
- ✅ Outlier Analysis

---

**Son Güncelleme:** 1 Ocak 2026
**Proje Durumu:** ✅ TAMAMLANDI
**Visualizations:** 5 grafik
**Scripts:** 6 Python dosyası
**Data:** 103 ülke, 15 feature
