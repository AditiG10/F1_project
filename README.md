# 🏎️ Formula 1 Race Outcome Predictor & Analytics Dashboard

This project is a complete pipeline to analyze, visualize, and predict Formula 1 race outcomes using historical and real-time data.

Fans and analysts can:
- Explore driver and constructor trends
- Visualize rivalries and team dominance
- Predict race results using machine learning models
- Interact with a polished Streamlit dashboard

---

## 📊 Data Sources & Structure

The project integrates:
- 🗂 **Kaggle F1 Historical Dataset (1950–2023)**
- 🌐 **Live scraping from ESPN for 2024 race results**

Data is cleaned, merged, and feature-engineered into a model-ready format. Key files:
- `results.csv`, `drivers.csv`, `constructors.csv`, `races.csv` – historical stats
- `espn_2024_results.csv` – scraped with Selenium for live results
- `features_ready.csv` – final engineered dataset with podium, synergy, DNF rate, rolling points

---

## 🛠 Tools & Technologies

| Category     | Tools Used                                   |
|--------------|-----------------------------------------------|
| Backend      | Python (Pandas, NumPy, Scikit-learn, XGBoost) |
| Visualization| Plotly                                        |
| Dashboard    | Streamlit                                     |
| Data Scraping| Selenium (for ESPN F1 Results)                |
| ML Models    | Random Forest, XGBoost                        |

---

## 🧠 Project Pipeline

| Stage                | Scripts / Notebooks                            |
|---------------------|------------------------------------------------|
| Data Collection      | `fetch_kaggle_data.py`, `fetch_espn_data.py`   |
| Merging              | `merge_all_sources.py`                         |
| Cleaning             | `clean_data.py`                                |
| Feature Engineering  | `generate_features.py`                         |
| Modeling Prep        | `prepare_training_data.py`                     |
| ML Notebooks         | `race_outcome_prediction.ipynb`                |
| Analysis             | `driver_performance_analysis.ipynb`, `constructor_insights.ipynb`, `eda.ipynb` |
| App Interface        | `streamlit_app.py`                             |

---

## 💡 About the Streamlit App

The app is the front-facing interface for users to interact with the full F1 analytics engine.

### 📈 Driver Insights
- View driver average finishing positions by season
- Track podium counts and points per race
- Compare two drivers side-by-side (e.g., Hamilton vs Verstappen)
- Filter by constructor

### 🏢 Constructor Insights
- Visualize average team points, DNF rates, and win consistency
- Cluster teams using KMeans into performance tiers (elite/midfield/backmarkers)
- View best driver–constructor pairings across seasons

### 🎯 Race Outcome Prediction
- Simulate race setups: change grid position, synergy, stats
- Get predicted podium from trained ML models (RF & XGBoost)
- Display confidence insights and “possible upset” alerts
- Show random fun facts from F1 history

---

## 🖥️ Run the App Locally

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
