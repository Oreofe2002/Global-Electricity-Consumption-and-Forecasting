import os
import pandas as pd
import numpy as np

def run_data_ingestion_pipeline():
    print("🚀 Initializing Global Energy Project Data Pipeline...")
    
    # This points directly to the active master branch on the official OWID GitHub storage
    OWID_ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
    RAW_DATA_PATH = os.path.join("data", "raw", "owid_energy_raw.csv")
    PROCESSED_DATA_PATH = os.path.join("data", "processed", "energy_cleaned.csv")
    
    # Ensure local directory paths exist
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    print(f"📥 Downloading latest live dataset from Our World in Data GitHub...")
    try:
        # Fetching directly from github raw content server
        df_raw = pd.read_csv(OWID_ENERGY_URL)
        df_raw.to_csv(RAW_DATA_PATH, index=False)
        print(f"✅ Raw dataset successfully mirrored to: {RAW_DATA_PATH}")
    except Exception as e:
        print(f"❌ Failed to download dataset. Error details: {e}")
        return

    # Extract our specific data science schema columns
    keep_columns = [
        'country', 'year', 'iso_code', 'population', 'gdp',
        'primary_energy_consumption', 'energy_per_capita', 'energy_per_gdp',
        'electricity_demand', 'electricity_generation',
        'fossil_electricity', 'coal_electricity', 'gas_electricity', 'oil_electricity',
        'renewables_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity'
    ]
    
    available_cols = [col for col in keep_columns if col in df_raw.columns]
    df_filtered = df_raw[available_cols].copy()
    
    # Filter regional rows to leave clean country data rows
    print("🧹 Cleaning data: Filtering regional aggregates and handling missing structures...")
    df_filtered = df_filtered.dropna(subset=['country', 'year'])
    
    aggregates_to_remove = ['World', 'High-income countries', 'Low-income countries', 
                             'Upper-middle-income countries', 'Lower-middle-income countries',
                             'Europe', 'Asia', 'North America', 'South America', 'Africa', 'Oceania',
                             'European Union (27)', 'Asia Pacific', 'CIS']
    
    df_cleaned = df_filtered[~df_filtered['country'].isin(aggregates_to_remove)]
    
    if 'iso_code' in df_cleaned.columns:
        df_cleaned = df_cleaned[~df_cleaned['iso_code'].astype(str).str.startswith('OWID_')]
        df_cleaned = df_cleaned.dropna(subset=['iso_code'])

    # Save to processed data folder path
    print(f"💾 Saving processed dataset for local ML and EDA exploration...")
    df_cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
    
    print("\n🏁 Data Ingestion Step Completed Successfully!")
    print(f"📊 Processed Dimensions: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} features ready.")

if __name__ == "__main__":
    run_data_ingestion_pipeline()
