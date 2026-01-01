"""
Statistical Analysis Script - AI Adoption Project
=================================================

İstatistiksel testler, korelasyon analizi, regression modelleri
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Stil ayarları
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data():
    """Temizlenmiş veriyi yükle"""
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"✅ {len(df)} ülke yüklendi\n")
    return df

def correlation_analysis(df):
    """Korelasyon analizi"""
    print("=" * 80)
    print("📊 KORELASYON ANALİZİ")
    print("=" * 80)
    
    # Numeric kolonları seç
    numeric_cols = ['avg_interest', 'gdp_per_capita', 'tertiary_education', 
                    'internet_users_pct', 'population', 'ai_adoption_score']
    
    # Sadece mevcut kolonları kullan
    available_cols = [col for col in numeric_cols if col in df.columns]
    corr_df = df[available_cols].corr()
    
    print("\n🔗 Pearson Korelasyon Matrisi:")
    print(corr_df.round(3))
    
    # En güçlü korelasyonlar
    print("\n⭐ avg_interest ile en güçlü korelasyonlar:")
    ai_corr = corr_df['avg_interest'].sort_values(ascending=False)
    for col, val in ai_corr.items():
        if col != 'avg_interest':
            print(f"  {col:25s}: {val:+.3f}")
    
    # Plotly interactive heatmap
    fig = px.imshow(corr_df, 
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    title='Correlation Heatmap - AI Adoption Factors',
                    labels=dict(color="Correlation"))
    
    fig.update_layout(
        width=800,
        height=700,
        font=dict(size=11)
    )
    
    output_path = Path('visualizations/correlation_heatmap.html')
    fig.write_html(output_path)
    print(f"\n💾 Heatmap kaydedildi: {output_path}")
    
    return corr_df

def regression_analysis(df):
    """Multiple Linear Regression analizi"""
    print("\n" + "=" * 80)
    print("📈 REGRESSION ANALİZİ")
    print("=" * 80)
    
    # Bağımlı ve bağımsız değişkenler
    feature_cols = ['gdp_per_capita', 'tertiary_education', 
                    'internet_users_pct', 'population']
    
    # Missing değerleri çıkar
    df_reg = df[feature_cols + ['avg_interest']].dropna()
    
    X = df_reg[feature_cols]
    y = df_reg['avg_interest']
    
    # Normalize et
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Model fit
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Predictions
    y_pred = model.predict(X_scaled)
    
    # R² score
    r2 = model.score(X_scaled, y)
    
    print(f"\n📊 Model Performance:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    
    print(f"\n🎯 Feature Coefficients (Standardized):")
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_,
        'Abs_Coef': np.abs(model.coef_)
    }).sort_values('Abs_Coef', ascending=False)
    
    for _, row in coef_df.iterrows():
        print(f"  {row['Feature']:25s}: {row['Coefficient']:+.4f}")
    
    # Feature importance plot
    fig = px.bar(coef_df, 
                 x='Coefficient', 
                 y='Feature',
                 orientation='h',
                 title='Feature Importance - AI Adoption Prediction',
                 labels={'Coefficient': 'Standardized Coefficient'},
                 color='Coefficient',
                 color_continuous_scale='RdBu',
                 text_auto='.3f')
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        width=800,
        height=500
    )
    
    output_path = Path('visualizations/feature_importance.html')
    fig.write_html(output_path)
    print(f"\n💾 Feature importance plot kaydedildi: {output_path}")
    
    # Actual vs Predicted scatter
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=y,
        y=y_pred,
        mode='markers',
        marker=dict(size=8, color='steelblue', opacity=0.6),
        text=df_reg.index,
        name='Predictions'
    ))
    
    # Perfect prediction line
    fig2.add_trace(go.Scatter(
        x=[y.min(), y.max()],
        y=[y.min(), y.max()],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Perfect Prediction'
    ))
    
    fig2.update_layout(
        title=f'Actual vs Predicted AI Interest (R² = {r2:.3f})',
        xaxis_title='Actual avg_interest',
        yaxis_title='Predicted avg_interest',
        width=800,
        height=600
    )
    
    output_path2 = Path('visualizations/regression_actual_vs_predicted.html')
    fig2.write_html(output_path2)
    print(f"💾 Actual vs Predicted plot kaydedildi: {output_path2}")
    
    return model, r2, coef_df

def anova_test(df):
    """ANOVA testi - ekonomik kategoriler arası fark"""
    print("\n" + "=" * 80)
    print("🧪 ANOVA TESTİ - Ekonomik Kategoriler")
    print("=" * 80)
    
    if 'economic_category' not in df.columns:
        print("⚠️  economic_category kolonu bulunamadı")
        return
    
    # Kategorilere göre grupla
    groups = []
    categories = df['economic_category'].dropna().unique()
    
    for cat in categories:
        group_data = df[df['economic_category'] == cat]['avg_interest'].dropna()
        groups.append(group_data)
        print(f"\n{cat}:")
        print(f"  N = {len(group_data)}")
        print(f"  Mean = {group_data.mean():.2f}")
        print(f"  Std = {group_data.std():.2f}")
    
    # ANOVA test
    f_stat, p_value = stats.f_oneway(*groups)
    
    print(f"\n📊 ANOVA Results:")
    print(f"  F-statistic: {f_stat:.4f}")
    print(f"  p-value: {p_value:.6f}")
    
    if p_value < 0.05:
        print(f"  ✅ Anlamlı fark VAR (p < 0.05)")
    else:
        print(f"  ❌ Anlamlı fark YOK (p >= 0.05)")
    
    # Pairwise t-tests
    print(f"\n🔬 Pairwise T-Tests:")
    for i, cat1 in enumerate(categories):
        for cat2 in categories[i+1:]:
            group1 = df[df['economic_category'] == cat1]['avg_interest'].dropna()
            group2 = df[df['economic_category'] == cat2]['avg_interest'].dropna()
            
            t_stat, p_val = stats.ttest_ind(group1, group2)
            significance = "✅" if p_val < 0.05 else "❌"
            print(f"  {cat1} vs {cat2}: t={t_stat:.3f}, p={p_val:.4f} {significance}")
    
    return f_stat, p_value

def regional_analysis(df):
    """Bölgesel analiz"""
    print("\n" + "=" * 80)
    print("🌍 BÖLGESEL ANALİZ")
    print("=" * 80)
    
    if 'region' not in df.columns:
        print("⚠️  region kolonu bulunamadı")
        return
    
    # Region bazında istatistikler
    regional_stats = df.groupby('region').agg({
        'avg_interest': ['mean', 'std', 'count'],
        'gdp_per_capita': 'mean',
        'ai_adoption_score': 'mean'
    }).round(2)
    
    print("\n📊 Bölge Bazında Ortalamalar:")
    print(regional_stats)
    
    # Continent bazında
    if 'continent' in df.columns:
        print("\n🌍 Kıta Bazında Ortalamalar:")
        continent_stats = df.groupby('continent').agg({
            'avg_interest': ['mean', 'std', 'count'],
            'gdp_per_capita': 'mean'
        }).round(2)
        print(continent_stats)
    
    return regional_stats

def main():
    """Ana işlem"""
    print("\n" + "=" * 80)
    print("🔬 İSTATİSTİKSEL ANALİZ BAŞLIYOR")
    print("=" * 80)
    
    df = load_data()
    
    # 1. Korelasyon analizi
    corr_df = correlation_analysis(df)
    
    # 2. Regression analizi
    model, r2, coef_df = regression_analysis(df)
    
    # 3. ANOVA testi
    f_stat, p_value = anova_test(df)
    
    # 4. Bölgesel analiz
    regional_stats = regional_analysis(df)
    
    print("\n" + "=" * 80)
    print("✅ TÜM ANALİZLER TAMAMLANDI!")
    print("=" * 80)
    print("\n📁 Oluşturulan dosyalar:")
    print("  - visualizations/correlation_heatmap.html")
    print("  - visualizations/feature_importance.html")
    print("  - visualizations/regression_actual_vs_predicted.html")

if __name__ == "__main__":
    main()
