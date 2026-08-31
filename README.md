# ⚡ Global Energy Consumption & Forecasting Platform

A full-stack data science portfolio project and interactive multi-page web application built to analyze historical energy transitions, evaluate macroeconomic demand indicators using machine learning, and forecast future regional electricity grid needs through 2030.

🔗 **Live Interactive Dashboard:** *https://global-electricity-consumption-and-forecasting-m5qcbddczwyg5ca.streamlit.app/*

---

## 📌 Project Overview & Architecture

This repository delivers an end-to-end data pipeline and predictive modeling suite designed to answer three critical domain questions:
* **What is happening?** Tracking long-term primary energy consumption and global electricity generation expansion from 1990 to the present.
* **Why is it happening?** Quantifying the statistical relationships between demographic population shifts, GDP growth, and total electricity demand.
* **What happens next?** Generating long-term time-series forecasts to project grid requirements for industrializing economies.

### 🗂️ Platform Structure
* **`01_eda.ipynb` & Page 1: Global Overview** — Visualizes global consumption paths and macro metric scales.
* **Page 2: Country Rankings** — Evaluates absolute energy metrics vs. per-capita indicators to expose high-intensity industrial nations (e.g., Qatar, Singapore).
* **Page 3: Energy Transition Mix** — Stacked area visualizations tracking the historical grid evolution from fossil baseloads to renewable adoption.
* **`02_modeling.ipynb` & Page 4: ML Predictive Sandbox** — Features an interactive scenario simulator driven by the **XGBoost Regressor** pipeline.
* **`03_forecasting.ipynb` & Page 5: Time-Series Projections** — Deep-dive country trend forecasting using **Meta Prophet** to map growth curves through 2030.

---

## 🛠️ Tech Stack & Ecosystem

* **Core Language:** Python 3.10+
* **Data Engineering:** Pandas, NumPy
* **Data Visualization:** Plotly Express, Seaborn, Matplotlib
* **Machine Learning:** Scikit-Learn, XGBoost
* **Time-Series Analysis:** Meta Prophet
* **Web Interface:** Streamlit Framework

---

## 📊 Key Insights & Discoveries

* **The Economic Signal:** Proved a near-perfect **0.97 Pearson correlation coefficient** between a nation's Gross Domestic Product (GDP) and its real-world electricity grid demand, establishing economic productivity as a primary predictive feature.
* **Algorithm Tournament Champion:** The **XGBoost Regressor** outperformed Random Forest and baseline Linear Regression models, achieving the lowest absolute error (**15.18 TWh MAE**) on unseen future test window segments (2019–2024).
* **Nigeria 2030 Forecast:** Time-series projection models identify a robust, continuous upward grid demand trajectory for Nigeria, forecasting baseline electricity requirements to scale to **44.63 TWh by the year 2030**.
