"""
Outlier Analysis - AI Adoption Project
=====================================

Sürpriz/ilginç ülkelerin detaylı analizi
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

def load_data():
    """Temizlenmiş veriyi yükle"""
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"✅ {len(df)} ülke yüklendi\n")
    return df

def identify_outliers(df):
    """İlginç outlier'ları tespit et"""
    print("=" * 80)
    print("🔍 OUTLIER TESPİTİ")
    print("=" * 80)
    
    outliers = {}
    
    # 1. High AI, Low GDP (Unexpected Leaders)
    median_gdp = df['gdp_per_capita'].median()
    high_ai_low_gdp = df[
        (df['avg_interest'] > df['avg_interest'].quantile(0.75)) &
        (df['gdp_per_capita'] < median_gdp)
    ].sort_values('avg_interest', ascending=False)
    
    print("\n🌟 HIGH AI INTEREST, LOW GDP (Unexpected Leaders):")
    print("-" * 80)
    for _, row in high_ai_low_gdp.head(10).iterrows():
        print(f"  {row['country_name']:20s}: AI={row['avg_interest']:5.1f}%, GDP=${row['gdp_per_capita']:,.0f}")
    
    outliers['high_ai_low_gdp'] = high_ai_low_gdp
    
    # 2. Low AI, High GDP (Underperformers)
    high_gdp = df['gdp_per_capita'].quantile(0.75)
    low_ai_high_gdp = df[
        (df['avg_interest'] < df['avg_interest'].median()) &
        (df['gdp_per_capita'] > high_gdp)
    ].sort_values('avg_interest', ascending=True)
    
    print("\n⚠️  LOW AI INTEREST, HIGH GDP (Underperformers):")
    print("-" * 80)
    for _, row in low_ai_high_gdp.head(5).iterrows():
        print(f"  {row['country_name']:20s}: AI={row['avg_interest']:5.1f}%, GDP=${row['gdp_per_capita']:,.0f}")
    
    outliers['low_ai_high_gdp'] = low_ai_high_gdp
    
    # 3. Extreme high AI (Top performers)
    top_ai = df.nlargest(10, 'avg_interest')
    
    print("\n🏆 TOP 10 AI ADOPTION LEADERS:")
    print("-" * 80)
    for i, (_, row) in enumerate(top_ai.iterrows(), 1):
        print(f"  {i:2d}. {row['country_name']:20s}: {row['avg_interest']:5.1f}% (GDP: ${row['gdp_per_capita']:,.0f})")
    
    outliers['top_performers'] = top_ai
    
    return outliers

def deep_dive_country(df, country_name):
    """Tek bir ülkenin detaylı analizi"""
    country = df[df['country_name'] == country_name]
    
    if len(country) == 0:
        print(f"⚠️  {country_name} bulunamadı")
        return None
    
    country = country.iloc[0]
    
    print(f"\n{'='*80}")
    print(f"🔬 DEEP DIVE: {country_name}")
    print(f"{'='*80}")
    
    print(f"\n📊 Temel Metrikler:")
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
    
    # Percentile rankings
    print(f"\n📈 Percentile Rankings:")
    for metric in ['avg_interest', 'gdp_per_capita', 'internet_users_pct', 'tertiary_education']:
        if metric in df.columns:
            percentile = (df[metric] < country[metric]).sum() / len(df) * 100
            print(f"  {metric:25s}: {percentile:5.1f}th percentile")
    
    # Comparison to similar countries
    if 'economic_category' in country:
        similar = df[df['economic_category'] == country['economic_category']]
        print(f"\n🔍 Comparison to {country['economic_category']} Countries:")
        print(f"  AI Interest - This country: {country['avg_interest']:.2f}%, Category avg: {similar['avg_interest'].mean():.2f}%")
        print(f"  GDP - This country: ${country['gdp_per_capita']:,.0f}, Category avg: ${similar['gdp_per_capita'].mean():,.0f}")
    
    return country

def create_outlier_visualizations(df, outliers):
    """Outlier görselleştirmeleri"""
    print("\n🎨 Outlier görselleştirmeleri oluşturuluyor...")
    
    # 1. Scatter plot with outliers highlighted
    df_plot = df.copy()
    df_plot['population'].fillna(df_plot['population'].median(), inplace=True)
    df_plot['category'] = 'Normal'
    
    # Mark outliers
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
    print(f"  ✅ {output_path1}")
    
    # 2. Radar chart comparison - Top outliers
    interesting_countries = [
        'Ghana', 'Belarus', 'Tanzania', 'Japan', 'Israel', 
        'United States', 'China', 'Finland'
    ]
    
    fig2 = go.Figure()
    
    metrics = ['avg_interest', 'gdp_per_capita', 'internet_users_pct', 'tertiary_education']
    metric_labels = ['AI Interest', 'GDP', 'Internet', 'Education']
    
    for country_name in interesting_countries:
        country_data = df[df['country_name'] == country_name]
        if len(country_data) > 0:
            country = country_data.iloc[0]
            
            # Normalize to 0-100
            values = []
            for metric in metrics:
                if metric in country and pd.notna(country[metric]):
                    normalized = (country[metric] / df[metric].max()) * 100
                    values.append(normalized)
                else:
                    values.append(0)
            
            fig2.add_trace(go.Scatterpolar(
                r=values,
                theta=metric_labels,
                fill='toself',
                name=country_name
            ))
    
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Outlier Profiles - Multi-dimensional Comparison',
        width=900,
        height=700
    )
    
    output_path2 = Path('visualizations/outliers_radar.html')
    fig2.write_html(output_path2)
    print(f"  ✅ {output_path2}")
    
    # 3. Bar chart - Unexpected leaders
    top_unexpected = outliers['high_ai_low_gdp'].head(10)
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=top_unexpected['country_name'],
        y=top_unexpected['avg_interest'],
        name='AI Interest',
        marker_color='green'
    ))
    
    fig3.add_trace(go.Bar(
        x=top_unexpected['country_name'],
        y=top_unexpected['gdp_per_capita'] / 1000,  # Scale to thousands
        name='GDP (thousands USD)',
        marker_color='orange',
        yaxis='y2'
    ))
    
    fig3.update_layout(
        title='Unexpected Leaders - High AI Interest Despite Low GDP',
        xaxis=dict(title='Country', tickangle=-45),
        yaxis=dict(title='AI Interest (%)'),
        yaxis2=dict(title='GDP per Capita (thousands USD)', overlaying='y', side='right'),
        width=1000,
        height=600,
        barmode='group'
    )
    
    output_path3 = Path('visualizations/outliers_unexpected_leaders.html')
    fig3.write_html(output_path3)
    print(f"  ✅ {output_path3}")

def generate_outlier_report(df, outliers):
    """Outlier raporu oluştur"""
    print("\n📝 Outlier raporu oluşturuluyor...")
    
    report = []
    report.append("# AI Adoption Outliers - Detailed Report\n")
    report.append("=" * 80)
    report.append("\n\n## Executive Summary\n")
    report.append(f"- Total countries analyzed: {len(df)}")
    report.append(f"- Unexpected high performers: {len(outliers['high_ai_low_gdp'])}")
    report.append(f"- Underperformers: {len(outliers['low_ai_high_gdp'])}")
    
    report.append("\n\n## Key Findings\n")
    report.append("\n### 1. Unexpected Leaders (High AI, Low GDP)\n")
    report.append("These countries show exceptionally high AI adoption despite lower economic development:\n")
    
    for _, row in outliers['high_ai_low_gdp'].head(5).iterrows():
        report.append(f"\n**{row['country_name']}**")
        report.append(f"- AI Interest: {row['avg_interest']:.1f}%")
        report.append(f"- GDP per Capita: ${row['gdp_per_capita']:,.0f}")
        report.append(f"- Internet Penetration: {row['internet_users_pct']:.1f}%")
        if 'region' in row:
            report.append(f"- Region: {row['region']}")
    
    report.append("\n\n### 2. Potential Explanations\n")
    report.append("- **Digital Leapfrogging**: Developing countries may skip traditional tech and adopt AI directly")
    report.append("- **Youth Demographics**: Younger populations are more tech-savvy")
    report.append("- **Mobile-First**: High mobile penetration enables AI adoption")
    report.append("- **Education Focus**: Investment in STEM education despite lower GDP")
    
    report_text = '\n'.join(report)
    
    output_path = Path('docs/outlier_analysis_report.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"  ✅ {output_path}")

def main():
    """Ana işlem"""
    print("\n" + "=" * 80)
    print("🔍 OUTLIER ANALİZİ BAŞLIYOR")
    print("=" * 80)
    
    df = load_data()
    
    # Outlier'ları tespit et
    outliers = identify_outliers(df)
    
    # İlginç ülkelerin deep dive analizi
    interesting_countries = ['Ghana', 'Belarus', 'Tanzania', 'Japan', 'Kazakhstan', 'Venezuela']
    
    for country in interesting_countries:
        if country in df['country_name'].values:
            deep_dive_country(df, country)
    
    # Görselleştirmeler
    create_outlier_visualizations(df, outliers)
    
    # Rapor oluştur
    generate_outlier_report(df, outliers)
    
    print("\n" + "=" * 80)
    print("✅ OUTLIER ANALİZİ TAMAMLANDI!")
    print("=" * 80)

if __name__ == "__main__":
    main()
