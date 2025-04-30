import streamlit as st
import pandas as pd
import joblib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualizations.driver_charts import (
    plot_avg_finish_per_season,
    plot_points_per_race,
    plot_podium_count,
    plot_team_driver_performance,
    plot_driver_comparison
)
from visualizations.constructor_charts import (
    plot_avg_driver_points,
    plot_total_pair_points,
    plot_win_rate_by_year,
    plot_dnf_rate,
    plot_team_points_by_season,
    plot_constructor_tiers,
    plot_best_driver_team_pairings
)

# Streamlit Page Config
st.set_page_config(page_title="F1 Analytics Dashboard", layout="wide")

# Load Data
@st.cache_data

def load_data():
    return pd.read_csv("public_data/features_ready.csv")


df = load_data()

# Fun Facts
fun_facts = [
    "Schumacher had 11 wins in 2002",
    "Hamilton has the most pole positions in F1 history",
    "Verstappen won 10 consecutive races in 2023",
    "McLaren won the 1988 season with 15/16 wins",
    "Ferrari has the most constructor titles",
    "Sebastian Vettel won 4 titles with Red Bull",
    "Ayrton Senna won 6 times at Monaco",
    "Kimi Raikkonen holds the record for most races before first win",
    "Button's 2011 Canadian GP win was from P21",
    "Gasly won his first race at Monza 2020"
]

# App Title
st.title("🏎️ Formula 1 Analytics Dashboard")
st.markdown("Explore drivers, constructors, and predict outcomes with real data.")

# TABS
tab1, tab2, tab3 = st.tabs(["👨‍✈️ Driver Insights", "🏢 Constructor Insights", "🎯 Race Outcome Prediction"])

# ---------------- DRIVER INSIGHTS ----------------
with tab1:
    st.header("Driver Performance Over Time")

    # Filters
    selected_year = st.slider("Select Season", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].max()))
    filtered_df = df[df['year'] == selected_year]

    col1, col2 = st.columns(2)
    col1.plotly_chart(plot_avg_finish_per_season(filtered_df))
    col2.plotly_chart(plot_points_per_race(filtered_df))

    st.plotly_chart(plot_podium_count(filtered_df))

    st.subheader("Team-Specific Driver Trends")
    selected_team = st.selectbox("Constructor", df['constructor_name'].unique(), key="driver_constructor")
    st.plotly_chart(plot_team_driver_performance(df, selected_team))

    st.subheader("Compare Two Drivers (Year-by-Year)")
    driver1 = st.selectbox("Driver 1", df['driver_name'].unique(), key="drv1")
    driver2 = st.selectbox("Driver 2", df['driver_name'].unique(), key="drv2")
    st.plotly_chart(plot_driver_comparison(df, driver1, driver2))

# ---------------- CONSTRUCTOR INSIGHTS ----------------
with tab2:
    st.header("Constructor Performance Dashboard")
    selected_year = st.slider("Select Season", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].max()), key="year2")
    year_df = df[df['year'] == selected_year]

    st.plotly_chart(plot_avg_driver_points(year_df))
    st.plotly_chart(plot_total_pair_points(year_df))
    st.plotly_chart(plot_win_rate_by_year(df))
    st.plotly_chart(plot_dnf_rate(df))
    st.plotly_chart(plot_team_points_by_season(df))
    st.plotly_chart(plot_constructor_tiers(df))

    st.subheader("Top Driver–Team Pairings (All-Time)")
    st.plotly_chart(plot_best_driver_team_pairings(df))

# ---------------- RACE PREDICTION ----------------
with tab3:
    st.header("🎯 Predict Race Outcome")
    st.markdown("Input your own setup to see predicted podium finishes")

    # Load models
    rf = joblib.load("../models/race_prediction/random_forest.pkl")
    xgb = joblib.load("../models/race_prediction/xgboost.pkl")

    st.subheader("📋 Input Race Setup")

    col1, col2 = st.columns(2)
    driver_input = col1.selectbox("Driver", df['driver_name'].unique(), key="predict_driver")
    constructor_input = col2.selectbox("Constructor", df['constructor_name'].unique(), key="predict_constructor")

    grid = st.slider("Grid Position", 1, 20, 10)
    rolling_points_driver = st.number_input("Driver Rolling Avg Points", min_value=0.0, max_value=50.0, value=12.0)
    synergy = st.slider("Team Synergy Score", 0.0, 1.0, 0.5)
    avg_finish_season = st.number_input("Avg Season Finish", min_value=1.0, max_value=20.0, value=7.0)
    constructor_dnf_rate = st.slider("Constructor DNF Rate", 0.0, 1.0, 0.1)
    constructor_avg_points = st.number_input("Constructor Avg Points", min_value=0.0, max_value=50.0, value=15.0)

    input_data = pd.DataFrame.from_dict({
        'driver_name': [driver_input],
        'constructor_name': [constructor_input],
        'grid': [grid],
        'rolling_points_driver': [rolling_points_driver],
        'synergy': [synergy],
        'avg_finish_season': [avg_finish_season],
        'constructor_dnf_rate': [constructor_dnf_rate],
        'constructor_avg_points': [constructor_avg_points]
    })

    input_features = ['rolling_points_driver', 'constructor_dnf_rate', 'avg_finish_season', 'synergy', 'grid', 'constructor_avg_points']

    rf_pred = rf.predict(input_data[input_features])[0]
    xgb_pred = xgb.predict(input_data[input_features])[0]

    col1, col2 = st.columns(2)
    col1.metric("Random Forest Prediction", rf_pred)
    col2.metric("XGBoost Prediction", xgb_pred)

    st.success(f"🧠 Fun Fact: {fun_facts[selected_year % len(fun_facts)]}")

    if grid >= 15 and (int(rf_pred) <= 3 or int(xgb_pred) <= 3):
        st.warning("⚠️ Possible Upset Alert: Low grid but high podium prediction!")
