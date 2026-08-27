import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Step 1: Find the pages/ folder path
PAGES_DIR = os.path.dirname(os.path.abspath(__file__))

# Step 2: Step out TWICE to reach the absolute root folder (Global_Energy/)
ROOT_DIR = os.path.dirname(os.path.dirname(PAGES_DIR))

# Step 3: Link straight down into your true historical data matrix file
CLEAN_DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "energy_cleaned.csv")

@st.cache_data
def load_data():
    return pd.read_csv(CLEAN_DATA_PATH)

# Load data safely
df = load_data()

# Page Title header
st.title("📈 Global Energy Trends & Macro Growth")
st.markdown("---")

# Aggregate records over time chronologically
global_trends = df.groupby('year')[['primary_energy_consumption', 'electricity_generation']].sum().reset_index()

# Interactive controls window panel
st.sidebar.header("📊 Global Trend Controls")
min_year = int(global_trends['year'].min())
max_year = int(global_trends['year'].max())

year_range = st.sidebar.slider(
    "Select Analysis Window (Years):",
    min_value=min_year,
    max_value=max_year,
    value=(1990, max_year)
)

# Filter dataset rows dynamically using slider range parameters
filtered_trends = global_trends[
    (global_trends['year'] >= year_range[0]) & 
    (global_trends['year'] <= year_range[1])
]

# Build Metric Card Blocks
total_consumption_latest = filtered_trends.iloc[-1]['primary_energy_consumption']
total_generation_latest = filtered_trends.iloc[-1]['electricity_generation']

metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric(
        label=f"Primary Energy Consumption ({year_range[1]})", 
        value=f"{total_consumption_latest:,.0f} TWh"
    )
with metric_col2:
    st.metric(
        label=f"Electricity Generation ({year_range[1]})", 
        value=f"{total_generation_latest:,.0f} TWh"
    )

st.markdown("### Interactive Time-Series Growth Curve")

# Build Interactive Multi-Line Dynamic Plotly Analytics Chart
fig = px.line(
    filtered_trends, 
    x='year', 
    y=['primary_energy_consumption', 'electricity_generation'],
    labels={'value': 'Terawatt-hours (TWh)', 'year': 'Year', 'variable': 'Metric Indicator'},
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig.update_layout(
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
