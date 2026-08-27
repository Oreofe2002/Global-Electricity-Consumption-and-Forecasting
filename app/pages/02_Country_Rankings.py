import streamlit as st
import pandas as pd
import plotly.express as px
import os


PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(PAGES_DIR))
CLEAN_DATA_PATH = os.path.join(ROOT_DIR, "data", "processed", "energy_cleaned.csv")

@st.cache_data
def load_data():
    return pd.read_csv(CLEAN_DATA_PATH)

df = load_data()

# Page Title
st.title("🌍 Country Energy Profiles & Leaderboards")
st.markdown("---")


df_valid_energy = df[df['primary_energy_consumption'].notna()]
latest_complete_year = int(df_valid_energy['year'].max())

#Adding an interactive year selector widget in the sidebar (defaulting to the latest complete year)
st.sidebar.header("📊 Ranking Configurations")
available_years = sorted(df['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Data Year:", available_years, index=available_years.index(latest_complete_year))

# Filtering dataset to match the user's selected year
df_year = df[df['year'] == selected_year].copy()


if len(df_year) == 0 or df_year['primary_energy_consumption'].isna().all():
    st.warning(f"⚠️ No complete data logs found for the year {selected_year}. Try selecting {latest_complete_year} or earlier!")
else:
    # Calculating top 10 positions
    top_total = df_year.sort_values(by='primary_energy_consumption', ascending=False).head(10)
    top_per_capita = df_year.sort_values(by='energy_per_capita', ascending=False).head(10)
    
    # 4. Display layout in side-by-side columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top 10 Total Energy Consumers ({selected_year})")
        fig_total = px.bar(
            top_total,
            x='primary_energy_consumption',
            y='country',
            orientation='h',
            labels={'primary_energy_consumption': 'Primary Energy (TWh)', 'country': 'Country'},
            color='primary_energy_consumption',
            color_continuous_scale='Viridis'
        )
        fig_total.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_total, use_container_width=True)
        
    with col2:
        st.subheader(f"Top 10 Per Capita Consumers ({selected_year})")
        fig_pc = px.bar(
            top_per_capita,
            x='energy_per_capita',
            y='country',
            orientation='h',
            labels={'energy_per_capita': 'Energy Per Capita (kWh/person)', 'country': 'Country'},
            color='energy_per_capita',
            color_continuous_scale='Plasma'
        )
        fig_pc.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_pc, use_container_width=True)
