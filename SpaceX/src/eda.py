"""
SpaceX Capstone: Exploratory Data Analysis (EDA) Module
------------------------------------------------------
Generates high-resolution visualization figures and empirical findings for:
1. Launch trends over time (Yearly cadence).
2. Launch site distribution and comparative landing success rates.
3. Payload mass distributions and relationship with landing success.
4. Orbit target distributions and success rates by orbit.
5. Flight number progression vs landing success.
6. Feature correlation matrix for numerical parameters.
"""

import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "dataset_part_2.csv")
VISUALS_DIR = os.path.join(os.path.dirname(__file__), "..", "visuals", "eda")

# Styling configurations for aerospace presentation theme
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
PALETTE = {0: "#D32F2F", 1: "#1976D2"}  # Red for failure, Blue for success
SITE_COLORS = ["#1A237E", "#0288D1", "#00897B"]


def ensure_visuals_dir():
    os.makedirs(VISUALS_DIR, exist_ok=True)


def plot_launches_over_time(df):
    """Figure 1: Yearly Launch Volume & Cumulative Launches."""
    plt.figure(figsize=(10, 5), dpi=300)
    yearly = df.groupby("Year").size().reset_index(name="Launches")
    bars = plt.bar(yearly["Year"], yearly["Launches"], color="#0D47A1", edgecolor="#0A2540", width=0.6, alpha=0.9)
    plt.title("SpaceX Falcon 9 Launch Volume Over Time (2010 - 2020)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Launch Year", fontsize=12, labelpad=10)
    plt.ylabel("Number of Launches", fontsize=12, labelpad=10)
    plt.xticks(yearly["Year"], fontsize=10)
    plt.ylim(0, yearly["Launches"].max() + 3)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, int(yval), ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "01_launches_over_time.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_launches_by_site(df):
    """Figure 2: Total Launches by Launch Site."""
    plt.figure(figsize=(9, 5), dpi=300)
    site_counts = df["LaunchSite"].value_counts().reset_index()
    site_counts.columns = ["LaunchSite", "Count"]
    
    bars = plt.bar(site_counts["LaunchSite"], site_counts["Count"], color=["#1A237E", "#00838F", "#FF6F00"], width=0.55)
    plt.title("Falcon 9 Launch Frequency by Launch Complex", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Launch Site", fontsize=12, labelpad=10)
    plt.ylabel("Total Launches", fontsize=12, labelpad=10)
    plt.ylim(0, site_counts["Count"].max() + 6)
    
    for bar in bars:
        yval = bar.get_height()
        pct = (yval / len(df)) * 100
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{int(yval)} ({pct:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "02_launches_by_site.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_overall_landing_success(df):
    """Figure 3: Overall Landing Success Distribution."""
    plt.figure(figsize=(7, 7), dpi=300)
    counts = df["Class"].value_counts()
    labels = ["Successful Landing (Class 1)", "Unsuccessful / Expended (Class 0)"]
    colors = ["#1976D2", "#D32F2F"]
    explode = (0.05, 0)
    
    plt.pie(
        [counts[1], counts[0]],
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        explode=explode,
        textprops={"fontsize": 12, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    plt.title("SpaceX Falcon 9 First Stage Landing Success Proportion", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "03_overall_landing_success_rate.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_flight_number_vs_launch_site(df):
    """Figure 4: Flight Number vs Launch Site with Landing Outcome."""
    plt.figure(figsize=(11, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="LaunchSite",
        hue="Class",
        palette=PALETTE,
        s=120,
        alpha=0.85,
        edgecolor="black",
        linewidth=0.8
    )
    plt.title("Flight Number vs Launch Site by Landing Outcome", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Flight Number (Chronological Progression)", fontsize=12, labelpad=10)
    plt.ylabel("Launch Site", fontsize=12, labelpad=10)
    plt.legend(title="Landing Outcome", labels=["Unsuccessful (0)", "Successful (1)"], loc="lower right", frameon=True)
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "04_flight_number_vs_launch_site.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_payload_mass_vs_launch_site(df):
    """Figure 5: Payload Mass vs Launch Site by Landing Outcome."""
    plt.figure(figsize=(11, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="LaunchSite",
        hue="Class",
        palette=PALETTE,
        s=120,
        alpha=0.85,
        edgecolor="black",
        linewidth=0.8
    )
    plt.title("Payload Mass (kg) vs Launch Site by Landing Outcome", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Payload Mass (kg)", fontsize=12, labelpad=10)
    plt.ylabel("Launch Site", fontsize=12, labelpad=10)
    plt.legend(title="Landing Outcome", labels=["Unsuccessful (0)", "Successful (1)"], loc="lower right", frameon=True)
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "05_payload_mass_vs_launch_site.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_success_rate_by_orbit(df):
    """Figure 6: Success Rate by Orbit Type."""
    plt.figure(figsize=(11, 6), dpi=300)
    orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
    orbit_success = orbit_success.sort_values(by="Class", ascending=False)
    
    colors = ["#2E7D32" if val >= 0.7 else "#F57C00" if val >= 0.5 else "#C62828" for val in orbit_success["Class"]]
    bars = plt.bar(orbit_success["Orbit"], orbit_success["Class"] * 100, color=colors, width=0.6, edgecolor="#333333")
    
    plt.title("Landing Success Rate (%) by Orbit Destination", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Target Orbit", fontsize=12, labelpad=10)
    plt.ylabel("Success Rate (%)", fontsize=12, labelpad=10)
    plt.ylim(0, 115)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "06_success_rate_by_orbit.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_flight_number_vs_orbit(df):
    """Figure 7: Flight Number vs Orbit Destination."""
    plt.figure(figsize=(11, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="Orbit",
        hue="Class",
        palette=PALETTE,
        s=110,
        alpha=0.85,
        edgecolor="black"
    )
    plt.title("Flight Number vs Orbit Type by Landing Outcome", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Flight Number", fontsize=12, labelpad=10)
    plt.ylabel("Orbit Type", fontsize=12, labelpad=10)
    plt.legend(title="Landing Outcome", labels=["Unsuccessful (0)", "Successful (1)"], loc="lower right")
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "07_flight_number_vs_orbit.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_payload_mass_vs_orbit(df):
    """Figure 8: Payload Mass vs Orbit Destination."""
    plt.figure(figsize=(11, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="Orbit",
        hue="Class",
        palette=PALETTE,
        s=110,
        alpha=0.85,
        edgecolor="black"
    )
    plt.title("Payload Mass (kg) vs Orbit Destination by Landing Outcome", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Payload Mass (kg)", fontsize=12, labelpad=10)
    plt.ylabel("Orbit Type", fontsize=12, labelpad=10)
    plt.legend(title="Landing Outcome", labels=["Unsuccessful (0)", "Successful (1)"], loc="lower right")
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "08_payload_mass_vs_orbit.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_yearly_success_trend(df):
    """Figure 9: Yearly Success Rate Trend (Learning Curve)."""
    plt.figure(figsize=(10, 5), dpi=300)
    yearly_trend = df.groupby("Year")["Class"].mean().reset_index()
    
    plt.plot(yearly_trend["Year"], yearly_trend["Class"] * 100, marker="o", linewidth=3, markersize=8, color="#0D47A1", label="Success Rate (%)")
    plt.title("SpaceX Falcon 9 Landing Success Rate Evolution (2010 - 2020)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Year", fontsize=12, labelpad=10)
    plt.ylabel("Success Rate (%)", fontsize=12, labelpad=10)
    plt.xticks(yearly_trend["Year"], fontsize=10)
    plt.ylim(-5, 105)
    
    for _, row in yearly_trend.iterrows():
        plt.text(row["Year"], (row["Class"] * 100) + 3, f"{row['Class']*100:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "09_yearly_success_trend.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def plot_correlation_heatmap(df):
    """Figure 10: Numeric Feature Correlation Heatmap."""
    plt.figure(figsize=(9, 7), dpi=300)
    numeric_cols = ["FlightNumber", "PayloadMass", "Flights", "GridFins", "Reused", "Legs", "Block", "ReusedCount", "Class"]
    corr = df[numeric_cols].corr()
    
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={"label": "Pearson Correlation Coefficient"}
    )
    plt.title("Correlation Matrix of Falcon 9 Operational Features", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    out_path = os.path.join(VISUALS_DIR, "10_correlation_heatmap.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    logging.info(f"Saved: {out_path}")


def run_all_eda():
    ensure_visuals_dir()
    logging.info(f"Loading wrangled dataset from {PROCESSED_DATA_PATH}")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    plot_launches_over_time(df)
    plot_launches_by_site(df)
    plot_overall_landing_success(df)
    plot_flight_number_vs_launch_site(df)
    plot_payload_mass_vs_launch_site(df)
    plot_success_rate_by_orbit(df)
    plot_flight_number_vs_orbit(df)
    plot_payload_mass_vs_orbit(df)
    plot_yearly_success_trend(df)
    plot_correlation_heatmap(df)
    
    logging.info(f"All 10 EDA visualizations generated and saved in {VISUALS_DIR}")


if __name__ == "__main__":
    print("=== Phase 4: Generating All EDA Visualizations ===")
    run_all_eda()
    print("=== EDA Visualizations Successfully Generated ===")
