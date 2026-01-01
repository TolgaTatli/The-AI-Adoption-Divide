# 🚀 Projeyi Çalıştırma Rehberi - BAŞLANGIÇ
### The AI Adoption Divide - How Economic Development Shapes Global AI Tool Adoption


## 📋 Dosyalar ve Ne İşe Yaradıkları

### 🔵 PYTHON SCRIPTLER (scripts/ klasörü)

```
scripts/
├── data_collection.py        ← 1️⃣ İLK BUNU ÇALIŞTIR
│   └── Google Trends + World Bank'ten 103 ülke verisi toplar
│
├── data_cleaning.py          ← 2️⃣ SONRA BUNU
│   └── Toplanan veriyi temizler, ISO-3 ekler, kategoriler oluşturur
│
├── visualization.py          ← 3️⃣ SONRA BUNU (Basit grafikler)
│   └── Dünya haritası + scatter plot oluşturur
│
├── statistical_analysis.py  ← 4️⃣ İSTERSEN BU (İstatistik)
│   └── Correlation, ANOVA, regression testleri yapar
│
├── clustering_analysis.py   ← 5️⃣ İSTERSEN BU (ML)
│   └── K-means ile ülkeleri 4 gruba ayırır
│
├── advanced_visualizations.py ← 6️⃣ İSTERSEN BU (Gelişmiş grafikler)
│   └── 11 tane advanced grafik oluşturur
│
└── outlier_analysis.py      ← 7️⃣ İSTERSEN BU (Sürpriz ülkeler)
    └── Ghana, Belarus gibi outlier'ları analiz eder
```

---

## 🎯 HIZLI BAŞLANGIÇ (5 Dakika)

### Adım 1: Sanal Ortamı Aktif Et
```powershell
# Terminal'i aç (VS Code içinde Ctrl+`)
cd "C:\Users\Tolga Tatlı\SENG Projects\DATASCIENCE"

# Sanal ortamı aktif et
.\venv\Scripts\Activate.ps1
```

**✅ Başarılı olursa:** Komut satırının başında `(venv)` yazısı görünür

**❌ Hata alırsan:**
```powershell
# PowerShell execution policy hatası
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Adım 2: Veri Topla (ZATENVERİLER VAR!)
```powershell
python scripts/data_collection.py
```

**⚠️ ÖNEMLİ:** Veriler zaten var! Bu adımı **atla** çünkü:
- `data/raw/trends_chatgpt.csv` ✅ Var
- `data/raw/world_bank_indicators.csv` ✅ Var

**Ne zaman çalıştırmalısın?**
- Sadece yeni veri toplamak istersen
- Ülke listesini değiştirirsen

**Süre:** ~5-10 dakika (103 ülke için)

---

### Adım 3: Veriyi Temizle
```powershell
python scripts/data_cleaning.py
```

**Ne yapar?**
- Ham veriyi okur
- ISO-3 kodları ekler (Plotly için)
- Region/Continent ekler
- Economic category oluşturur
- AI Adoption Score hesaplar

**Çıktı:**
```
✅ 103 kayıt yüklendi
✅ Temizleme tamamlandı!
💾 Kaydedildi: data/processed/ai_adoption_cleaned.csv

Final dataset: 103 ülke, 15 sütun
```

**Süre:** ~2-3 saniye

---

### Adım 4: Grafikler Oluştur
```powershell
python scripts/visualization.py
```

**Ne yapar?**
- Dünya haritası (choropleth)
- GDP vs AI scatter plot
- Top 20 ülke bar chart

**Çıktı:**
```
✅ 103 kayıt yüklendi
🗺️  Dünya haritası oluşturuluyor...
✅ Harita kaydedildi: visualizations/world_map_ai_adoption.html
📊 GDP vs AI Interest grafiği oluşturuluyor...
✅ Scatter plot kaydedildi: visualizations/scatter_gdp_vs_ai.html
📊 Top 20 ülke grafiği oluşturuluyor...
✅ Bar chart kaydedildi: visualizations/top_20_countries.html
```

**Süre:** ~3-5 saniye

**Grafikleri görmek için:**
```powershell
# Haritayı aç
Start-Process "visualizations\world_map_ai_adoption.html"

# Scatter plot'u aç
Start-Process "visualizations\scatter_gdp_vs_ai.html"
```

---

## 🎓 DETAYLI ANALİZ (İleri Seviye)

### Adım 5A: İstatistiksel Analiz
```powershell
python scripts/statistical_analysis.py
```

**Ne yapar?**
- ✅ Correlation matrix (GDP vs AI, Education vs AI, etc.)
- ✅ ANOVA test (Ekonomik kategoriler arası fark var mı?)
- ✅ Multiple regression (GDP + Education + Internet → AI?)
- ✅ Feature importance plot

**Çıktı:**
```
📊 KORELASYON ANALİZİ:
avg_interest ↔ gdp_per_capita: r = +0.199, p = 0.0440 ✅
avg_interest ↔ tertiary_education: r = -0.041, p = 0.6884
avg_interest ↔ internet_users_pct: r = +0.216, p = 0.0292 ✅

📊 ANOVA TESTİ:
F-statistic: 5.6730
p-value: 0.004637 ✅ (Anlamlı fark var!)

📊 ÇOKLU REGRESYON:
R² Score: 0.2568
GDP katsayısı: +3.6186 (en güçlü!)
```

**Grafik Çıktıları:**
- `visualizations/correlation_heatmap.html`
- `visualizations/feature_importance.html`
- `visualizations/regression_actual_vs_predicted.html`

**Süre:** ~5 saniye

---

### Adım 5B: Machine Learning (Clustering)
```powershell
python scripts/clustering_analysis.py
```

**Ne yapar?**
- ✅ K-means clustering (k=4)
- ✅ Elbow method (optimal k bulma)
- ✅ Silhouette score (kalite ölçümü)
- ✅ 4 adoption profile tanımlar

**Çıktı:**
```
🤖 K-MEANS CLUSTERING

Optimal k: 4 cluster
Silhouette Score: 0.324

📊 CLUSTER PROFİLLERİ:

Cluster 0: "Early Adopters" (n=24)
  - Ortalama AI: 34.2%
  - Ortalama GDP: $19,438
  - Örnek: Mexico, Poland, Colombia

Cluster 1: "Fast Followers" (n=20)
  - Ortalama AI: 43.6%
  - Ortalama GDP: $62,150
  - Örnek: USA, UK, Germany

Cluster 2: "Moderate Users" (n=2)
  - Ortalama AI: 26.1%
  - Ortalama GDP: $7,854
  - Örnek: China, India

Cluster 3: "Laggards" (n=7)
  - Ortalama AI: 39.9%
  - Ortalama GDP: $4,787
  - Örnek: Indonesia, Pakistan
```

**Grafik Çıktıları:**
- `visualizations/clustering_elbow.html` (Optimal k seçimi)
- `visualizations/clustering_gdp_vs_ai.html` (2D scatter)
- `visualizations/clustering_3d.html` (3D scatter)
- `visualizations/clustering_parallel.html` (Parallel coordinates)

**Süre:** ~5-7 saniye

---

### Adım 5C: Gelişmiş Görselleştirmeler
```powershell
python scripts/advanced_visualizations.py
```

**Ne yapar?**
- ✅ Box plots (ekonomik kategori, region)
- ✅ Violin plots (continent)
- ✅ Radar charts (regional comparison)
- ✅ Sunburst chart (hierarchical)
- ✅ Treemap (population-weighted)
- ✅ Heatmap matrix (top 30 countries)

**Çıktı:**
```
📊 GELİŞMİŞ GÖRSELLEŞTİRMELER

✅ Box plot (economic_category) oluşturuldu
✅ Box plot (regions) oluşturuldu
✅ Violin plot (continents) oluşturuldu
✅ Regional comparison (4 grafik) oluşturuldu
✅ Distribution plots (2 grafik) oluşturuldu
✅ Treemap (population) oluşturuldu
✅ Heatmap matrix (top 30) oluşturuldu

✅ TÜM GÖRSELLEŞTİRMELER TAMAMLANDI!
Toplam: 11 grafik
```

**Süre:** ~8-10 saniye

---

### Adım 5D: Outlier Analizi
```powershell
python scripts/outlier_analysis.py
```

**Ne yapar?**
- ✅ Unexpected leaders bulur (Yüksek AI, Düşük GDP)
- ✅ Underperformers bulur (Düşük AI, Yüksek GDP)
- ✅ Detaylı ülke profilleri oluşturur
- ✅ Percentile rankings hesaplar

**Çıktı:**
```
🔍 OUTLIER ANALİZİ

📈 UNEXPECTED LEADERS (Yüksek AI, Düşük GDP):

1. Ghana 🇬🇭
   AI Interest: 51.2% (97th percentile!)
   GDP: $2,391 (8th percentile)
   → Digital leapfrogging örneği!

2. Belarus 🇧🇾
   AI Interest: 48.3% (94th percentile)
   GDP: $8,318 (24th percentile)
   → STEM education güçlü

3. Tanzania 🇹🇿
   AI Interest: 46.2% (93rd percentile)
   GDP: $1,187 (4th percentile)
   → Mobile-first adoption

📉 UNDERPERFORMERS (Düşük AI, Yüksek GDP):

1. Slovenia 🇸🇮
   AI Interest: 25.1% (5th percentile)
   GDP: $34,074 (81st percentile)

2. Finland 🇫🇮
   AI Interest: 30.4% (19th percentile)
   GDP: $53,983 (93rd percentile)
```

**Grafik Çıktıları:**
- `visualizations/outliers_scatter.html`
- `visualizations/outliers_radar.html`
- `visualizations/outliers_unexpected_leaders.html`

**Rapor Çıktısı:**
- `docs/outlier_analysis_report.md`

**Süre:** ~5 saniye

---

## 🗂️ ÇIKTI DOSYALARI

### 📁 data/raw/ (Ham Veri)
```
trends_chatgpt.csv          ← Google Trends verisi (103 ülke)
world_bank_indicators.csv   ← Ekonomik göstergeler (102 ülke)
```

### 📁 data/processed/ (Temizlenmiş Veri)
```
ai_adoption_combined.csv    ← Trends + World Bank birleştirilmiş
ai_adoption_cleaned.csv     ← Temizlenmiş, 15 sütun, 103 ülke ✅ ANA VERİ
ai_adoption_clustered.csv   ← Cluster bilgisi eklenmiş
```

### 📁 visualizations/ (Grafikler)
```
TEMEL (3 grafik):
├── world_map_ai_adoption.html     ← Dünya haritası
├── scatter_gdp_vs_ai.html         ← GDP vs AI scatter
└── top_20_countries.html          ← Top 20 bar chart

İSTATİSTİK (3 grafik):
├── correlation_heatmap.html
├── feature_importance.html
└── regression_actual_vs_predicted.html

CLUSTERING (4 grafik):
├── clustering_elbow.html
├── clustering_gdp_vs_ai.html
├── clustering_3d.html
└── clustering_parallel.html

GELİŞMİŞ (11 grafik):
├── boxplot_economic_category.html
├── boxplot_regions.html
├── violin_continents.html
├── regional_ai_interest.html
├── regional_radar.html
├── regional_sunburst.html
├── regional_bubble.html
├── distribution_histogram.html
├── distribution_by_category.html
├── treemap_population.html
└── heatmap_top30.html

OUTLIER (3 grafik):
├── outliers_scatter.html
├── outliers_radar.html
└── outliers_unexpected_leaders.html

TOPLAM: 24 grafik
```

### 📁 docs/ (Dokümantasyon)
```
COMPREHENSIVE_REPORT.md          ← Ana rapor (580 satır)
outlier_analysis_report.md       ← Outlier analizi
improvement_suggestions.md       ← İyileştirme önerileri
PROJECT_COMPLETION.md            ← Proje özeti
LEARNING_GUIDE.md                ← Kod öğrenme rehberi (bu dosya)
```

---

## 🎬 TAM PROJE ÇALIŞTIRMA (Sıfırdan)

### Senaryo 1: Sadece Grafikler Görmek İstiyorum
```powershell
# 1. Veriyi temizle
python scripts/data_cleaning.py

# 2. Basit grafikleri oluştur
python scripts/visualization.py

# 3. Haritayı aç
Start-Process "visualizations\world_map_ai_adoption.html"

# 4. Scatter plot'u aç
Start-Process "visualizations\scatter_gdp_vs_ai.html"
```
**Süre:** ~10 saniye

---

### Senaryo 2: Tam Analiz (Her Şey)
```powershell
# 1. Veri temizle
python scripts/data_cleaning.py

# 2. Basit grafikler
python scripts/visualization.py

# 3. İstatistiksel analiz
python scripts/statistical_analysis.py

# 4. Machine learning
python scripts/clustering_analysis.py

# 5. Gelişmiş grafikler
python scripts/advanced_visualizations.py

# 6. Outlier analizi
python scripts/outlier_analysis.py

# 7. Tüm grafikleri göster
Start-Process "visualizations"
```
**Süre:** ~30-40 saniye

---

### Senaryo 3: Yeni Veri Topla (Sıfırdan)
```powershell
# 1. Yeni veri topla (⚠️ 5-10 dakika sürer!)
python scripts/data_collection.py

# 2. Veriyi temizle
python scripts/data_cleaning.py

# 3. Grafikleri oluştur
python scripts/visualization.py

# 4. Haritayı aç
Start-Process "visualizations\world_map_ai_adoption.html"
```
**Süre:** ~5-10 dakika

---

## 🔧 SORUN GİDERME

### ❌ Hata 1: "ModuleNotFoundError: No module named 'pandas'"
**Çözüm:**
```powershell
# Sanal ortamı aktif et
.\venv\Scripts\Activate.ps1

# Paketleri yükle
pip install -r requirements.txt
```

---

### ❌ Hata 2: "FileNotFoundError: data/raw/trends_chatgpt.csv"
**Çözüm:**
```powershell
# Önce veri toplama scriptini çalıştır
python scripts/data_collection.py
```

---

### ❌ Hata 3: "KeyError: 'country_code_iso3'"
**Çözüm:**
```powershell
# Veri temizleme scriptini çalıştır
python scripts/data_cleaning.py
```

---

### ❌ Hata 4: PowerShell Execution Policy
**Çözüm:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ Hata 5: API Timeout (Google Trends/World Bank)
**Çözüm:**
```python
# data_collection.py içinde timeout süresini artır
response = requests.get(url, timeout=30)  # 10 → 30
```

---

## 📊 ÇIKTILARI ANLAMA

### Dünya Haritası (world_map_ai_adoption.html)
```
🟪 Koyu mor = Yüksek AI ilgisi (Japan, Israel, Ghana)
🟦 Açık mavi = Orta AI ilgisi (Turkey, Mexico)
🟨 Sarı = Düşük AI ilgisi (Venezuela, Slovenia)
```

**Mouse ile tıkla:**
- Ülke adı
- AI Interest yüzdesi
- GDP per capita
- Internet users %

---

### Scatter Plot (scatter_gdp_vs_ai.html)
```
X ekseni: GDP per Capita (ekonomik gelişmişlik)
Y ekseni: AI Interest (ChatGPT ilgisi)
Nokta boyutu: Population (nüfus)
Renk: Economic Category
```

**Ne gösterir?**
- Sağ üst köşe: Zengin + Yüksek AI (USA, Germany)
- Sol üst köşe: Fakir + Yüksek AI (Ghana, Tanzania) ← SÜRPRİZ!
- Sağ alt köşe: Zengin + Düşük AI (Finland, Slovenia)

---

### Correlation Heatmap
```
🟥 Kırmızı = Pozitif korelasyon (+1'e yakın)
🟦 Mavi = Negatif korelasyon (-1'e yakın)
⬜ Beyaz = Korelasyon yok (0'a yakın)
```

**Bizim sonuçlar:**
- GDP ↔ AI: +0.199 (zayıf pozitif)
- Internet ↔ AI: +0.216 (zayıf pozitif)
- Education ↔ AI: -0.041 (ilişki yok)

---

### Clustering (clustering_gdp_vs_ai.html)
```
🔴 Kırmızı = Cluster 0 "Early Adopters"
🔵 Mavi = Cluster 1 "Fast Followers"
🟢 Yeşil = Cluster 2 "Moderate Users"
🟡 Sarı = Cluster 3 "Laggards"
```

**Her cluster'ın özellikleri:**
- Cluster 0: Orta GDP, orta AI (gelişmekte olan)
- Cluster 1: Yüksek GDP, yüksek AI (gelişmiş)
- Cluster 2: Düşük AI, orta GDP (Çin, Hindistan)
- Cluster 3: Düşük GDP, orta AI (Afrika, Asya)

---

## 🎯 ÖNEMLİ SONUÇLAR (Projenin Hikayesi)

### 🏆 Top 5 Ülke (AI Adoption)
```
1. 🇯🇵 Japan - 53.9%
2. 🇮🇱 Israel - 53.3%
3. 🇬🇭 Ghana - 51.2%    ← SÜRPRİZ!
4. 🇸🇬 Singapore - 49.7%
5. 🇧🇾 Belarus - 48.3%   ← SÜRPRİZ!
```

### 🌍 Kıtalara Göre Ortalama
```
🥇 Africa: 41.2%     ← EN YÜKSEK!
🥈 Asia: 39.8%
🥉 Europe: 35.5%
4️⃣ Americas: 33.5%
5️⃣ Oceania: 37.7%
```

### 💡 Ana Bulgu
**"Ekonomik gelişmişlik AI benimsenmesini belirlemez!"**

- GDP ile AI ilgisi: sadece r = +0.199
- Fakir ülkeler (Ghana, Tanzania) AI'da lider
- Zengin ülkeler (Finland, Slovenia) geride

**Neden?**
1. 📱 Mobile-first infrastructure
2. 👨‍🎓 Young population (18-35 yaş)
3. 🚀 Digital leapfrogging effect
4. 📚 STEM education investment
5. 💼 Economic necessity (girişimcilik)

---

## 🎓 SONRAKİ ADIMLAR

### 1. Grafiklerle Oyna
```powershell
# Farklı bir harita rengi dene
# visualization.py içinde:
color_continuous_scale='Reds'  # Viridis yerine
```

### 2. Farklı Bir Analiz Ekle
```python
# Örnek: İnternet kullanımı ile AI ilgisi arasındaki korelasyon
from scipy.stats import pearsonr
corr, p = pearsonr(df['internet_users_pct'], df['avg_interest'])
```

### 3. Yeni Bir Ülke Ekle
```python
# data_collection.py içinde:
self.countries = {
    'US': 'United States',
    'TR': 'Turkey',
    # ... yeni ülke ekle
    'XX': 'New Country'
}
```

### 4. Dashboard Oluştur
```bash
# Streamlit ile interaktif dashboard
pip install streamlit
streamlit run dashboard.py
```

### 5. Rapor Hazırla
```markdown
# docs/COMPREHENSIVE_REPORT.md dosyasını oku
# Poster/Sunum için kullan:
- Top 10 ülke tablosu
- Kıta bazında karşılaştırma
- Ghana deep dive
- İstatistiksel test sonuçları
```

---

## 📞 YARDIM

### Hangi dosya ne iş yapıyor karıştıysa:
```
VERİ TOPLAMA     → data_collection.py
VERİ TEMİZLEME   → data_cleaning.py
BASIT GRAFİKLER  → visualization.py
İSTATİSTİK       → statistical_analysis.py
MACHINE LEARNING → clustering_analysis.py
GELİŞMİŞ GRAFİK  → advanced_visualizations.py
OUTLIER          → outlier_analysis.py
```

### Hangi grafik nerede?
```
TÜM GRAFİKLER    → visualizations/ klasörü
ANA VERİ         → data/processed/ai_adoption_cleaned.csv
RAPORLAR         → docs/ klasörü
```

### Script çalışmıyor?
```
1. Sanal ortam aktif mi?     → .\venv\Scripts\Activate.ps1
2. Paketler yüklü mü?        → pip install -r requirements.txt
3. Veri var mı?              → data/raw/ klasörüne bak
4. Veri temizlendi mi?       → python scripts/data_cleaning.py
```

---

## ✅ HANGİ SCRIPTI NE ZAMAN ÇALIŞTIRMALI?

### 🟢 HER ZAMAN ÇALIŞTIR (Zorunlu)
1. ✅ `data_cleaning.py` - Veriyi hazırla
2. ✅ `visualization.py` - Basit grafikleri oluştur

### 🟡 İSTERSEN ÇALIŞTIR (Opsiyonel)
3. 🔶 `statistical_analysis.py` - İstatistiksel testler
4. 🔶 `clustering_analysis.py` - Machine learning
5. 🔶 `advanced_visualizations.py` - Gelişmiş grafikler
6. 🔶 `outlier_analysis.py` - Outlier analizi

### 🔴 SADECE YENİ VERİ TOPLARKEN (Nadiren)
7. ⛔ `data_collection.py` - API'den yeni veri çek (5-10 dakika)

---

## 🎉 ÖZET: 3 ADIMDA BAŞLA

```powershell
# 1. Veriyi hazırla
python scripts/data_cleaning.py

# 2. Grafikler oluştur
python scripts/visualization.py

# 3. Haritayı aç
Start-Process "visualizations\world_map_ai_adoption.html"
```

**🎯 Bu kadar! Artık projen çalışıyor.**

**💬 Soru varsa sor!**

---

## 📚 DAHA FAZLA BİLGİ

- **Kod açıklamaları:** `docs/LEARNING_GUIDE.md`
- **Proje özeti:** `docs/PROJECT_COMPLETION.md`
- **Ana rapor:** `docs/COMPREHENSIVE_REPORT.md`
- **Outlier analizi:** `docs/outlier_analysis_report.md`
