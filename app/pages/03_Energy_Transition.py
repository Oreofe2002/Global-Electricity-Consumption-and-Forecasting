import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Resolve paths safely
PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(PAGES_DIR))
CLEAN_DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "energy_cleaned.csv")

@st.cache_data
def load_data():
    return pd.read_csv(CLEAN_DATA_PATH)

df = load_data()

st.title("⚡ Global Electricity Generation Mix")
st.markdown("---")


fossil_cols = ['coal_electricity', 'gas_electricity', 'oil_electricity']
clean_cols = ['hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity']

st.sidebar.header("🗺️ Grid Filter Options")
country_list = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox("Select Country/Region:", country_list, index=country_list.index("World") if "World" in country_list else 0)

#Filtering the dataset to match selection
df_filtered = df[df['country'] == selected_country].copy()

#Processing wide table layout to a long format for Plotly area charts
mix_trends = df_filtered.groupby('year')[fossil_cols + clean_cols].sum().reset_index()
mix_melted = mix_trends.melt(
    id_vars='year', 
    value_vars=fossil_cols + clean_cols,
    var_name='Source', 
    value_name='Generation_TWh'
)

mix_melted['Source'] = mix_melted['Source'].str.replace('_electricity', '').str.title()

#Render Interactive Stacked Area Chart
st.subheader(f"Evolution of {selected_country}'s Electricity Grid Mix (1990–Present)")
fig = px.area(
    mix_melted, 
    x='year', 
    y='Generation_TWh', 
    color='Source',
    labels={'Generation_TWh': 'Generation (TWh)', 'year': 'Year'},
    color_discrete_sequence=px.colors.qualitative.Safe
)

fig.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)
