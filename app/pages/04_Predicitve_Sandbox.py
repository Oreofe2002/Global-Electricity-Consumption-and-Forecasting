import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

#Resolving structural data pathing layers cleanly
PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(PAGES_DIR))
CLEAN_DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "energy_cleaned.csv")
if not os.path.exists(CLEAN_DATA_PATH):
    CLEAN_DATA_PATH = os.path.join(ROOT_DIR, "data", "Processed", "energy_cleaned.csv")

@st.cache_data
def load_and_train_champion_model():
    # Load base analytics dataset matrix
    df = pd.read_csv(CLEAN_DATA_PATH)
    

    features_list = ['gdp', 'population', 'primary_energy_consumption', 'renewables_electricity', 'fossil_electricity']
    target_col = 'electricity_demand'
    
    df_ml = df.dropna(subset=features_list + [target_col]).copy()
    
    X = df_ml[features_list]
    y = df_ml[target_col]
    
    champion_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
    ])
    champion_pipeline.fit(X, y)
    return champion_pipeline, features_list

pipe_engine, features = load_and_train_champion_model()

# Render Page Header Title
st.title("🤖 ML Electricity Demand Sandbox Simulator")
st.markdown("---")
st.write(
    "This interactive simulation layer utilizes our tournament-winning **XGBoost Regressor model** "
    "to calculate real-time grid electricity demand predictions based on custom socio-economic indicators."
)
st.sidebar.header("🛠️ Simulator Predictor Handles")


user_gdp = st.sidebar.slider("Gross Domestic Product (GDP, Billions USD):", 1, 5000, 500) * 1e9
user_pop = st.sidebar.slider("National Population Size (Millions):", 1, 1500, 100) * 1e6
user_primary_energy = st.sidebar.slider("Total Primary Energy Consumption (TWh):", 10, 5000, 300)
user_renewables = st.sidebar.slider("Renewable Power Sourced Generation (TWh):", 0, 2000, 50)
user_fossil = st.sidebar.slider("Fossil Fuel Sourced Generation (TWh):", 0, 3000, 200)

input_data = pd.DataFrame([{
    'gdp': user_gdp,
    'population': user_pop,
    'primary_energy_consumption': user_primary_energy,
    'renewables_electricity': user_renewables,
    'fossil_electricity': user_fossil
}])


predicted_demand = pipe_engine.predict(input_data)[0]


st.markdown("### 📊 Live Model Prediction Output")

kpi_col1, kpi_col2 = st.columns([2, 1])

with kpi_col1:
    st.info(
        f"💡 Based on your configuration inputs, the XGBoost engine predicts this simulated country's "
        f"overall electricity demand will scale to approximately **{predicted_demand:,.2f} Terawatt-hours (TWh)**."
    )

with kpi_col2:
    st.metric(label="Predicted Demand", value=f"{predicted_demand:,.1f} TWh")

#Displaying Interactive Data Input Table Preview
st.markdown("#### Input Parameter Vector Matrix Summary")
st.dataframe(pd.DataFrame({
    "Indicator Feature Name": ["GDP (USD)", "Population", "Primary Energy (TWh)", "Renewable Grid Mix (TWh)", "Fossil Grid Mix (TWh)"],
    "Configured Input Scalar": [f"${user_gdp:,.0f}", f"{user_pop:,.0f}", f"{user_primary_energy:,.1f}", f"{user_renewables:,.1f}", f"{user_fossil:,.1f}"]
}))
