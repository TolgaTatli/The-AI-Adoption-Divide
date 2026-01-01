# 🌍 The AI Adoption Divide

**How Economic Development Shapes Global AI Tool Adoption - A Geographic Analysis**

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Data](https://img.shields.io/badge/Countries-103-green.svg)](data/)
[![Visualizations](https://img.shields.io/badge/Visualizations-24-orange.svg)](visualizations/)

## 📊 Project Overview

This data science project analyzes how 103 countries worldwide embrace AI tools (specifically ChatGPT) and explores the relationship with economic development, internet penetration, education levels, and geographic factors.

### 🎯 Research Question
> **"Does economic development determine AI adoption, or are there unexpected patterns that challenge conventional wisdom?"**

### 🌟 Key Finding
**Surprise!** Some of the world's poorest countries (Ghana 🇬🇭, Tanzania 🇹🇿) show HIGHER AI adoption than many wealthy nations!

---

## 🏆 Top 10 AI Adoption Leaders

1. 🥇 **Japan** (53.9%)
2. 🥈 **Israel** (53.3%)
3. 🥉 **Ghana** (51.2%) - **Unexpected leader!** 
4. **Singapore** (49.8%)
5. **Belarus** (48.3%)
6. **Australia** (46.7%)
7. **Tanzania** (46.2%)
8. **Kazakhstan** (46.1%)
9. **Canada** (46.0%)
10. **Nepal** (45.8%)

---

## 📈 Key Results

### Continental Patterns
| Continent | Avg AI Interest | Countries |
|-----------|----------------|-----------|
| 🌍 **Africa** | **41.2%** | 16 |
| 🌊 Oceania | 42.8% | 4 |
| 🌏 Asia | 37.7% | 39 |
| 🇪🇺 Europe | 35.5% | 32 |
| 🌎 Americas | 33.5% | 11 |

**Insight:** Africa leads globally despite lowest GDP! 🚀

### Statistical Analysis
- **Correlation (GDP ↔ AI):** +0.199 (weak!)
- **ANOVA:** p < 0.05 (significant differences between economic categories)
- **Regression R²:** 0.257 (economic factors explain only 26%)
- **Clustering:** 4 distinct adoption profiles identified

---

## 🎨 Visualizations (24 Total)

### Interactive Dashboards
- 🗺️ World Choropleth Map
- 📊 GDP vs AI Scatter
- 🎯 Clustering Visualization
- 📦 Box Plots by Region
- 🌐 Sunburst Hierarchical Chart
- 🔥 Correlation Heatmap
- 🎻 Violin Plots
- 📈 Radar Charts

[View all visualizations →](visualizations/)

---

## 📂 Project Structure

```
DATASCIENCE/
├── data/
│   ├── raw/                     # Google Trends + World Bank data
│   └── processed/               # Cleaned datasets (103 countries)
├── scripts/
│   ├── data_collection.py       # API data collection
│   ├── data_cleaning.py         # Cleaning + feature engineering
│   ├── statistical_analysis.py # Correlation, regression, ANOVA
│   ├── clustering_analysis.py   # K-means clustering
│   ├── advanced_visualizations.py
│   └── outlier_analysis.py
├── visualizations/              # 24 interactive HTML files
├── notebooks/                   # Jupyter analysis notebooks
└── docs/
    ├── COMPREHENSIVE_REPORT.md  # Full analysis report
    └── outlier_analysis_report.md
```

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/TolgaTatli/The-AI-Adoption-Divide.git
cd The-AI-Adoption-Divide

# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run analysis
python scripts/data_cleaning.py
python scripts/statistical_analysis.py
python scripts/clustering_analysis.py
python scripts/advanced_visualizations.py

# Open visualizations
start visualizations/world_map_ai_adoption.html
```

---

## 🔬 Methodology

### Data Sources
1. **Google Trends API** - ChatGPT search interest (103 countries)
2. **World Bank Open Data** - GDP, education, internet, population

### Analysis Techniques
- ✅ Statistical Tests: Pearson correlation, ANOVA, multiple regression
- ✅ Machine Learning: K-means clustering (4 clusters)
- ✅ Geographic Analysis: 15 regions across 5 continents
- ✅ Outlier Detection: Deep dive into surprises

---

## 📚 Key Dependencies

```python
pandas>=1.5.0          # Data manipulation
plotly>=5.11.0         # Interactive visualizations
scikit-learn>=1.2.0    # ML clustering
scipy>=1.9.0           # Statistical tests
pytrends>=4.9.0        # Google Trends API
requests>=2.28.0       # World Bank API
```

---

## 📊 Key Findings

### ✅ Confirmed
- Significant differences between economic categories (p < 0.05)
- 4 distinct adoption profiles exist
- Regional patterns are strong

### ❌ Rejected
- GDP is NOT a strong predictor (r = 0.199)
- Rich countries don't always lead
- Internet penetration shows negative correlation!

### 🤯 Unexpected
- Developing countries > Emerging economies (38.1% vs 34.4%)
- Africa leads globally
- Ghana (#3), Tanzania (#7) beat most developed nations

---

## 🎓 Academic Value

### Novel Insights
- Digital leapfrogging in AI adoption
- Mobile-first AI patterns
- Youth demographic effects
- Economic necessity drives adoption

### Methodological Strengths
- Large sample (103 countries)
- Multi-source triangulation
- Rigorous statistical testing
- Transparent limitations

---

## 📝 Documentation

- 📄 [Comprehensive Analysis Report](docs/COMPREHENSIVE_REPORT.md)
- 📋 [Outlier Analysis](docs/outlier_analysis_report.md)
- 💡 [Future Improvements](docs/improvement_suggestions.md)

---

## 🤝 Contributing

Contributions welcome! See [improvement_suggestions.md](docs/improvement_suggestions.md) for ideas:
- Time series analysis
- Qualitative interviews
- Language analysis
- Platform comparisons
- Interactive dashboard

---

## 📄 License

MIT License - See LICENSE for details

### Data Licenses
- Google Trends: [Terms of Service](https://trends.google.com/trends/)
- World Bank: [CC BY-4.0](https://www.worldbank.org/en/about/legal)

---

## 🏆 Project Stats

- 📊 **103 countries** analyzed
- 🌍 **5 continents** covered
- 📈 **24 visualizations** created
- 🤖 **4 ML clusters** identified
- ⏱️ **~8 hours** development time

---

**🌍 "The future of AI is not just in Silicon Valley—it's in Accra, Minsk, and Dar es Salaam."**

---

*Last Updated: January 1, 2026*

---

## 📞 Contact

- GitHub: [@TolgaTatli](https://github.com/TolgaTatli)
- Repository: [The-AI-Adoption-Divide](https://github.com/TolgaTatli/The-AI-Adoption-Divide)
