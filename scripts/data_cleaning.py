"""
Data Cleaning Script - AI Adoption Project
==========================================

Toplanan verileri temizler ve analiz için hazırlar.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ISO 2-letter to 3-letter country code mapping
ISO_CODE_MAP = {
    'US': 'USA', 'GB': 'GBR', 'DE': 'DEU', 'FR': 'FRA', 'JP': 'JPN',
    'CN': 'CHN', 'IN': 'IND', 'BR': 'BRA', 'CA': 'CAN', 'AU': 'AUS',
    'KR': 'KOR', 'IT': 'ITA', 'ES': 'ESP', 'MX': 'MEX', 'ID': 'IDN',
    'NL': 'NLD', 'TR': 'TUR', 'SA': 'SAU', 'CH': 'CHE', 'PL': 'POL',
    'SE': 'SWE', 'BE': 'BEL', 'AR': 'ARG', 'NO': 'NOR', 'AT': 'AUT',
    'IL': 'ISR', 'IE': 'IRL', 'DK': 'DNK', 'SG': 'SGP', 'MY': 'MYS'
}

def load_data():
    """Tüm veri dosyalarını yükle"""
    data_path = Path("data/processed/ai_adoption_combined.csv")
    
    if not data_path.exists():
        print("❌ Veri dosyası bulunamadı! Önce data_collection.py çalıştırın.")
        return None
    
    df = pd.read_csv(data_path)
    print(f"✅ {len(df)} kayıt yüklendi")
    
    # ISO-3 kodlarına çevir
    df['country_code_iso3'] = df['country_code'].map(ISO_CODE_MAP)
    
    return df

def clean_data(df):
    """Veri temizleme işlemleri"""
    print("\n🧹 Veri temizleme başlıyor...")
    
    # Kayıp değerleri kontrol et
    print("\n📊 Kayıp değerler:")
    print(df.isnull().sum())
    
    # GDP kayıp değerleri için median ile doldur
    if 'gdp_per_capita' in df.columns:
        median_gdp = df['gdp_per_capita'].median()
        df['gdp_per_capita'].fillna(median_gdp, inplace=True)
        print(f"\n💰 GDP kayıp değerleri median ({median_gdp:.0f}) ile dolduruldu")
    
    # AI interest 0 olanları temizle
    df = df[df['avg_interest'] > 0]
    print(f"\n✅ Temizleme tamamlandı: {len(df)} kayıt kaldı")
    
    return df

def create_features(df):
    """Yeni özellikler oluştur"""
    print("\n🔧 Yeni özellikler oluşturuluyor...")
    
    # Ekonomik kategoriler
    if 'gdp_per_capita' in df.columns:
        df['economic_category'] = pd.cut(
            df['gdp_per_capita'],
            bins=[0, 10000, 30000, float('inf')],
            labels=['Developing', 'Emerging', 'Developed']
        )
        print("✅ Ekonomik kategori oluşturuldu")
    
    # AI Adoption Score (normalize edilmiş)
    if 'avg_interest' in df.columns and 'internet_users_pct' in df.columns:
        df['ai_adoption_score'] = (
            df['avg_interest'] / df['avg_interest'].max() * 0.7 +
            df['internet_users_pct'] / 100 * 0.3
        ) * 100
        print("✅ AI Adoption Score hesaplandı")
    
    return df

def save_cleaned_data(df):
    """Temizlenmiş veriyi kaydet"""
    output_path = Path("data/processed/ai_adoption_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"\n💾 Temizlenmiş veri kaydedildi: {output_path}")
    return output_path

def main():
    """Ana işlem"""
    df = load_data()
    if df is None:
        return
    
    df = clean_data(df)
    df = create_features(df)
    save_cleaned_data(df)
    
    print("\n" + "="*60)
    print("✅ VERİ TEMİZLEME TAMAMLANDI!")
    print("="*60)
    print(f"\nFinal dataset: {len(df)} ülke, {len(df.columns)} sütun")
    print("\nSütunlar:", list(df.columns))

if __name__ == "__main__":
    main()
