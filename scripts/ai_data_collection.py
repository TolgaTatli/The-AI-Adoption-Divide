"""
AI Adoption Data Collection Script
===================================

Bu script Google Trends, World Bank ve GitHub API'lerinden
yapay zeka araçlarının benimsenmesi hakkında veri toplar.

Author: SENG Data Science Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from pytrends.request import TrendReq
import requests
import time
from pathlib import Path
import json
from datetime import datetime, timedelta

class AIAdoptionCollector:
    """
    AI araçlarının küresel benimsenmesi hakkında veri toplar.
    """
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Analiz edilecek AI araçları
        self.ai_tools = [
            'ChatGPT',
            'Midjourney',
            'GitHub Copilot',
            'DALL-E',
            'Stable Diffusion'
        ]
        
        # Analiz edilecek ülkeler (ISO 2-letter codes)
        self.countries = {
            'US': 'United States',
            'GB': 'United Kingdom', 
            'DE': 'Germany',
            'FR': 'France',
            'JP': 'Japan',
            'CN': 'China',
            'IN': 'India',
            'BR': 'Brazil',
            'CA': 'Canada',
            'AU': 'Australia',
            'KR': 'South Korea',
            'IT': 'Italy',
            'ES': 'Spain',
            'MX': 'Mexico',
            'ID': 'Indonesia',
            'NL': 'Netherlands',
            'TR': 'Turkey',
            'SA': 'Saudi Arabia',
            'CH': 'Switzerland',
            'PL': 'Poland',
            'SE': 'Sweden',
            'BE': 'Belgium',
            'AR': 'Argentina',
            'NO': 'Norway',
            'AT': 'Austria',
            'IL': 'Israel',
            'IE': 'Ireland',
            'DK': 'Denmark',
            'SG': 'Singapore',
            'MY': 'Malaysia'
        }
        
    def collect_google_trends(self, tool_name, timeframe='2023-01-01 2025-12-31'):
        """
        Belirli bir AI aracı için Google Trends verisi toplar.
        
        Args:
            tool_name (str): AI aracının adı
            timeframe (str): Zaman aralığı
            
        Returns:
            pd.DataFrame: Ülke bazında trend verileri
        """
        print(f"\n🔍 {tool_name} için Google Trends verisi topluyorum...")
        
        all_data = []
        
        for country_code, country_name in self.countries.items():
            try:
                # Google Trends API çağrısı
                self.pytrends.build_payload(
                    [tool_name],
                    cat=0,
                    timeframe=timeframe,
                    geo=country_code,
                    gprop=''
                )
                
                # Interest over time
                interest_over_time = self.pytrends.interest_over_time()
                
                if not interest_over_time.empty:
                    # Ortalama, maksimum ve son değerleri hesapla
                    avg_interest = interest_over_time[tool_name].mean()
                    max_interest = interest_over_time[tool_name].max()
                    last_interest = interest_over_time[tool_name].iloc[-1]
                    
                    # Trend (yükseliş/düşüş) hesapla
                    first_half = interest_over_time[tool_name].iloc[:len(interest_over_time)//2].mean()
                    second_half = interest_over_time[tool_name].iloc[len(interest_over_time)//2:].mean()
                    trend_direction = 'rising' if second_half > first_half else 'falling'
                    trend_magnitude = abs(second_half - first_half) / (first_half + 1) * 100
                    
                    all_data.append({
                        'country_code': country_code,
                        'country_name': country_name,
                        'tool': tool_name,
                        'avg_interest': round(avg_interest, 2),
                        'max_interest': max_interest,
                        'current_interest': last_interest,
                        'trend_direction': trend_direction,
                        'trend_magnitude': round(trend_magnitude, 2),
                        'data_points': len(interest_over_time)
                    })
                    
                    print(f"  ✅ {country_name}: Avg={avg_interest:.1f}, Max={max_interest}")
                else:
                    print(f"  ⚠️  {country_name}: Veri bulunamadı")
                
                # API rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ {country_name}: {str(e)}")
                continue
        
        df = pd.DataFrame(all_data)
        
        # Dosyaya kaydet
        output_file = self.data_dir / f"trends_{tool_name.lower().replace(' ', '_')}.csv"
        df.to_csv(output_file, index=False)
        print(f"\n💾 {len(df)} kayıt kaydedildi: {output_file}")
        
        return df
    
    def collect_world_bank_data(self):
        """
        World Bank API'den ekonomik ve sosyal göstergeleri çeker.
        
        Returns:
            pd.DataFrame: Ülke bazında ekonomik veriler
        """
        print("\n🌍 World Bank verilerini topluyorum...")
        
        # World Bank API indicators
        indicators = {
            'NY.GDP.PCAP.CD': 'gdp_per_capita',  # GDP per capita
            'SE.TER.ENRR': 'tertiary_education',  # Tertiary education enrollment
            'IT.NET.USER.ZS': 'internet_users_pct',  # Internet users %
            'SP.POP.TOTL': 'population'  # Population
        }
        
        all_data = []
        
        for country_code in self.countries.keys():
            country_data = {'country_code': country_code}
            
            for indicator_code, indicator_name in indicators.items():
                try:
                    # World Bank API request
                    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
                    params = {
                        'format': 'json',
                        'date': '2022:2024',  # Son 3 yıl
                        'per_page': 100
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if len(data) > 1 and data[1]:
                            # En son veriyi al
                            values = [item['value'] for item in data[1] if item['value'] is not None]
                            if values:
                                country_data[indicator_name] = values[0]
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  ⚠️  {country_code} - {indicator_name}: {str(e)}")
                    continue
            
            if len(country_data) > 1:  # Sadece country_code'dan fazlası varsa
                all_data.append(country_data)
                print(f"  ✅ {country_code}: {len(country_data)-1} gösterge")
        
        df = pd.DataFrame(all_data)
        
        # Dosyaya kaydet
        output_file = self.data_dir / "world_bank_indicators.csv"
        df.to_csv(output_file, index=False)
        print(f"\n💾 {len(df)} ülke kaydedildi: {output_file}")
        
        return df
    
    def collect_github_data(self):
        """
        GitHub API'den AI/ML repository istatistikleri toplar.
        
        Returns:
            pd.DataFrame: Ülke bazında GitHub aktivitesi
        """
        print("\n💻 GitHub verilerini topluyorum...")
        
        # GitHub API (authentication olmadan 60 request/hour limit var)
        base_url = "https://api.github.com/search/repositories"
        
        ai_topics = ['artificial-intelligence', 'machine-learning', 'deep-learning', 'chatgpt']
        
        all_data = []
        
        for country_code, country_name in self.countries.items():
            try:
                # Ülke bazında AI repository arama
                query = f"topic:artificial-intelligence OR topic:machine-learning location:{country_name}"
                params = {
                    'q': query,
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 100
                }
                
                response = requests.get(base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    all_data.append({
                        'country_code': country_code,
                        'country_name': country_name,
                        'ai_repos_count': data.get('total_count', 0),
                        'top_repo_stars': data['items'][0]['stargazers_count'] if data['items'] else 0
                    })
                    
                    print(f"  ✅ {country_name}: {data.get('total_count', 0)} repo")
                elif response.status_code == 403:
                    print(f"  ⚠️  Rate limit aşıldı, bekliyorum...")
                    time.sleep(60)
                    continue
                else:
                    print(f"  ⚠️  {country_name}: HTTP {response.status_code}")
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ {country_name}: {str(e)}")
                continue
        
        df = pd.DataFrame(all_data)
        
        # Dosyaya kaydet
        output_file = self.data_dir / "github_ai_activity.csv"
        df.to_csv(output_file, index=False)
        print(f"\n💾 {len(df)} ülke kaydedildi: {output_file}")
        
        return df
    
    def collect_all_data(self):
        """
        Tüm veri kaynaklarından veri toplar ve birleştirir.
        """
        print("=" * 60)
        print("🚀 AI Adoption Data Collection Başlıyor")
        print("=" * 60)
        
        start_time = time.time()
        
        # 1. Google Trends - Sadece ChatGPT için başlangıç
        print("\n📊 ADIM 1/3: Google Trends Verileri")
        print("-" * 60)
        chatgpt_trends = self.collect_google_trends('ChatGPT')
        
        # İsterseniz diğer araçlar için de:
        # for tool in self.ai_tools[1:]:
        #     self.collect_google_trends(tool)
        
        # 2. World Bank Data
        print("\n📊 ADIM 2/3: World Bank Ekonomik Verileri")
        print("-" * 60)
        wb_data = self.collect_world_bank_data()
        
        # 3. GitHub Data (Opsiyonel - rate limit var)
        print("\n📊 ADIM 3/3: GitHub AI Aktivitesi")
        print("-" * 60)
        print("⚠️  Not: GitHub API rate limit nedeniyle yavaş olabilir")
        github_data = self.collect_github_data()
        
        # Tüm verileri birleştir
        print("\n🔗 Verileri birleştiriyorum...")
        
        # ChatGPT trends ile başla
        combined = chatgpt_trends[['country_code', 'country_name', 'avg_interest', 
                                   'max_interest', 'current_interest', 'trend_direction']]
        
        # World Bank verilerini ekle
        if not wb_data.empty:
            combined = combined.merge(wb_data, on='country_code', how='left')
        
        # GitHub verilerini ekle
        if not github_data.empty:
            combined = combined.merge(
                github_data[['country_code', 'ai_repos_count']], 
                on='country_code', 
                how='left'
            )
        
        # Final dataset kaydet
        output_file = self.data_dir.parent / "processed" / "ai_adoption_combined.csv"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_file, index=False)
        
        # Özet
        elapsed = time.time() - start_time
        print("\n" + "=" * 60)
        print("✅ VERİ TOPLAMA TAMAMLANDI!")
        print("=" * 60)
        print(f"📁 Toplam ülke: {len(combined)}")
        print(f"📊 Toplam sütun: {len(combined.columns)}")
        print(f"⏱️  Süre: {elapsed/60:.1f} dakika")
        print(f"💾 Ana dosya: {output_file}")
        print("=" * 60)
        
        # Veri özeti göster
        print("\n📈 Veri Özeti:")
        print(combined.describe())
        
        return combined


def main():
    """Ana çalıştırma fonksiyonu"""
    collector = AIAdoptionCollector()
    df = collector.collect_all_data()
    
    # Hızlı görselleştirme
    print("\n🌍 En Yüksek ChatGPT İlgisi Gösteren Ülkeler:")
    print(df.nlargest(10, 'avg_interest')[['country_name', 'avg_interest', 'gdp_per_capita']])
    
    print("\n💰 En Yüksek GDP'li Ülkelerin AI İlgisi:")
    top_gdp = df.nlargest(10, 'gdp_per_capita')[['country_name', 'gdp_per_capita', 'avg_interest']]
    print(top_gdp)


if __name__ == "__main__":
    main()
