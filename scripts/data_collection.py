"""
AI Adoption Data Collection Script

Collects data about AI tool adoption from Google Trends and World Bank APIs.

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
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.ai_tools = [
            'ChatGPT',
            'Midjourney',
            'GitHub Copilot',
            'DALL-E',
            'Stable Diffusion'
        ]
        
        self.countries = {
            'US': 'United States', 'CA': 'Canada', 'MX': 'Mexico',
            'BR': 'Brazil', 'AR': 'Argentina', 'CO': 'Colombia', 'CL': 'Chile',
            'PE': 'Peru', 'VE': 'Venezuela', 'EC': 'Ecuador', 'UY': 'Uruguay',
            'GB': 'United Kingdom', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy',
            'ES': 'Spain', 'NL': 'Netherlands', 'BE': 'Belgium', 'CH': 'Switzerland',
            'AT': 'Austria', 'IE': 'Ireland', 'PT': 'Portugal', 'GR': 'Greece',
            'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland',
            'IS': 'Iceland',
            'PL': 'Poland', 'CZ': 'Czech Republic', 'HU': 'Hungary', 'RO': 'Romania',
            'BG': 'Bulgaria', 'SK': 'Slovakia', 'HR': 'Croatia', 'SI': 'Slovenia',
            'RS': 'Serbia', 'LT': 'Lithuania', 'LV': 'Latvia', 'EE': 'Estonia',
            'UA': 'Ukraine', 'BY': 'Belarus',
            'CN': 'China', 'JP': 'Japan', 'KR': 'South Korea', 'TW': 'Taiwan',
            'HK': 'Hong Kong', 'MN': 'Mongolia',
            'ID': 'Indonesia', 'TH': 'Thailand', 'VN': 'Vietnam', 'PH': 'Philippines',
            'MY': 'Malaysia', 'SG': 'Singapore', 'MM': 'Myanmar', 'KH': 'Cambodia',
            'LA': 'Laos',
            'IN': 'India', 'PK': 'Pakistan', 'BD': 'Bangladesh', 'LK': 'Sri Lanka',
            'NP': 'Nepal', 'AF': 'Afghanistan',
            'TR': 'Turkey', 'SA': 'Saudi Arabia', 'AE': 'United Arab Emirates',
            'IL': 'Israel', 'IR': 'Iran', 'IQ': 'Iraq', 'EG': 'Egypt', 
            'JO': 'Jordan', 'LB': 'Lebanon', 'KW': 'Kuwait', 'QA': 'Qatar',
            'OM': 'Oman', 'BH': 'Bahrain', 'YE': 'Yemen',
            'MA': 'Morocco', 'DZ': 'Algeria', 'TN': 'Tunisia', 'LY': 'Libya',
            'NG': 'Nigeria', 'GH': 'Ghana', 'CI': 'Ivory Coast', 'SN': 'Senegal',
            'KE': 'Kenya', 'ET': 'Ethiopia', 'TZ': 'Tanzania', 'UG': 'Uganda',
            'ZA': 'South Africa', 'ZW': 'Zimbabwe', 'BW': 'Botswana', 'NA': 'Namibia',
            'AU': 'Australia', 'NZ': 'New Zealand', 'FJ': 'Fiji', 'PG': 'Papua New Guinea',
            'RU': 'Russia', 'KZ': 'Kazakhstan', 'UZ': 'Uzbekistan', 'GE': 'Georgia',
            'AZ': 'Azerbaijan', 'AM': 'Armenia'
        }
        
    def collect_google_trends(self, tool_name, timeframe='2023-01-01 2025-12-31'):
        
        print(f"\nCollecting Google Trends data for {tool_name}...")
        
        all_data = []
        
        for country_code, country_name in self.countries.items():
            try:
                self.pytrends.build_payload(
                    [tool_name],
                    cat=0,
                    timeframe=timeframe,
                    geo=country_code,
                    gprop=''
                )
                
                interest_over_time = self.pytrends.interest_over_time()
                
                if not interest_over_time.empty:
                    avg_interest = interest_over_time[tool_name].mean()
                    max_interest = interest_over_time[tool_name].max()
                    last_interest = interest_over_time[tool_name].iloc[-1]
                    
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
                    
                    print(f"  {country_name}: Avg={avg_interest:.1f}, Max={max_interest}")
                else:
                    print(f"  {country_name}: No data available")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"  {country_name}: Error - {str(e)}")
                continue
        
        df = pd.DataFrame(all_data)
        
        output_file = self.data_dir / f"trends_{tool_name.lower().replace(' ', '_')}.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSaved {len(df)} records to {output_file}")
        
        return df
    
    def collect_world_bank_data(self):
        
        print("\nCollecting World Bank data...")
        
        indicators = {
            'NY.GDP.PCAP.CD': 'gdp_per_capita',
            'SE.TER.ENRR': 'tertiary_education',
            'IT.NET.USER.ZS': 'internet_users_pct',
            'SP.POP.TOTL': 'population'
        }
        
        all_data = []
        
        for country_code in self.countries.keys():
            country_data = {'country_code': country_code}
            
            for indicator_code, indicator_name in indicators.items():
                try:
                    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
                    params = {
                        'format': 'json',
                        'date': '2022:2024',
                        'per_page': 100
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if len(data) > 1 and data[1]:
                            values = [item['value'] for item in data[1] if item['value'] is not None]
                            if values:
                                country_data[indicator_name] = values[0]
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  {country_code} - {indicator_name}: {str(e)}")
                    continue
            
            if len(country_data) > 1:
                all_data.append(country_data)
                print(f"  {country_code}: {len(country_data)-1} indicators collected")
        
        df = pd.DataFrame(all_data)
        
        output_file = self.data_dir / "world_bank_indicators.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSaved data for {len(df)} countries to {output_file}")
        
        return df
    
    def collect_github_data(self):
        
        print("\nCollecting GitHub data...")
        
        base_url = "https://api.github.com/search/repositories"
        
        all_data = []
        
        for country_code, country_name in self.countries.items():
            try:
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
                    
                    print(f"  {country_name}: {data.get('total_count', 0)} repos")
                elif response.status_code == 403:
                    print(f"  Rate limit reached, waiting...")
                    time.sleep(60)
                    continue
                
                time.sleep(2)
                
            except Exception as e:
                print(f"  {country_name}: {str(e)}")
                continue
        
        df = pd.DataFrame(all_data)
        
        output_file = self.data_dir / "github_ai_activity.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSaved data for {len(df)} countries to {output_file}")
        
        return df
    
    def collect_all_data(self):
        
        print("="*60)
        print("AI ADOPTION DATA COLLECTION")
        print("="*60)
        
        start_time = time.time()
        
        print("\nStep 1/2: Google Trends Data")
        print("-"*60)
        chatgpt_trends = self.collect_google_trends('ChatGPT')
        
        print("\nStep 2/2: World Bank Economic Data")
        print("-"*60)
        wb_data = self.collect_world_bank_data()
        
        print("\nSkipping GitHub API (location data unreliable)")
        
        print("\nMerging datasets...")
        
        combined = chatgpt_trends[['country_code', 'country_name', 'avg_interest', 
                                   'max_interest', 'current_interest', 'trend_direction']]
        
        if not wb_data.empty:
            combined = combined.merge(wb_data, on='country_code', how='left')
        
        output_file = Path("data/processed/ai_adoption_combined.csv")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_file, index=False)
        
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("DATA COLLECTION COMPLETE")
        print("="*60)
        print(f"Total countries: {len(combined)}")
        print(f"Total columns: {len(combined.columns)}")
        print(f"Time elapsed: {elapsed/60:.1f} minutes")
        print(f"Output file: {output_file}")
        print("="*60)
        
        print("\nData Summary:")
        print(combined.describe())
        
        return combined


def main():
    
    collector = AIAdoptionCollector()
    df = collector.collect_all_data()
    
    print("\nTop Countries by ChatGPT Interest:")
    print(df.nlargest(10, 'avg_interest')[['country_name', 'avg_interest', 'gdp_per_capita']])


if __name__ == "__main__":
    main()
