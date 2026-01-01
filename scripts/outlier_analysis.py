"""
Outlier Analysis - AI Adoption Project

Detailed analysis of surprising/interesting countries.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

def load_data():
    
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"Loaded {len(df)} countries\n")
    return df

def identify_outliers(df):
    
    print("="*80)
    print("OUTLIER DETECTION")
    print("="*80)
    
    outliers = {}
    
    median_gdp = df['gdp_per_capita'].median()
    high_ai_low_gdp = df[
        (df['avg_interest'] > df['avg_interest'].quantile(0.75)) &
        (df['gdp_per_capita'] < median_gdp)
    ].sort_values('avg_interest', ascending=False)
    
    print("\nHIGH AI INTEREST, LOW GDP (Unexpected Leaders):")
    print("-"*80)
    for _, row in high_ai_low_gdp.head(10).iterrows():
        print(f"  {row['country_name']:20s}: AI={row['avg_interest']:5.1f}%, GDP=${row['gdp_per_capita']:,.0f}")
    
    outliers['high_ai_low_gdp'] = high_ai_low_gdp
    
    high_gdp = df['gdp_per_capita'].quantile(0.75)
    low_ai_high_gdp = df[
        (df['avg_interest'] < df['avg_interest'].median()) &
        (df['gdp_per_capita'] > high_gdp)
    ].sort_values('avg_interest', ascending=True)
    
    print("\nLOW AI INTEREST, HIGH GDP (Underperformers):")
    print("-"*80)
    for _, row in low_ai_high_gdp.head(5).iterrows():
        print(f"  {row['country_name']:20s}: AI={row['avg_interest']:5.1f}%, GDP=${row['gdp_per_capita']:,.0f}")
    
    outliers['low_ai_high_gdp'] = low_ai_high_gdp
    
    top_ai = df.nlargest(10, 'avg_interest')
    
    print("\nTOP 10 AI ADOPTION LEADERS:")
    print("-"*80)
    for i, (_, row) in enumerate(top_ai.iterrows(), 1):
        print(f"  {i:2d}. {row['country_name']:20s}: {row['avg_interest']:5.1f}% (GDP: ${row['gdp_per_capita']:,.0f})")
    
    outliers['top_performers'] = top_ai
    
    return outliers

def deep_dive_country(df, country_name):
    
    country = df[df['country_name'] == country_name]
    
    if len(country) == 0:
        print(f"Warning: {country_name} not found")
        return None
    
    country = country.iloc[0]
    
    print(f"\n{'='*80}")
    print(f"DEEP DIVE: {country_name}")
    print(f"{'='*80}")
    
    print(f"\nCore Metrics:")
    print(f"  AI Interest:         {country['avg_interest']:.2f}% (Rank: {(df['avg_interest'] > country['avg_interest']).sum() + 1}/{len(df)})")
    print(f"  GDP per Capita:      ${country['gdp_per_capita']:,.0f}")
    print(f"  Internet Users:      {country['internet_users_pct']:.1f}%")
    print(f"  Tertiary Education:  {country['tertiary_education']:.1f}%")
    print(f"  Population:          {country['population']:,.0f}")
    
    if 'economic_category' in country:
        print(f"  Economic Category:   {country['economic_category']}")
    
    if 'region' in country:
        print(f"  Region:              {country['region']}")
    
    if 'ai_adoption_score' in country:
        print(f"  AI Adoption Score:   {country['ai_adoption_score']:.2f}")
    
    print(f"\nPercentile Rankings:")
    for metric in ['avg_interest', 'gdp_per_capita', 'internet_users_pct', 'tertiary_education']:
        if metric in df.columns:
            percentile = (df[metric] < country[metric]).sum() / len(df) * 100
            print(f"  {metric:25s}: {percentile:5.1f}th percentile")
    
    if 'economic_category' in country:
        similar = df[df['economic_category'] == country['economic_category']]
        print(f"\nComparison to {country['economic_category']} Countries:")
        print(f"  AI Interest - This country: {country['avg_interest']:.2f}%, Category avg: {similar['avg_interest'].mean():.2f}%")
        print(f"  GDP - This country: ${country['gdp_per_capita']:,.0f}, Category avg: ${similar['gdp_per_capita'].mean():,.0f}")
    
    return country

def create_outlier_visualizations(df, outliers):
    
    print("\nGenerating outlier visualizations...")
    
    df_plot = df.copy()
    df_plot['population'].fillna(df_plot['population'].median(), inplace=True)
    df_plot['category'] = 'Normal'
    
    high_ai_low_gdp_codes = outliers['high_ai_low_gdp']['country_code'].tolist()
    low_ai_high_gdp_codes = outliers['low_ai_high_gdp']['country_code'].tolist()
    
    df_plot.loc[df_plot['country_code'].isin(high_ai_low_gdp_codes), 'category'] = 'High AI, Low GDP'
    df_plot.loc[df_plot['country_code'].isin(low_ai_high_gdp_codes), 'category'] = 'Low AI, High GDP'
    
    fig1 = px.scatter(df_plot,
                     x='gdp_per_capita',
                     y='avg_interest',
                     color='category',
                     size='population',
                     hover_data=['country_name', 'internet_users_pct'],
                     title='AI Adoption Outliers - Unexpected Patterns',
                     labels={
                         'gdp_per_capita': 'GDP per Capita (USD)',
                         'avg_interest': 'AI Interest (%)',
                         'category': 'Category'
                     },
                     log_x=True,
                     color_discrete_map={
                         'Normal': 'lightblue',
                         'High AI, Low GDP': 'green',
                         'Low AI, High GDP': 'red'
                     })
    
    fig1.update_layout(width=1100, height=700)
    
    output_path1 = Path('visualizations/outliers_scatter.html')
    fig1.write_html(output_path1)
    print(f"Outlier scatter plot saved: {output_path1}")
    
    top_unexpected = outliers['high_ai_low_gdp'].head(10)
    
    fig2 = px.bar(top_unexpected,
                  x='country_name',
                  y='avg_interest',
                  color='gdp_per_capita',
                  title='Unexpected Leaders - High AI Interest, Low GDP',
                  labels={
                      'avg_interest': 'AI Interest (%)',
                      'country_name': 'Country',
                      'gdp_per_capita': 'GDP per Capita'
                  },
                  color_continuous_scale='Viridis')
    
    fig2.update_layout(xaxis_tickangle=-45, width=1000, height=600)
    
    output_path2 = Path('visualizations/outliers_unexpected_leaders.html')
    fig2.write_html(output_path2)
    print(f"Unexpected leaders chart saved: {output_path2}")
    
    return fig1, fig2

def main():
    
    df = load_data()
    
    outliers = identify_outliers(df)
    
    create_outlier_visualizations(df, outliers)
    
    case_studies = ['Ghana', 'Philippines', 'Belarus']
    for country in case_studies:
        if country in df['country_name'].values:
            deep_dive_country(df, country)
    
    print("\n" + "="*80)
    print("OUTLIER ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
