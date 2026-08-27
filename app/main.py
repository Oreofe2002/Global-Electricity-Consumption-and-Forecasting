import streamlit as st

# Configure the universal browser tab layout
st.set_page_config(
    page_title="Global Energy Analytics Platform",
    page_icon="⚡",
    layout="wide"
)

# Application Main Hero Title
st.title("⚡ Global Energy Consumption & Forecasting Platform")
st.markdown("---")

# Layout Configuration: Set up side-by-side informational cards
col1, col2 = st.columns(2)

with col1:
    st.header("📌 Project Executive Summary")
    st.write(
        "This interactive analytics platform uses data science to explore how energy "
        "use has changed over time, identify the world’s major energy consumers"
        "and apply machine learning to predict future trends in electricity markets."
    )
    st.write(
        "Navigate through the sidebar pages to explore specific data layers, "
        "test predictive machine learning features, or examine time-series model projections."
    )

with col2:
    st.header("🗂️ Platform Architecture")
    st.info("**Page 1: Global Overview** — Long-term production and demand charts.")
    st.info("**Page 2: Country Rankings** — Absolute vs. Per Capita leaderboards.")
    st.info("**Page 3: Energy Transition** — Fossil fuels vs. Renewables generation mix.")
    st.info("**Page 4: ML Predictive Sandbox** — Test the winning XGBoost model inputs.")
    st.info("**Page 5: Time-Series Projections** — Deep-dive country trend forecasting.")
