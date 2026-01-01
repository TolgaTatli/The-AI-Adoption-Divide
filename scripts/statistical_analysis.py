"""
Statistical Analysis Script - AI Adoption Project

Statistical tests, correlation analysis, and regression models.
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

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data():
    
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"Loaded {len(df)} countries\n")
    return df

def correlation_analysis(df):
    
    print("="*80)
    print("CORRELATION ANALYSIS")
    print("="*80)
    
    numeric_cols = ['avg_interest', 'gdp_per_capita', 'tertiary_education', 
                    'internet_users_pct', 'population', 'ai_adoption_score']
    
    available_cols = [col for col in numeric_cols if col in df.columns]
    corr_df = df[available_cols].corr()
    
    print("\nPearson Correlation Matrix:")
    print(corr_df.round(3))
    
    print("\nStrongest correlations with avg_interest:")
    ai_corr = corr_df['avg_interest'].sort_values(ascending=False)
    for col, val in ai_corr.items():
        if col != 'avg_interest':
            print(f"  {col:25s}: {val:+.3f}")
    
    fig = px.imshow(corr_df, 
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    title='Correlation Heatmap - AI Adoption Factors',
                    labels=dict(color="Correlation"))
    
    fig.update_layout(width=800, height=700, font=dict(size=11))
    
    output_path = Path('visualizations/correlation_heatmap.html')
    fig.write_html(output_path)
    print(f"\nHeatmap saved: {output_path}")
    
    return corr_df

def regression_analysis(df):
    
    print("\n" + "="*80)
    print("REGRESSION ANALYSIS")
    print("="*80)
    
    feature_cols = ['gdp_per_capita', 'tertiary_education', 
                    'internet_users_pct', 'population']
    
    df_reg = df[feature_cols + ['avg_interest']].dropna()
    
    X = df_reg[feature_cols]
    y = df_reg['avg_interest']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    y_pred = model.predict(X_scaled)
    r2 = model.score(X_scaled, y)
    
    print(f"\nModel Performance:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    
    print(f"\nFeature Coefficients (Standardized):")
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_,
        'Abs_Coef': np.abs(model.coef_)
    }).sort_values('Abs_Coef', ascending=False)
    
    for _, row in coef_df.iterrows():
        print(f"  {row['Feature']:25s}: {row['Coefficient']:+.4f}")
    
    fig = px.bar(coef_df, 
                 x='Coefficient', 
                 y='Feature',
                 orientation='h',
                 title='Feature Importance - AI Adoption Prediction',
                 labels={'Coefficient': 'Standardized Coefficient'},
                 color='Coefficient',
                 color_continuous_scale='RdBu',
                 text_auto='.3f')
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, width=800, height=500)
    
    output_path = Path('visualizations/feature_importance.html')
    fig.write_html(output_path)
    print(f"\nFeature importance plot saved: {output_path}")
    
    return model, r2

def anova_test(df):
    
    print("\n" + "="*80)
    print("ANOVA TEST - Economic Categories")
    print("="*80)
    
    if 'economic_category' not in df.columns:
        print("Economic category column not found")
        return
    
    df_anova = df[['economic_category', 'avg_interest']].dropna()
    
    groups = []
    categories = df_anova['economic_category'].unique()
    
    for category in categories:
        group_data = df_anova[df_anova['economic_category'] == category]['avg_interest']
        groups.append(group_data)
    
    f_stat, p_value = stats.f_oneway(*groups)
    
    print(f"\nF-statistic: {f_stat:.4f}")
    print(f"P-value: {p_value:.6f}")
    
    if p_value < 0.05:
        print("\nResult: Significant difference between economic categories (p < 0.05)")
    else:
        print("\nResult: No significant difference between categories (p >= 0.05)")
    
    print("\nCategory Means:")
    for category in categories:
        mean_val = df_anova[df_anova['economic_category'] == category]['avg_interest'].mean()
        count = len(df_anova[df_anova['economic_category'] == category])
        print(f"  {category:15s}: {mean_val:.2f} (n={count})")
    
    return f_stat, p_value

def main():
    
    df = load_data()
    
    corr_df = correlation_analysis(df)
    
    model, r2 = regression_analysis(df)
    
    anova_test(df)
    
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
