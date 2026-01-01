# 🎓 AI Adoption Divide - Kod Öğrenme Rehberi

## 📚 İçindekiler
1. [Proje Yapısı](#proje-yapısı)
2. [Adım 1: Veri Toplama](#adım-1-veri-toplama)
3. [Adım 2: Veri Temizleme](#adım-2-veri-temizleme)
4. [Adım 3: Görselleştirme](#adım-3-görselleştirme)
5. [Adım 4: İstatistiksel Analiz](#adım-4-i̇statistiksel-analiz)
6. [Adım 5: Machine Learning](#adım-5-machine-learning)
7. [Adım 6: İleri Görselleştirmeler](#adım-6-i̇leri-görselleştirmeler)
8. [Adım 7: Outlier Analizi](#adım-7-outlier-analizi)
9. [Önemli Kavramlar](#önemli-kavramlar)

---

## Proje Yapısı

```
DATASCIENCE/
│
├── data/
│   ├── raw/                      # Ham veri (API'den gelen)
│   │   ├── trends_chatgpt.csv    # Google Trends verisi
│   │   └── world_bank_indicators.csv  # Ekonomik göstergeler
│   │
│   └── processed/                # Temizlenmiş veri
│       ├── ai_adoption_combined.csv   # Birleştirilmiş
│       ├── ai_adoption_cleaned.csv    # Temizlenmiş
│       └── ai_adoption_clustered.csv  # Cluster eklenmiş
│
├── scripts/                      # Python kodları
│   ├── data_collection.py        # 1. Veri toplama
│   ├── data_cleaning.py          # 2. Veri temizleme
│   ├── visualization.py          # 3. Temel görselleştirme
│   ├── statistical_analysis.py   # 4. İstatistiksel testler
│   ├── clustering_analysis.py    # 5. Machine learning
│   ├── advanced_visualizations.py # 6. İleri görselleştirmeler
│   └── outlier_analysis.py       # 7. Outlier analizi
│
├── visualizations/               # Çıkan grafikler (.html)
├── docs/                         # Dokümantasyon
└── requirements.txt              # Python paketleri
```

---

# Adım 1: Veri Toplama

## 📁 Dosya: `scripts/data_collection.py`

### Ne İşe Yarar?
Bu script **103 ülkeden** ChatGPT ile ilgili Google Trends verisini ve World Bank'ten ekonomik göstergeleri toplar.

### Temel Kavramlar

#### 1. Class (Sınıf) Nedir?
```python
class AIAdoptionCollector:
    """Veri toplama sınıfı"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.data_dir = Path("data/raw")
```

**Açıklama:**
- `class` = Bir şablondur (blueprint). İçinde değişkenler ve fonksiyonlar barındırır.
- `__init__` = Constructor. Sınıf ilk oluşturulduğunda çalışır.
- `self` = Sınıfın kendisini temsil eder (Java/C++'daki `this` gibi).
- `self.pytrends` = Sınıfın içinde kullanabileceğin bir değişken.

**Örnek Kullanım:**
```python
collector = AIAdoptionCollector()  # __init__ çalışır
collector.collect_google_trends()  # Method çağrısı
```

#### 2. Google Trends API
```python
from pytrends.request import TrendReq

self.pytrends = TrendReq(hl='en-US', tz=360)

# ChatGPT arama trendini al
self.pytrends.build_payload(['ChatGPT'], 
                            geo=country_code, 
                            timeframe='today 12-m')
data = self.pytrends.interest_over_time()
```

**Ne Yapıyor?**
- Google'da "ChatGPT" kelimesini arayan insanların **ülke bazında yüzdelik oranını** getiriyor
- `timeframe='today 12-m'` = Son 12 aydaki trendi
- `geo='US'` = Amerika'daki aramaları filtrele
- Sonuç: 0-100 arası bir sayı (100 = en yüksek ilgi)

**Örnek Çıktı:**
```
Country: Japan
avg_interest: 53.9  (Japonya'da %53.9 ChatGPT ilgisi)
max_interest: 65    (En yüksek 65'e çıkmış)
```

#### 3. World Bank API
```python
def fetch_world_bank_indicator(self, indicator, countries):
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
    params = {
        'format': 'json',
        'per_page': 300,
        'date': '2020:2023'
    }
    response = requests.get(url, params=params, timeout=10)
```

**Ekonomik Göstergeler:**
- `NY.GDP.PCAP.CD` = GDP per capita (Kişi başı milli gelir)
- `SE.TER.ENRR` = Tertiary education (Üniversite eğitimi %)
- `IT.NET.USER.ZS` = Internet users (İnternet kullanıcıları %)
- `SP.POP.TOTL` = Population (Toplam nüfus)

**Örnek Çıktı:**
```json
{
  "country": "Turkey",
  "gdp_per_capita": 10672.5,
  "tertiary_education": 45.2,
  "internet_users_pct": 82.0,
  "population": 84339067
}
```

#### 4. Hata Yönetimi (Try-Except)
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 404, 500 hataları için exception fırlat
    data = response.json()
    return data
    
except requests.Timeout:
    print(f"⏳ Timeout: {country}")
    return None
    
except Exception as e:
    print(f"❌ Hata: {e}")
    return None
```

**Neden Gerekli?**
- API yanıt vermeyebilir (timeout)
- İnternet kesintisi olabilir
- Ülke verisi olmayabilir
- Program çökmez, hata mesajı verir ve devam eder

#### 5. Time Delay (API Rate Limiting)
```python
import time

for country in self.countries:
    data = self.collect_for_country(country)
    time.sleep(0.5)  # 0.5 saniye bekle
```

**Neden?**
- Google/World Bank API'leri **rate limiting** yapar
- Çok hızlı istek atarsan banlanırsın
- Her istekten sonra 0.5 saniye beklemek güvenlidir

---

# Adım 2: Veri Temizleme

## 📁 Dosya: `scripts/data_cleaning.py`

### Ne İşe Yarar?
Ham verideki eksiklikleri düzeltir, yeni sütunlar ekler, analiz için hazırlar.

### Temel Kavramlar

#### 1. Dictionary (Sözlük) Mapping
```python
ISO_CODE_MAP = {
    'US': 'USA',
    'GB': 'GBR',
    'TR': 'TUR',
    'DE': 'DEU'
}

# Kullanımı
df['country_code_iso3'] = df['country_code'].map(ISO_CODE_MAP)
```

**Açıklama:**
- `dict` = Key-value (anahtar-değer) çiftleri
- `map()` = Her satıra sözlükteki karşılığını ekler
- ISO-2 ('US') → ISO-3 ('USA') dönüşümü için kullanıyoruz

**Neden ISO-3?**
- Plotly haritaları ISO-3 formatında ülke kodu istiyor
- 'US' yerine 'USA' yazmalısın yoksa haritada gözükmez

#### 2. Region/Continent Mapping
```python
REGION_MAP = {
    'US': 'North America',
    'TR': 'Middle East',
    'GH': 'West Africa',
    'JP': 'East Asia'
}

CONTINENT_MAP = {
    'US': 'Americas',
    'TR': 'Asia',
    'GH': 'Africa',
    'JP': 'Asia'
}
```

**Neden Gerekli?**
- Ülke bazında değil, **bölge bazında** analiz yapmak için
- Örnek: "Afrika'da ortalama AI ilgisi ne?" sorusuna cevap vermek için

#### 3. Missing Data (Eksik Veri) Yönetimi
```python
# NaN'leri kontrol et
print(df.isnull().sum())

# Medyan ile doldur
df['gdp_per_capita'].fillna(df['gdp_per_capita'].median(), inplace=True)

# Satırı sil
df.dropna(subset=['country_name'], inplace=True)
```

**fillna() vs dropna():**
- `fillna()` = Eksik değeri doldur (ortalama, medyan, 0, vb.)
- `dropna()` = Eksik değeri olan satırı komple sil

**Hangi Durumda Ne Yapılır?**
- Kritik sütun (country_name) → Sil (`dropna`)
- Nümerik sütun (GDP) → Doldur (`fillna`)

#### 4. Feature Engineering (Özellik Mühendisliği)
```python
def create_economic_category(gdp):
    """GDP'ye göre kategori oluştur"""
    if pd.isna(gdp):
        return 'Unknown'
    elif gdp < 5000:
        return 'Developing'
    elif gdp < 15000:
        return 'Emerging'
    elif gdp < 30000:
        return 'Advanced Emerging'
    else:
        return 'Developed'

# Yeni sütun oluştur
df['economic_category'] = df['gdp_per_capita'].apply(create_economic_category)
```

**Açıklama:**
- `apply()` = Her satıra fonksiyonu uygula
- GDP sayısını kategoriye çeviriyor
- Kategorik verilerle analiz yapmak daha kolay

**Örnek:**
```
Turkey: GDP $10,672 → "Emerging"
Ghana: GDP $2,391 → "Developing"
USA: GDP $76,398 → "Developed"
```

#### 5. AI Adoption Score (Composite Score)
```python
def calculate_ai_adoption_score(row):
    """AI benimseme skoru hesapla"""
    score = 0
    
    # Google Trends ilgisi (0-100)
    score += row['avg_interest'] * 0.5  # Ağırlık: 50%
    
    # İnternet kullanıcı oranı (0-100)
    if not pd.isna(row['internet_users_pct']):
        score += row['internet_users_pct'] * 0.3  # Ağırlık: 30%
    
    # Eğitim seviyesi (0-100)
    if not pd.isna(row['tertiary_education']):
        score += row['tertiary_education'] * 0.2  # Ağırlık: 20%
    
    return score

df['ai_adoption_score'] = df.apply(calculate_ai_adoption_score, axis=1)
```

**Composite Score Mantığı:**
- 3 faktörü birleştirip tek bir skor oluştur
- Her faktöre ağırlık ver (toplam %100)
- Sonuç: 0-100 arası tek bir skor

---

# Adım 3: Görselleştirme

## 📁 Dosya: `scripts/visualization.py`

### Ne İşe Yarar?
Verileri **interaktif HTML grafikleri** olarak görselleştirir.

### Temel Kavramlar

#### 1. Plotly Express (px)
```python
import plotly.express as px

fig = px.choropleth(
    df,
    locations='country_code_iso3',   # ISO-3 ülke kodu
    locationmode='ISO-3',             # Harita modu
    color='avg_interest',             # Renklendirme
    hover_name='country_name',        # Mouse hover'da göster
    title='AI Adoption by Country'
)

fig.write_html('world_map.html')  # HTML olarak kaydet
```

**Choropleth Map Nedir?**
- Dünya haritası üzerinde ülkeleri renklendirir
- Koyu renk = Yüksek değer
- Açık renk = Düşük değer

**Örnek:**
- Japonya → Koyu mor (53.9% AI ilgisi)
- Venezuela → Açık sarı (10.5% AI ilgisi)

#### 2. Scatter Plot (Dağılım Grafiği)
```python
fig = px.scatter(
    df,
    x='gdp_per_capita',       # X ekseni: GDP
    y='avg_interest',         # Y ekseni: AI ilgisi
    size='population',        # Nokta boyutu: Nüfus
    color='economic_category', # Renk: Ekonomik kategori
    hover_name='country_name'
)
```

**Ne Gösterir?**
- X ekseni: Ekonomik gelişmişlik (GDP)
- Y ekseni: AI ilgisi
- Nokta boyutu: Ülkenin nüfusu
- Renk: Hangi ekonomik kategoride

**İlişki Okuma:**
- Eğer noktalar sağa yukarı gidiyorsa → Pozitif korelasyon
- Eğer dağınıksa → Zayıf ilişki (bizim durumumuz!)

#### 3. Bar Chart (Çubuk Grafik)
```python
# Top 20 ülke
top_20 = df.nlargest(20, 'avg_interest')

fig = px.bar(
    top_20,
    x='avg_interest',
    y='country_name',
    orientation='h',  # Horizontal (yatay)
    title='Top 20 Countries - AI Adoption'
)
```

**Kullanım Alanları:**
- Karşılaştırma (comparison)
- Sıralama (ranking)
- Top N listesi

---

# Adım 4: İstatistiksel Analiz

## 📁 Dosya: `scripts/statistical_analysis.py`

### Ne İşe Yarar?
İstatistiksel testlerle hipotezleri sınar, ilişkileri sayılarla kanıtlar.

### Temel Kavramlar

#### 1. Correlation (Korelasyon)
```python
from scipy.stats import pearsonr

# GDP ile AI ilgisi arasındaki korelasyon
corr, p_value = pearsonr(df['gdp_per_capita'], df['avg_interest'])

print(f"Korelasyon: {corr:.3f}")
print(f"P-value: {p_value:.4f}")
```

**Korelasyon Nedir?**
- **r = +1**: Mükemmel pozitif ilişki (biri artarsa diğeri de artar)
- **r = 0**: İlişki yok
- **r = -1**: Mükemmel negatif ilişki (biri artarsa diğeri azalır)

**Bizim Sonucumuz:**
```
r = +0.199
p = 0.044
```
- **Yorum:** Çok zayıf pozitif ilişki var ama istatistiksel olarak anlamlı (p < 0.05)

#### 2. ANOVA Test
```python
from scipy.stats import f_oneway

# Ekonomik kategorilere göre AI ilgisi farklı mı?
developing = df[df['economic_category'] == 'Developing']['avg_interest']
emerging = df[df['economic_category'] == 'Emerging']['avg_interest']
developed = df[df['economic_category'] == 'Developed']['avg_interest']

f_stat, p_value = f_oneway(developing, emerging, developed)
```

**ANOVA Nedir?**
- **3+ grup** arasında ortalama farkı test eder
- **H0 (Null Hypothesis):** Tüm gruplar eşit
- **H1 (Alternative):** En az bir grup farklı

**Bizim Sonucumuz:**
```
F = 5.67
p = 0.0046
```
- **Yorum:** Gruplar arasında **anlamlı fark var** (p < 0.05)
- Developing vs Developed farklı değil ama Emerging farklı!

#### 3. Multiple Regression (Çoklu Regresyon)
```python
from sklearn.linear_model import LinearRegression

# Bağımsız değişkenler (X)
X = df[['gdp_per_capita', 'tertiary_education', 'internet_users_pct']]

# Bağımlı değişken (y)
y = df['avg_interest']

# Model eğit
model = LinearRegression()
model.fit(X, y)

# R² skoru
r2 = model.score(X, y)
print(f"R² = {r2:.3f}")  # 0.257
```

**R² Nedir?**
- Model varyansın ne kadarını açıklıyor?
- **R² = 0.257** → %25.7 açıklıyor
- Geri kalan %74.3 başka faktörler (dilbilgisi, kültür, politika...)

**Katsayılar:**
```
GDP: +3.62     (GDP artarsa AI ilgisi artar)
Education: -0.05  (Üniversite eğitimi etkisiz)
Internet: +0.18   (İnternet kullanımı artarsa AI ilgisi artar)
```

---

# Adım 5: Machine Learning

## 📁 Dosya: `scripts/clustering_analysis.py`

### Ne İşe Yarar?
Ülkeleri **benzerliklerine göre gruplara** ayırır (unsupervised learning).

### Temel Kavramlar

#### 1. K-Means Clustering
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Özellikleri normalize et
scaler = StandardScaler()
X = df[['avg_interest', 'gdp_per_capita', 'internet_users_pct']]
X_scaled = scaler.fit_transform(X)

# K-means modeli
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)
```

**K-Means Nedir?**
- Unsupervised learning (etiket yok)
- Ülkeleri **k adet gruba** ayırır
- Her grup içindeki ülkeler birbirine benzer

**Bizim Clusterlarımız:**
```
Cluster 0: "Early Adopters" (n=24)
  - Orta AI ilgisi, orta GDP
  - Örnek: Meksika, Polonya, Kolombiya

Cluster 1: "Fast Followers" (n=20)
  - Yüksek AI ilgisi, yüksek GDP
  - Örnek: ABD, Almanya, İngiltere

Cluster 2: "Moderate Users" (n=2)
  - Düşük AI ilgisi, orta GDP
  - Örnek: Çin, Hindistan (nüfus etkisi)

Cluster 3: "Laggards" (n=7)
  - Orta AI ilgisi, düşük GDP
  - Örnek: Endonezya, Pakistan
```

#### 2. StandardScaler (Normalizasyon)
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**Neden Gerekli?**
- GDP: 1,000 - 80,000 aralığında
- Internet: 20 - 100 aralığında
- AI Interest: 10 - 60 aralığında

Aynı ölçeğe getirmeliyiz yoksa GDP baskın çıkar!

**Sonuç:**
```
Ortalama = 0
Std sapma = 1
```

#### 3. Elbow Method (Optimal k Bulma)
```python
inertias = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Grafik çiz
plt.plot(range(2, 11), inertias)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
```

**Elbow Method Nedir?**
- Her k değeri için **inertia** (grup içi mesafe toplamı) hesapla
- Grafikte "dirsek" nerede kırılıyorsa o optimal k

**Bizim Sonucumuz:**
- Optimal k = 5 ama yorumlanabilirlik için k=4 seçtik

#### 4. Silhouette Score (Kümeleme Kalitesi)
```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X_scaled, df['cluster'])
print(f"Silhouette: {score:.3f}")  # 0.324
```

**Silhouette Nedir?**
- Kümeleme kalitesini ölçer
- **-1 ile +1 arası**
  - +1: Mükemmel kümeleme
  - 0: Kümeler iç içe
  - -1: Yanlış kümeleme

**0.324 = Kabul edilebilir**

---

# Adım 6: İleri Görselleştirmeler

## 📁 Dosya: `scripts/advanced_visualizations.py`

### Ne İşe Yarar?
Daha karmaşık ve estetik grafikler oluşturur.

### Temel Kavramlar

#### 1. Box Plot (Kutu Grafiği)
```python
fig = px.box(
    df,
    x='economic_category',
    y='avg_interest',
    color='economic_category',
    title='AI Interest by Economic Category'
)
```

**Box Plot Nedir?**
```
      ┌─────┐
      │     │  ← Q3 (75th percentile)
  ────┼─────┤  ← Median (50th)
      │     │  ← Q1 (25th percentile)
      └─────┘
   o          ← Outlier (aykırı değer)
```

**Ne Gösterir?**
- Dağılımın şeklini
- Medyan'ı
- Outlier'ları

#### 2. Violin Plot (Keman Grafiği)
```python
fig = px.violin(
    df,
    x='continent',
    y='avg_interest',
    box=True,  # İçine box plot ekle
    points='all'  # Tüm noktaları göster
)
```

**Violin Plot Nedir?**
- Box plot + Density plot (yoğunluk)
- Dağılımın **şeklini** gösterir
- Hangi değerde daha çok veri var?

#### 3. Sunburst Chart (Güneş Patlaması)
```python
fig = px.sunburst(
    df,
    path=['continent', 'region', 'country_name'],  # Hiyerarşi
    values='population',  # Büyüklük
    color='avg_interest'  # Renk
)
```

**Sunburst Nedir?**
- Hiyerarşik veriler için
- İç halka: Kıta
- Orta halka: Bölge
- Dış halka: Ülke

#### 4. Treemap (Ağaç Haritası)
```python
fig = px.treemap(
    df,
    path=['continent', 'country_name'],
    values='population',  # Kutu boyutu
    color='avg_interest'  # Renk
)
```

**Treemap Nedir?**
- Nested rectangles (iç içe dikdörtgenler)
- Büyük kutu = Yüksek nüfus
- Koyu renk = Yüksek AI ilgisi

#### 5. Radar Chart (Örümcek Ağı)
```python
categories = ['AI Interest', 'GDP', 'Education', 'Internet']
values = [country['avg_interest'], 
          country['gdp_per_capita'],
          country['tertiary_education'],
          country['internet_users_pct']]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name=country_name
))
```

**Radar Chart Nedir?**
- Çok boyutlu karşılaştırma
- Her eksen = Bir özellik
- Ülkeyi 4 farklı özellikte değerlendir

---

# Adım 7: Outlier Analizi

## 📁 Dosya: `scripts/outlier_analysis.py`

### Ne İşe Yarar?
**Sürpriz ülkeleri** bulur ve detaylı inceler.

### Temel Kavramlar

#### 1. Percentile Rank (Yüzdelik Dilim)
```python
df['ai_percentile'] = df['avg_interest'].rank(pct=True) * 100
df['gdp_percentile'] = df['gdp_per_capita'].rank(pct=True) * 100
```

**Percentile Nedir?**
- Bir değerin ne kadar üstte olduğunu gösterir
- **95th percentile** = En üstteki %5'te
- **50th percentile** = Medyan

**Örnek:**
```
Ghana:
  AI Interest: 51.2% → 97th percentile (çok yüksek!)
  GDP: $2,391 → 8th percentile (çok düşük!)
  
Sonuç: OUTLIER! (Fakir ama AI'da lider)
```

#### 2. Z-Score (Standart Sapma)
```python
from scipy.stats import zscore

df['ai_zscore'] = zscore(df['avg_interest'])

# |z| > 2 ise outlier
outliers = df[abs(df['ai_zscore']) > 2]
```

**Z-Score Nedir?**
- Ortama göre kaç standart sapma uzakta?
- **z = 0**: Ortalamada
- **z = +2**: Ortalamadan +2 std sapma yukarıda
- **z = -2**: Ortalamadan -2 std sapma aşağıda

**Kural:**
- |z| > 2 → Outlier (aykırı değer)

#### 3. Unexpected Leaders (Sürpriz Liderler)
```python
def find_unexpected_leaders(df):
    """Yüksek AI, düşük GDP"""
    return df[(df['ai_percentile'] > 70) & (df['gdp_percentile'] < 30)]
```

**Mantık:**
- AI ilgisi TOP %30'da
- GDP ise BOTTOM %30'da
- Bu kombinasyon sürpriz!

**Bulgular:**
```
Ghana: 97th AI, 8th GDP → Digital leapfrogging!
Tanzania: 93rd AI, 5th GDP → Mobile-first adoption
Belarus: 94th AI, 24th GDP → STEM education strong
```

---

# Önemli Kavramlar

## 1. API (Application Programming Interface)
**Tanım:** Bir servisin verilerini programatik olarak çekmene izin verir.

**Örnek:**
```python
# Google Trends API
response = pytrends.interest_over_time()

# World Bank API
response = requests.get('https://api.worldbank.org/v2/country/TR/indicator/NY.GDP.PCAP.CD')
```

**Avantajları:**
- Manuel kopyala-yapıştır yerine otomatik
- Güncel veri
- Reproducible (tekrarlanabilir)

---

## 2. DataFrame (Pandas)
**Tanım:** Excel gibi tablo yapısı.

```python
import pandas as pd

df = pd.DataFrame({
    'country': ['USA', 'Turkey', 'Ghana'],
    'gdp': [76398, 10672, 2391],
    'ai_interest': [41.2, 37.5, 51.2]
})

# Filtreleme
high_ai = df[df['ai_interest'] > 40]

# Sıralama
sorted_df = df.sort_values('ai_interest', ascending=False)

# Yeni sütun
df['gdp_category'] = df['gdp'].apply(lambda x: 'High' if x > 20000 else 'Low')
```

**Temel Operasyonlar:**
- `df.head()` = İlk 5 satır
- `df.info()` = Sütun bilgileri
- `df.describe()` = İstatistikler
- `df.groupby()` = Gruplama
- `df.merge()` = Birleştirme

---

## 3. Lambda Function (Anonim Fonksiyon)
```python
# Normal fonksiyon
def double(x):
    return x * 2

# Lambda versiyonu
double = lambda x: x * 2

# Kullanım
df['doubled'] = df['value'].apply(lambda x: x * 2)
```

**Ne Zaman Kullanılır?**
- Tek satırlık basit fonksiyonlar
- `apply()`, `map()`, `filter()` ile

---

## 4. P-Value (İstatistiksel Anlamlılık)
**Tanım:** Sonucun rastlantısal olma olasılığı.

**Yorum:**
- **p < 0.05**: İstatistiksel olarak anlamlı (kabul et!)
- **p > 0.05**: Anlamlı değil (rastlantısal olabilir)

**Örnek:**
```
Korelasyon: r = 0.199, p = 0.044

Yorum: GDP ile AI ilgisi arasında zayıf ama 
       istatistiksel olarak anlamlı ilişki var.
```

---

## 5. Null Hypothesis (H0) vs Alternative (H1)
**H0:** İlişki/fark yok
**H1:** İlişki/fark var

**Örnek:**
```
H0: Developing ve Developed ülkelerde AI ilgisi eşit
H1: Farklı

ANOVA testi:
p = 0.0046 < 0.05 → H0 reddedildi → Fark var!
```

---

# 🎯 Proje Çalıştırma Sırası

## Adım 1: Kurulum
```bash
# Sanal ortam oluştur
python -m venv venv

# Aktif et
venv\Scripts\activate

# Paketleri yükle
pip install -r requirements.txt
```

## Adım 2: Veri Toplama
```bash
python scripts/data_collection.py
```
**Çıktı:** `data/raw/trends_chatgpt.csv`, `data/raw/world_bank_indicators.csv`

## Adım 3: Veri Temizleme
```bash
python scripts/data_cleaning.py
```
**Çıktı:** `data/processed/ai_adoption_cleaned.csv` (15 sütun, 103 ülke)

## Adım 4: Temel Görselleştirme
```bash
python scripts/visualization.py
```
**Çıktı:** `visualizations/world_map_ai_adoption.html`, `scatter_gdp_vs_ai.html`

## Adım 5: İstatistiksel Analiz
```bash
python scripts/statistical_analysis.py
```
**Çıktı:** 
- Correlation heatmap
- Feature importance
- Regression plot

## Adım 6: Clustering
```bash
python scripts/clustering_analysis.py
```
**Çıktı:**
- Elbow plot
- 2D/3D cluster scatters
- Parallel coordinates

## Adım 7: İleri Görselleştirmeler
```bash
python scripts/advanced_visualizations.py
```
**Çıktı:** 11 grafik (box, violin, sunburst, treemap, radar, vb.)

## Adım 8: Outlier Analizi
```bash
python scripts/outlier_analysis.py
```
**Çıktı:** 
- Outlier scatter
- Radar charts
- Unexpected leaders bar chart
- Markdown rapor

---

# 📖 Önerilen Öğrenme Yolu

## Seviye 1: Başlangıç
1. ✅ Python temelleri (değişken, döngü, fonksiyon)
2. ✅ Pandas DataFrame (okuma, filtreleme, sıralama)
3. ✅ Plotly ile basit grafik (scatter, bar, choropleth)

## Seviye 2: Orta
1. ✅ API kullanımı (requests, JSON parsing)
2. ✅ Veri temizleme (fillna, dropna, map)
3. ✅ İstatistiksel testler (correlation, ANOVA, regression)

## Seviye 3: İleri
1. ✅ Machine Learning (K-means, StandardScaler)
2. ✅ Complex visualizations (radar, sunburst, treemap)
3. ✅ Feature engineering (composite scores, percentiles)

---

# 🎓 Pratik Yapma Önerileri

## 1. Veri Toplama Pratiği
```python
# Farklı bir anahtar kelime dene
self.pytrends.build_payload(['Midjourney'], geo='US')

# Farklı bir World Bank göstergesi ekle
# Örnek: CO2 emissions (EN.ATM.CO2E.PC)
```

## 2. Veri Temizleme Pratiği
```python
# Farklı bir ekonomik kategori sistemi yap
# Örnek: GDP'ye göre 3 kategori yerine 5 kategori

# Yeni bir composite score oluştur
# Örnek: "Tech Readiness Score" = Internet + Education + GDP
```

## 3. Görselleştirme Pratiği
```python
# Farklı color scales dene
color_continuous_scale='Reds'  # Viridis yerine

# Heatmap yerine 3D surface plot dene
fig = px.scatter_3d(df, x='gdp', y='education', z='ai_interest')
```

## 4. İstatistik Pratiği
```python
# İnternet kullanımı ile AI ilgisi arasındaki korelasyon
corr, p = pearsonr(df['internet_users_pct'], df['avg_interest'])

# Kıtalara göre ANOVA
f, p = f_oneway(*[group['avg_interest'].values 
                  for name, group in df.groupby('continent')])
```

## 5. Machine Learning Pratiği
```python
# Farklı k değerleri dene (k=3, k=5, k=6)
kmeans = KMeans(n_clusters=5)

# DBSCAN clustering dene (density-based)
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
```

---

# ❓ Sıkça Sorulan Sorular

## S: Neden ISO-3 kullanıyoruz?
**C:** Plotly haritaları ISO-3 formatında ülke kodu bekliyor. 'US' yerine 'USA' yazmalısın.

## S: fillna() vs dropna() hangisi?
**C:** 
- Kritik sütun (country_name) → `dropna()`
- Nümerik sütun (GDP) → `fillna(median)`

## S: API rate limiting nedir?
**C:** API'ler çok hızlı istek atarsan banlar. `time.sleep(0.5)` ile ara ver.

## S: P-value < 0.05 ne demek?
**C:** İstatistiksel olarak anlamlı demek. Sonuç rastlantısal değil, gerçek bir ilişki var.

## S: K-means'te k nasıl seçilir?
**C:** Elbow method ile optimal k'yı bul. Grafikteki "dirsek" noktası.

## S: Composite score neden gerekli?
**C:** Birden fazla faktörü tek bir skorda birleştirmek için. Karşılaştırma kolaylaşır.

## S: Outlier nedir?
**C:** Aykırı değer. Genel eğilimden çok farklı olan veri noktası.

---

# 🚀 İleri Seviye Konular

## 1. Time Series Analysis
- 12 aylık trend verisi topla
- Momentum analizi (yükseliş/düşüş)
- ARIMA forecasting

## 2. Sentiment Analysis
- Twitter/Reddit'ten AI ile ilgili yorumları çek
- NLP ile pozitif/negatif duygu analizi
- Ülke bazında sentiment skoru

## 3. Causal Inference
- Does GDP **cause** AI adoption?
- Regression Discontinuity Design
- Instrumental Variables

## 4. Interactive Dashboard
- Streamlit ile web app yap
- Kullanıcı ülke seçsin, grafikler güncellensin
- Filtreleme, download özelliği

## 5. Deep Learning
- Neural Network ile prediction
- LSTM ile time series forecasting
- Autoencoders ile anomaly detection

---

# 📚 Kaynaklar

## Pandas
- https://pandas.pydata.org/docs/
- https://www.kaggle.com/learn/pandas

## Plotly
- https://plotly.com/python/
- https://plotly.com/python/plotly-express/

## Statistics
- https://www.statisticshowto.com/
- https://www.scipy.org/

## Machine Learning
- https://scikit-learn.org/stable/
- https://www.kaggle.com/learn/intro-to-machine-learning

## APIs
- https://trends.google.com/trends/
- https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

---

# ✅ Proje Tamamlama Checklist

- [x] Veri toplama scripti çalışıyor
- [x] 103 ülke verisi toplandı
- [x] Veri temizleme tamamlandı
- [x] ISO-3 mapping doğru
- [x] Region/Continent mapping eklendi
- [x] Temel görselleştirmeler (harita, scatter, bar)
- [x] İstatistiksel testler (correlation, ANOVA, regression)
- [x] K-means clustering (4 cluster)
- [x] İleri görselleştirmeler (11 grafik)
- [x] Outlier analizi (Ghana, Belarus, Tanzania)
- [x] Comprehensive report yazıldı
- [x] README profesyonel formatta
- [x] GitHub repo oluşturuldu

---

**🎉 Tebrikler! Artık bu projenin her satırını anlıyorsun.**

**💡 Sorular:** 
1. Hangi bölümü daha detaylı anlatmamı ister misin?
2. Pratik yapmak için hangi kodu değiştirmek istersin?
3. Yeni bir analiz eklemek ister misin?

