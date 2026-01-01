"""
Data Cleaning Script - AI Adoption Project

Cleans and prepares collected data for analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ISO_CODE_MAP = {
    'US': 'USA', 'CA': 'CAN', 'MX': 'MEX',
    'BR': 'BRA', 'AR': 'ARG', 'CO': 'COL', 'CL': 'CHL', 'PE': 'PER', 
    'VE': 'VEN', 'EC': 'ECU', 'UY': 'URY',
    'GB': 'GBR', 'DE': 'DEU', 'FR': 'FRA', 'IT': 'ITA', 'ES': 'ESP', 
    'NL': 'NLD', 'BE': 'BEL', 'CH': 'CHE', 'AT': 'AUT', 'IE': 'IRL', 
    'PT': 'PRT', 'GR': 'GRC',
    'SE': 'SWE', 'NO': 'NOR', 'DK': 'DNK', 'FI': 'FIN', 'IS': 'ISL',
    'PL': 'POL', 'CZ': 'CZE', 'HU': 'HUN', 'RO': 'ROU', 'BG': 'BGR', 
    'SK': 'SVK', 'HR': 'HRV', 'SI': 'SVN', 'RS': 'SRB', 'LT': 'LTU', 
    'LV': 'LVA', 'EE': 'EST', 'UA': 'UKR', 'BY': 'BLR',
    'CN': 'CHN', 'JP': 'JPN', 'KR': 'KOR', 'TW': 'TWN', 'HK': 'HKG', 'MN': 'MNG',
    'ID': 'IDN', 'TH': 'THA', 'VN': 'VNM', 'PH': 'PHL', 'MY': 'MYS', 
    'SG': 'SGP', 'MM': 'MMR', 'KH': 'KHM', 'LA': 'LAO',
    'IN': 'IND', 'PK': 'PAK', 'BD': 'BGD', 'LK': 'LKA', 'NP': 'NPL', 'AF': 'AFG',
    'TR': 'TUR', 'SA': 'SAU', 'AE': 'ARE', 'IL': 'ISR', 'IR': 'IRN', 
    'IQ': 'IRQ', 'EG': 'EGY', 'JO': 'JOR', 'LB': 'LBN', 'KW': 'KWT', 
    'QA': 'QAT', 'OM': 'OMN', 'BH': 'BHR', 'YE': 'YEM',
    'MA': 'MAR', 'DZ': 'DZA', 'TN': 'TUN', 'LY': 'LBY', 'NG': 'NGA', 
    'GH': 'GHA', 'CI': 'CIV', 'SN': 'SEN', 'KE': 'KEN', 'ET': 'ETH', 
    'TZ': 'TZA', 'UG': 'UGA', 'ZA': 'ZAF', 'ZW': 'ZWE', 'BW': 'BWA', 'NA': 'NAM',
    'AU': 'AUS', 'NZ': 'NZL', 'FJ': 'FJI', 'PG': 'PNG',
    'RU': 'RUS', 'KZ': 'KAZ', 'UZ': 'UZB', 'GE': 'GEO', 'AZ': 'AZE', 'AM': 'ARM'
}

REGION_MAP = {
    'US': 'North America', 'CA': 'North America', 'MX': 'North America',
    'BR': 'South America', 'AR': 'South America', 'CO': 'South America', 
    'CL': 'South America', 'PE': 'South America', 'VE': 'South America', 
    'EC': 'South America', 'UY': 'South America',
    'GB': 'Western Europe', 'DE': 'Western Europe', 'FR': 'Western Europe', 
    'IT': 'Western Europe', 'ES': 'Western Europe', 'NL': 'Western Europe', 
    'BE': 'Western Europe', 'CH': 'Western Europe', 'AT': 'Western Europe', 
    'IE': 'Western Europe', 'PT': 'Western Europe', 'GR': 'Western Europe',
    'SE': 'Northern Europe', 'NO': 'Northern Europe', 'DK': 'Northern Europe', 
    'FI': 'Northern Europe', 'IS': 'Northern Europe',
    'PL': 'Eastern Europe', 'CZ': 'Eastern Europe', 'HU': 'Eastern Europe', 
    'RO': 'Eastern Europe', 'BG': 'Eastern Europe', 'SK': 'Eastern Europe', 
    'HR': 'Eastern Europe', 'SI': 'Eastern Europe', 'RS': 'Eastern Europe', 
    'LT': 'Eastern Europe', 'LV': 'Eastern Europe', 'EE': 'Eastern Europe', 
    'UA': 'Eastern Europe', 'BY': 'Eastern Europe',
    'CN': 'East Asia', 'JP': 'East Asia', 'KR': 'East Asia', 
    'TW': 'East Asia', 'HK': 'East Asia', 'MN': 'East Asia',
    'ID': 'Southeast Asia', 'TH': 'Southeast Asia', 'VN': 'Southeast Asia', 
    'PH': 'Southeast Asia', 'MY': 'Southeast Asia', 'SG': 'Southeast Asia', 
    'MM': 'Southeast Asia', 'KH': 'Southeast Asia', 'LA': 'Southeast Asia',
    'IN': 'South Asia', 'PK': 'South Asia', 'BD': 'South Asia', 
    'LK': 'South Asia', 'NP': 'South Asia', 'AF': 'South Asia',
    'TR': 'Middle East', 'SA': 'Middle East', 'AE': 'Middle East', 
    'IL': 'Middle East', 'IR': 'Middle East', 'IQ': 'Middle East', 
    'EG': 'Middle East', 'JO': 'Middle East', 'LB': 'Middle East', 
    'KW': 'Middle East', 'QA': 'Middle East', 'OM': 'Middle East', 
    'BH': 'Middle East', 'YE': 'Middle East',
    'MA': 'North Africa', 'DZ': 'North Africa', 'TN': 'North Africa', 
    'LY': 'North Africa',
    'NG': 'West Africa', 'GH': 'West Africa', 'CI': 'West Africa', 'SN': 'West Africa',
    'KE': 'East Africa', 'ET': 'East Africa', 'TZ': 'East Africa', 'UG': 'East Africa',
    'ZA': 'Southern Africa', 'ZW': 'Southern Africa', 'BW': 'Southern Africa', 
    'NA': 'Southern Africa',
    'AU': 'Oceania', 'NZ': 'Oceania', 'FJ': 'Oceania', 'PG': 'Oceania',
    'RU': 'Russia & Central Asia', 'KZ': 'Russia & Central Asia', 
    'UZ': 'Russia & Central Asia', 'GE': 'Russia & Central Asia', 
    'AZ': 'Russia & Central Asia', 'AM': 'Russia & Central Asia'
}

CONTINENT_MAP = {
    'US': 'Americas', 'CA': 'Americas', 'MX': 'Americas',
    'BR': 'Americas', 'AR': 'Americas', 'CO': 'Americas', 'CL': 'Americas', 
    'PE': 'Americas', 'VE': 'Americas', 'EC': 'Americas', 'UY': 'Americas',
    'GB': 'Europe', 'DE': 'Europe', 'FR': 'Europe', 'IT': 'Europe', 
    'ES': 'Europe', 'NL': 'Europe', 'BE': 'Europe', 'CH': 'Europe', 
    'AT': 'Europe', 'IE': 'Europe', 'PT': 'Europe', 'GR': 'Europe',
    'SE': 'Europe', 'NO': 'Europe', 'DK': 'Europe', 'FI': 'Europe', 'IS': 'Europe',
    'PL': 'Europe', 'CZ': 'Europe', 'HU': 'Europe', 'RO': 'Europe', 
    'BG': 'Europe', 'SK': 'Europe', 'HR': 'Europe', 'SI': 'Europe', 
    'RS': 'Europe', 'LT': 'Europe', 'LV': 'Europe', 'EE': 'Europe', 
    'UA': 'Europe', 'BY': 'Europe', 'RU': 'Europe',
    'CN': 'Asia', 'JP': 'Asia', 'KR': 'Asia', 'TW': 'Asia', 'HK': 'Asia', 'MN': 'Asia',
    'ID': 'Asia', 'TH': 'Asia', 'VN': 'Asia', 'PH': 'Asia', 'MY': 'Asia', 
    'SG': 'Asia', 'MM': 'Asia', 'KH': 'Asia', 'LA': 'Asia',
    'IN': 'Asia', 'PK': 'Asia', 'BD': 'Asia', 'LK': 'Asia', 'NP': 'Asia', 'AF': 'Asia',
    'TR': 'Asia', 'SA': 'Asia', 'AE': 'Asia', 'IL': 'Asia', 'IR': 'Asia', 
    'IQ': 'Asia', 'EG': 'Africa', 'JO': 'Asia', 'LB': 'Asia', 'KW': 'Asia', 
    'QA': 'Asia', 'OM': 'Asia', 'BH': 'Asia', 'YE': 'Asia',
    'MA': 'Africa', 'DZ': 'Africa', 'TN': 'Africa', 'LY': 'Africa',
    'NG': 'Africa', 'GH': 'Africa', 'CI': 'Africa', 'SN': 'Africa',
    'KE': 'Africa', 'ET': 'Africa', 'TZ': 'Africa', 'UG': 'Africa',
    'ZA': 'Africa', 'ZW': 'Africa', 'BW': 'Africa', 'NA': 'Africa',
    'AU': 'Oceania', 'NZ': 'Oceania', 'FJ': 'Oceania', 'PG': 'Oceania',
    'KZ': 'Asia', 'UZ': 'Asia', 'GE': 'Asia', 'AZ': 'Asia', 'AM': 'Asia'
}

def load_data():
    
    data_path = Path("data/processed/ai_adoption_combined.csv")
    
    if not data_path.exists():
        print("Error: Data file not found. Please run data_collection.py first.")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records")
    
    df['country_code_iso3'] = df['country_code'].map(ISO_CODE_MAP)
    df['region'] = df['country_code'].map(REGION_MAP)
    df['continent'] = df['country_code'].map(CONTINENT_MAP)
    
    return df

def clean_data(df):
    
    print("\nCleaning data...")
    
    print("\nMissing values:")
    print(df.isnull().sum())
    
    if 'gdp_per_capita' in df.columns:
        median_gdp = df['gdp_per_capita'].median()
        df['gdp_per_capita'].fillna(median_gdp, inplace=True)
        print(f"\nGDP missing values filled with median: {median_gdp:.0f}")
    
    df = df[df['avg_interest'] > 0]
    print(f"\nCleaning complete: {len(df)} records remaining")
    
    return df

def create_features(df):
    
    print("\nCreating new features...")
    
    if 'gdp_per_capita' in df.columns:
        df['economic_category'] = pd.cut(
            df['gdp_per_capita'],
            bins=[0, 10000, 30000, float('inf')],
            labels=['Developing', 'Emerging', 'Developed']
        )
        print("Economic category created")
    
    if 'avg_interest' in df.columns and 'internet_users_pct' in df.columns:
        df['ai_adoption_score'] = (
            df['avg_interest'] / df['avg_interest'].max() * 0.7 +
            df['internet_users_pct'] / 100 * 0.3
        ) * 100
        print("AI Adoption Score calculated")
    
    return df

def save_cleaned_data(df):
    
    output_path = Path("data/processed/ai_adoption_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved: {output_path}")
    return output_path

def main():
    
    df = load_data()
    if df is None:
        return
    
    df = clean_data(df)
    df = create_features(df)
    save_cleaned_data(df)
    
    print("\n" + "="*60)
    print("DATA CLEANING COMPLETE")
    print("="*60)
    print(f"\nFinal dataset: {len(df)} countries, {len(df.columns)} columns")
    print("\nColumns:", list(df.columns))

if __name__ == "__main__":
    main()
