"""
Clustering Analysis - AI Adoption Project

K-means clustering to group countries by AI adoption patterns.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def load_data():
    
    df = pd.read_csv('data/processed/ai_adoption_cleaned.csv')
    print(f"Loaded {len(df)} countries\n")
    return df

def find_optimal_clusters(X_scaled, max_k=8):
    
    print("Finding optimal number of clusters...")
    
    inertias = []
    silhouette_scores = []
    K_range = range(2, max_k+1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(K_range),
        y=inertias,
        mode='lines+markers',
        name='Inertia',
        yaxis='y1'
    ))
    
    fig.add_trace(go.Scatter(
        x=list(K_range),
        y=silhouette_scores,
        mode='lines+markers',
        name='Silhouette Score',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Elbow Method - Optimal Number of Clusters',
        xaxis=dict(title='Number of Clusters (k)'),
        yaxis=dict(title='Inertia', side='left'),
        yaxis2=dict(title='Silhouette Score', overlaying='y', side='right'),
        width=900,
        height=500
    )
    
    output_path = Path('visualizations/clustering_elbow.html')
    fig.write_html(output_path)
    print(f"Elbow plot saved: {output_path}")
    
    best_k = K_range[np.argmax(silhouette_scores)]
    print(f"Recommended clusters: {best_k} (Silhouette: {max(silhouette_scores):.3f})")
    
    return best_k

def perform_clustering(df, n_clusters=4):
    
    print(f"\nK-Means Clustering (k={n_clusters})...")
    
    feature_cols = ['avg_interest', 'gdp_per_capita', 'internet_users_pct', 
                    'tertiary_education', 'population']
    
    df_cluster = df[feature_cols + ['country_name', 'country_code']].dropna()
    
    X = df_cluster[feature_cols]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_cluster['cluster'] = kmeans.fit_predict(X_scaled)
    
    cluster_names = {
        0: 'Early Adopters',
        1: 'Fast Followers',
        2: 'Moderate Users',
        3: 'Laggards'
    }
    
    df_cluster['cluster_name'] = df_cluster['cluster'].map(cluster_names)
    
    print("\nCluster Statistics:")
    print("="*80)
    
    for cluster_id in range(n_clusters):
        cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]
        print(f"\n{cluster_names.get(cluster_id, f'Cluster {cluster_id}')} (n={len(cluster_data)}):")
        print(f"  AI Interest: {cluster_data['avg_interest'].mean():.2f} ± {cluster_data['avg_interest'].std():.2f}")
        print(f"  GDP: ${cluster_data['gdp_per_capita'].mean():.0f}")
        print(f"  Internet: {cluster_data['internet_users_pct'].mean():.1f}%")
        print(f"  Countries: {', '.join(cluster_data['country_name'].head(5).tolist())}")
        if len(cluster_data) > 5:
            print(f"           ... and {len(cluster_data)-5} more")
    
    silhouette_avg = silhouette_score(X_scaled, df_cluster['cluster'])
    print(f"\nOverall Silhouette Score: {silhouette_avg:.3f}")
    
    return df_cluster, kmeans, scaler, X_scaled

def visualize_clusters(df_cluster):
    
    print("\nGenerating cluster visualizations...")
    
    fig1 = px.scatter(df_cluster,
                     x='gdp_per_capita',
                     y='avg_interest',
                     color='cluster_name',
                     size='population',
                     hover_data=['country_name', 'internet_users_pct'],
                     title='AI Adoption Clusters - GDP vs Interest',
                     labels={
                         'gdp_per_capita': 'GDP per Capita (USD)',
                         'avg_interest': 'AI Interest (%)',
                         'cluster_name': 'Cluster'
                     },
                     log_x=True,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig1.update_layout(width=1000, height=600)
    
    output_path1 = Path('visualizations/clustering_gdp_vs_ai.html')
    fig1.write_html(output_path1)
    print(f"GDP vs AI scatter saved: {output_path1}")
    
    fig2 = px.scatter_3d(df_cluster,
                         x='gdp_per_capita',
                         y='internet_users_pct',
                         z='avg_interest',
                         color='cluster_name',
                         size='population',
                         hover_data=['country_name'],
                         title='AI Adoption Clusters - 3D View',
                         labels={
                             'gdp_per_capita': 'GDP per Capita',
                             'internet_users_pct': 'Internet Users %',
                             'avg_interest': 'AI Interest',
                             'cluster_name': 'Cluster'
                         },
                         color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig2.update_layout(width=1000, height=700)
    
    output_path2 = Path('visualizations/clustering_3d.html')
    fig2.write_html(output_path2)
    print(f"3D cluster view saved: {output_path2}")
    
    return fig1, fig2

def save_clustered_data(df_cluster):
    
    output_path = Path('data/processed/ai_adoption_clustered.csv')
    df_cluster.to_csv(output_path, index=False)
    print(f"\nClustered data saved: {output_path}")
    return output_path

def main():
    
    df = load_data()
    
    feature_cols = ['avg_interest', 'gdp_per_capita', 'internet_users_pct', 
                    'tertiary_education', 'population']
    df_scaled = df[feature_cols].dropna()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_scaled)
    
    best_k = find_optimal_clusters(X_scaled)
    
    df_cluster, kmeans, scaler, X_scaled = perform_clustering(df, n_clusters=4)
    
    visualize_clusters(df_cluster)
    
    save_clustered_data(df_cluster)
    
    print("\n" + "="*80)
    print("CLUSTERING ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
