"""
Advanced Visualizations - AI Adoption Project
============================================

Box plots, regional comparisons, ve diğer gelişmiş görselleştirmeler
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

def load_data():
    """Temizlenmiş veriyi yükle"""
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"✅ {len(df)} ülke yüklendi\n")
    return df

def create_box_plots(df):
    """Box plot görselleştirmeleri"""
    print("📦 Box plots oluşturuluyor...")
    
    # 1. Economic category bazında AI interest
    fig1 = px.box(df,
                  x='economic_category',
                  y='avg_interest',
                  color='economic_category',
                  points='all',
                  hover_data=['country_name'],
                  title='AI Interest Distribution by Economic Category',
                  labels={
                      'avg_interest': 'AI Interest (%)',
                      'economic_category': 'Economic Category'
                  },
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig1.update_layout(showlegend=False, width=900, height=600)
    
    output_path1 = Path('visualizations/boxplot_economic_category.html')
    fig1.write_html(output_path1)
    print(f"  ✅ {output_path1}")
    
    # 2. Region bazında AI interest
    if 'region' in df.columns:
        fig2 = px.box(df,
                      x='region',
                      y='avg_interest',
                      color='region',
                      points='all',
                      hover_data=['country_name'],
                      title='AI Interest Distribution by Region',
                      labels={
                          'avg_interest': 'AI Interest (%)',
                          'region': 'Region'
                      })
        
        fig2.update_xaxes(tickangle=-45)
        fig2.update_layout(showlegend=False, width=1200, height=600)
        
        output_path2 = Path('visualizations/boxplot_regions.html')
        fig2.write_html(output_path2)
        print(f"  ✅ {output_path2}")

def create_violin_plots(df):
    """Violin plot görselleştirmeleri"""
    print("\n🎻 Violin plots oluşturuluyor...")
    
    # Continent bazında
    if 'continent' in df.columns:
        fig = px.violin(df,
                       x='continent',
                       y='avg_interest',
                       color='continent',
                       box=True,
                       points='all',
                       hover_data=['country_name'],
                       title='AI Interest Distribution by Continent',
                       labels={
                           'avg_interest': 'AI Interest (%)',
                           'continent': 'Continent'
                       })
        
        fig.update_layout(showlegend=False, width=1000, height=600)
        
        output_path = Path('visualizations/violin_continents.html')
        fig.write_html(output_path)
        print(f"  ✅ {output_path}")

def create_regional_comparison(df):
    """Bölgesel karşılaştırma görselleştirmeleri"""
    print("\n🌍 Bölgesel karşılaştırmalar oluşturuluyor...")
    
    if 'continent' not in df.columns:
        print("  ⚠️  continent kolonu bulunamadı")
        return
    
    # Continent bazında ortalamalar
    continent_stats = df.groupby('continent').agg({
        'avg_interest': 'mean',
        'gdp_per_capita': 'mean',
        'internet_users_pct': 'mean',
        'tertiary_education': 'mean',
        'country_name': 'count'
    }).round(2)
    
    continent_stats.rename(columns={'country_name': 'country_count'}, inplace=True)
    continent_stats = continent_stats.reset_index()
    
    # 1. Bar chart - AI interest by continent
    fig1 = px.bar(continent_stats,
                  x='continent',
                  y='avg_interest',
                  color='avg_interest',
                  text='avg_interest',
                  title='Average AI Interest by Continent',
                  labels={
                      'avg_interest': 'Average AI Interest (%)',
                      'continent': 'Continent'
                  },
                  color_continuous_scale='Viridis')
    
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(width=900, height=600, showlegend=False)
    
    output_path1 = Path('visualizations/regional_ai_interest.html')
    fig1.write_html(output_path1)
    print(f"  ✅ {output_path1}")
    
    # 2. Radar chart - Multi-dimensional comparison
    categories = ['AI Interest', 'GDP', 'Internet', 'Education']
    
    fig2 = go.Figure()
    
    for continent in continent_stats['continent']:
        data = continent_stats[continent_stats['continent'] == continent].iloc[0]
        
        # Normalize to 0-100 scale
        values = [
            data['avg_interest'],
            (data['gdp_per_capita'] / df['gdp_per_capita'].max()) * 100,
            data['internet_users_pct'],
            data['tertiary_education']
        ]
        
        fig2.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=continent
        ))
    
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Continental Profile - Multi-dimensional Comparison',
        width=800,
        height=700
    )
    
    output_path2 = Path('visualizations/regional_radar.html')
    fig2.write_html(output_path2)
    print(f"  ✅ {output_path2}")
    
    # 3. Sunburst - Hierarchical view
    if 'region' in df.columns:
        sunburst_data = df[['continent', 'region', 'country_name', 'avg_interest']].copy()
        sunburst_data = sunburst_data.dropna()  # Remove rows with NaN values
        
        fig3 = px.sunburst(sunburst_data,
                          path=['continent', 'region', 'country_name'],
                          values='avg_interest',
                          title='Hierarchical View - Continent > Region > Country',
                          color='avg_interest',
                          color_continuous_scale='RdYlGn',
                          color_continuous_midpoint=df['avg_interest'].mean())
        
        fig3.update_layout(width=1000, height=1000)
        
        output_path3 = Path('visualizations/regional_sunburst.html')
        fig3.write_html(output_path3)
        print(f"  ✅ {output_path3}")
    
    # 4. Bubble chart - GDP vs AI by continent
    df_bubble = df.copy()
    df_bubble['population'].fillna(df_bubble['population'].median(), inplace=True)
    
    fig4 = px.scatter(df_bubble,
                     x='gdp_per_capita',
                     y='avg_interest',
                     size='population',
                     color='continent',
                     hover_data=['country_name', 'internet_users_pct'],
                     title='GDP vs AI Interest - Continental Patterns',
                     labels={
                         'gdp_per_capita': 'GDP per Capita (USD)',
                         'avg_interest': 'AI Interest (%)',
                         'continent': 'Continent'
                     },
                     log_x=True,
                     size_max=50)
    
    fig4.update_layout(width=1100, height=700)
    
    output_path4 = Path('visualizations/regional_bubble.html')
    fig4.write_html(output_path4)
    print(f"  ✅ {output_path4}")

def create_distribution_plots(df):
    """Dağılım grafikleri"""
    print("\n📊 Dağılım grafikleri oluşturuluyor...")
    
    # 1. Histogram - AI interest distribution
    fig1 = px.histogram(df,
                       x='avg_interest',
                       nbins=20,
                       title='Distribution of AI Interest Across Countries',
                       labels={'avg_interest': 'AI Interest (%)'},
                       color_discrete_sequence=['steelblue'])
    
    fig1.add_vline(x=df['avg_interest'].mean(), 
                   line_dash="dash", 
                   line_color="red",
                   annotation_text=f"Mean: {df['avg_interest'].mean():.1f}%")
    
    fig1.update_layout(width=900, height=500)
    
    output_path1 = Path('visualizations/distribution_histogram.html')
    fig1.write_html(output_path1)
    print(f"  ✅ {output_path1}")
    
    # 2. Multiple histograms by economic category
    fig2 = px.histogram(df,
                       x='avg_interest',
                       color='economic_category',
                       nbins=15,
                       barmode='overlay',
                       opacity=0.7,
                       title='AI Interest Distribution by Economic Category',
                       labels={'avg_interest': 'AI Interest (%)'},
                       color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig2.update_layout(width=1000, height=600)
    
    output_path2 = Path('visualizations/distribution_by_category.html')
    fig2.write_html(output_path2)
    print(f"  ✅ {output_path2}")

def create_treemap(df):
    """Treemap görselleştirmesi"""
    print("\n🗺️  Treemap oluşturuluyor...")
    
    if 'continent' in df.columns and 'region' in df.columns:
        df_tree = df[['continent', 'region', 'country_name', 'population', 'avg_interest', 
                      'gdp_per_capita', 'internet_users_pct']].copy()
        df_tree = df_tree.dropna(subset=['continent', 'region', 'country_name', 'population', 'avg_interest'])
        
        fig = px.treemap(df_tree,
                        path=['continent', 'region', 'country_name'],
                        values='population',
                        color='avg_interest',
                        hover_data=['gdp_per_capita', 'internet_users_pct'],
                        title='World AI Adoption - Treemap by Population',
                        color_continuous_scale='RdYlGn',
                        color_continuous_midpoint=df['avg_interest'].mean())
        
        fig.update_layout(width=1200, height=800)
        
        output_path = Path('visualizations/treemap_population.html')
        fig.write_html(output_path)
        print(f"  ✅ {output_path}")

def create_heatmap_matrix(df):
    """Country comparison heatmap"""
    print("\n🔥 Heatmap matrix oluşturuluyor...")
    
    # Top 30 ülke seç
    top_countries = df.nlargest(30, 'avg_interest')
    
    # Sadece numeric kolonları al
    numeric_cols = ['avg_interest', 'gdp_per_capita', 'tertiary_education', 
                    'internet_users_pct', 'ai_adoption_score']
    
    available_cols = [col for col in numeric_cols if col in top_countries.columns]
    
    # Normalize et (0-100)
    heatmap_data = top_countries[available_cols].copy()
    for col in available_cols:
        heatmap_data[col] = (heatmap_data[col] / heatmap_data[col].max()) * 100
    
    heatmap_data.index = top_countries['country_name']
    
    fig = px.imshow(heatmap_data.T,
                    labels=dict(x="Country", y="Metric", color="Normalized Score (0-100)"),
                    title='Top 30 Countries - Multi-metric Heatmap',
                    color_continuous_scale='RdYlGn',
                    aspect='auto')
    
    fig.update_xaxes(tickangle=-45)
    fig.update_layout(width=1400, height=600)
    
    output_path = Path('visualizations/heatmap_top30.html')
    fig.write_html(output_path)
    print(f"  ✅ {output_path}")

def main():
    """Ana işlem"""
    print("\n" + "=" * 80)
    print("🎨 ADVANCED VISUALIZATIONS OLUŞTURULUYOR")
    print("=" * 80)
    
    df = load_data()
    
    create_box_plots(df)
    create_violin_plots(df)
    create_regional_comparison(df)
    create_distribution_plots(df)
    create_treemap(df)
    create_heatmap_matrix(df)
    
    print("\n" + "=" * 80)
    print("✅ TÜM GÖRSELLEŞTİRMELER TAMAMLANDI!")
    print("=" * 80)
    print("\n📁 visualizations/ klasörünü kontrol edin!")

if __name__ == "__main__":
    main()
