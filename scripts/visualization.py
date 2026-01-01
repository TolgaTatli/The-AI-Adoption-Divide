"""
Visualization Script - AI Adoption Project

Creates interactive maps and charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

class AIAdoptionVisualizer:
    
    def __init__(self, data_path="data/processed/ai_adoption_cleaned.csv"):
        self.df = pd.read_csv(data_path)
        self.output_dir = Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)
        print(f"Loaded {len(self.df)} records")
    
    def create_world_map(self):
        
        print("\nGenerating world map...")
        
        fig = px.choropleth(
            self.df,
            locations='country_code_iso3',
            locationmode='ISO-3',
            color='avg_interest',
            hover_name='country_name',
            hover_data={
                'country_code_iso3': False,
                'avg_interest': ':.1f',
                'gdp_per_capita': ':,.0f',
                'internet_users_pct': ':.1f'
            },
            title='AI Tool Adoption by Country (ChatGPT Interest)',
            color_continuous_scale='Viridis',
            labels={
                'avg_interest': 'Search Interest',
                'gdp_per_capita': 'GDP per Capita ($)',
                'internet_users_pct': 'Internet Users (%)'
            },
            range_color=[20, 60]
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False, 
                showcoastlines=True,
                projection_type='natural earth'
            ),
            height=600
        )
        
        output_file = self.output_dir / "world_map_ai_adoption.html"
        fig.write_html(str(output_file))
        print(f"Map saved: {output_file}")
        
        return fig
    
    def create_scatter_gdp_vs_ai(self):
        
        print("\nGenerating GDP vs AI Interest chart...")
        
        df_plot = self.df.copy()
        df_plot['population'] = df_plot['population'].fillna(df_plot['population'].median())
        
        fig = px.scatter(
            df_plot,
            x='gdp_per_capita',
            y='avg_interest',
            size='population',
            color='economic_category',
            hover_name='country_name',
            title='Economic Development vs AI Adoption',
            labels={
                'gdp_per_capita': 'GDP per Capita ($)',
                'avg_interest': 'AI Interest (Google Trends)'
            },
            log_x=True
        )
        
        output_file = self.output_dir / "scatter_gdp_vs_ai.html"
        fig.write_html(str(output_file))
        print(f"Chart saved: {output_file}")
        
        return fig
    
    def create_top_countries_bar(self, top_n=15):
        
        print(f"\nGenerating top {top_n} countries chart...")
        
        top_countries = self.df.nlargest(top_n, 'avg_interest')
        
        fig = px.bar(
            top_countries,
            x='country_name',
            y='avg_interest',
            color='economic_category',
            title=f'Top {top_n} Countries by AI Tool Interest',
            labels={'avg_interest': 'Search Interest', 'country_name': 'Country'}
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        output_file = self.output_dir / f"top_{top_n}_countries.html"
        fig.write_html(str(output_file))
        print(f"Chart saved: {output_file}")
        
        return fig
    
    def create_all_visualizations(self):
        
        print("="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        
        self.create_world_map()
        self.create_scatter_gdp_vs_ai()
        self.create_top_countries_bar()
        
        print("\n" + "="*60)
        print("ALL VISUALIZATIONS COMPLETE")
        print(f"Output folder: {self.output_dir}")
        print("Total charts: 3")
        print("="*60)

def main():
    
    visualizer = AIAdoptionVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main()
