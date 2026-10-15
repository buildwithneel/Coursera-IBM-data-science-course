"""
SpaceX Capstone: Data Wrangling Module
-------------------------------------
Performs:
1. Missing value identification and imputation (PayloadMass mean replacement).
2. Categorical landing outcome conversion to binary target variable `Class`:
   - 1 = Successful landing (True Ocean, True RTLS, True ASDS)
   - 0 = Unsuccessful / No landing attempt (False Ocean, False RTLS, False ASDS, None None, None ASDS)
3. Date parsing and feature extraction (Year).
4. One-hot encoding of categorical variables for machine learning (dataset_part_3).
5. Dataset summary generation for validation and documentation.
"""

import os
import json
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "dataset_part_1.csv")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
PART_2_PATH = os.path.join(PROCESSED_DIR, "dataset_part_2.csv")
PART_3_PATH = os.path.join(PROCESSED_DIR, "dataset_part_3.csv")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def wrangle_spacex_data():
    """Load raw data, clean, impute, create target variable, and export processed datasets."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    logging.info(f"Loading raw dataset from {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    raw_shape = df.shape
    logging.info(f"Raw dataset shape: {raw_shape[0]} rows, {raw_shape[1]} columns")

    # 1. Missing Values Analysis
    missing_before = df.isnull().sum()
    logging.info(f"Missing values before imputation:\n{missing_before[missing_before > 0]}")

    # Impute missing PayloadMass with mean value
    if "PayloadMass" in df.columns and df["PayloadMass"].isnull().sum() > 0:
        mean_payload = df["PayloadMass"].mean()
        df["PayloadMass"] = df["PayloadMass"].fillna(mean_payload)
        logging.info(f"Imputed missing PayloadMass with mean: {mean_payload:.2f} kg")

    # 2. Date handling and Year extraction
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year

    # 3. Target Variable Construction (`Class`)
    # Inspect Outcome column
    outcomes = df["Outcome"].value_counts()
    logging.info(f"Unique landing outcomes breakdown:\n{outcomes}")

    # Successful landing outcomes start with 'True'
    # Unsuccessful landing outcomes start with 'False' or 'None'
    landing_class = []
    for outcome in df["Outcome"]:
        if isinstance(outcome, str) and outcome.startswith("True"):
            landing_class.append(1)
        else:
            landing_class.append(0)

    df["Class"] = landing_class
    success_rate = df["Class"].mean()
    logging.info(f"Target variable `Class` created. Overall Landing Success Rate: {success_rate:.2%}")

    # Save processed dataset part 2
    df.to_csv(PART_2_PATH, index=False)
    logging.info(f"Saved wrangled dataset to {PART_2_PATH} with {df.shape[0]} rows, {df.shape[1]} columns")

    # 4. Feature Selection & One-Hot Encoding for ML (dataset_part_3)
    features = df[[
        "FlightNumber", "PayloadMass", "Orbit", "LaunchSite",
        "Flights", "GridFins", "Reused", "Legs", "LandingPad", "Block", "ReusedCount", "Serial"
    ]].copy()

    # Cast boolean columns to numeric/int
    features["GridFins"] = features["GridFins"].astype(int)
    features["Reused"] = features["Reused"].astype(int)
    features["Legs"] = features["Legs"].astype(int)

    # One-hot encode categorical features: Orbit, LaunchSite, LandingPad, Serial
    categorical_cols = ["Orbit", "LaunchSite", "LandingPad", "Serial"]
    features_one_hot = pd.get_dummies(features, columns=categorical_cols, drop_first=False)
    # Convert all columns to float/int
    features_one_hot = features_one_hot.astype(float)

    # Attach Class target column to part 3 for complete modeling convenience
    df_part_3 = pd.concat([features_one_hot, df["Class"]], axis=1)
    df_part_3.to_csv(PART_3_PATH, index=False)
    logging.info(f"Saved one-hot encoded dataset to {PART_3_PATH} with {df_part_3.shape[0]} rows, {df_part_3.shape[1]} columns")

    # 5. Generate data summary documentation
    generate_data_summary(df, raw_shape, df.shape, df_part_3.shape)

    return df, df_part_3


def generate_data_summary(df, raw_shape, processed_shape, one_hot_shape):
    """Write markdown summary of data wrangling outcomes."""
    summary_path = os.path.join(RESULTS_DIR, "data_summary.md")
    
    site_counts = df["LaunchSite"].value_counts().to_dict()
    orbit_counts = df["Orbit"].value_counts().to_dict()
    outcome_counts = df["Outcome"].value_counts().to_dict()
    success_by_site = df.groupby("LaunchSite")["Class"].mean().to_dict()
    
    summary_text = f"""# SpaceX Falcon 9 Dataset Summary & Data Wrangling Report

## 1. Dataset Dimensions
- **Raw Dataset Size:** {raw_shape[0]} rows, {raw_shape[1]} columns
- **Processed Dataset Size (`dataset_part_2.csv`):** {processed_shape[0]} rows, {processed_shape[1]} columns
- **One-Hot Encoded ML Matrix (`dataset_part_3.csv`):** {one_hot_shape[0]} rows, {one_hot_shape[1]} columns (including target `Class`)
- **Cleaning Strategy:** Handled missing `PayloadMass` values via mean imputation ({df['PayloadMass'].mean():.2f} kg). Zero rows were removed to preserve historical launch sequences.

## 2. Target Variable Definition (`Class`)
- **Definition:** First-stage landing success indicator.
  - `Class = 1` (Success): Successful recovery on Drone Ship (`True ASDS`), Ground Pad (`True RTLS`), or Ocean Water (`True Ocean`).
  - `Class = 0` (Failure / Uncontrolled): Unsuccessful attempt (`False ASDS`, `False RTLS`, `False Ocean`) or no landing attempt / destroyed (`None None`, `None ASDS`).
- **Total Successful Landings:** {int(df['Class'].sum())} / {len(df)} ({df['Class'].mean():.1%})
- **Total Unsuccessful Launches:** {int((1 - df['Class']).sum())} / {len(df)} ({(1 - df['Class'].mean()):.1%})

## 3. Landing Outcomes Breakdown
| Landing Outcome Type | Description | Count | Class Assignment |
| :--- | :--- | :--- | :--- |
"""
    for outcome, count in outcome_counts.items():
        assigned = 1 if outcome.startswith("True") else 0
        summary_text += f"| `{outcome}` | Stage 1 landing result | {count} | `{assigned}` |\n"

    summary_text += f"""
## 4. Launch Site Statistics & Success Rates
| Launch Site | Total Launches | Successful Landings | Success Rate |
| :--- | :--- | :--- | :--- |
"""
    for site, total in site_counts.items():
        rate = success_by_site.get(site, 0)
        success_count = int(round(rate * total))
        summary_text += f"| **{site}** | {total} | {success_count} | {rate:.1%} |\n"

    summary_text += f"""
## 5. Orbit Distribution
| Orbit Target | Number of Missions |
| :--- | :--- |
"""
    for orbit, count in orbit_counts.items():
        summary_text += f"| **{orbit}** | {count} |\n"

    summary_text += f"""
## 6. Payload Statistics (kg)
- **Minimum Payload:** {df['PayloadMass'].min():.1f} kg
- **Average Payload:** {df['PayloadMass'].mean():.1f} kg
- **Maximum Payload:** {df['PayloadMass'].max():.1f} kg
- **Standard Deviation:** {df['PayloadMass'].std():.1f} kg

## 7. Machine Learning Features (`dataset_part_3.csv`)
- Total binary and numerical features: **{one_hot_shape[1] - 1}**
- Features include: Flight number, normalized payload mass, booster reuse flags, leg deployment, grid fins, and one-hot encoded categories for `Orbit`, `LaunchSite`, `LandingPad`, and core `Serial`.
"""
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    logging.info(f"Generated comprehensive data summary at {summary_path}")


if __name__ == "__main__":
    print("=== Phase 2: Running Data Wrangling ===")
    df_clean, df_ml = wrangle_spacex_data()
    print(f"Data Wrangling complete: {df_clean.shape[0]} rows ready for EDA, SQL, and ML modeling.")
