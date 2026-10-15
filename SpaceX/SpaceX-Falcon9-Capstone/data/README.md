# SpaceX Falcon 9 Capstone: Data Directory Documentation

This directory contains both the raw data ingested from SpaceX APIs and web scraping, as well as the processed data ready for exploratory data analysis, SQL querying, and machine learning.

## Directory Structure

```text
data/
├── raw/
│   ├── dataset_part_1.csv      # Raw SpaceX Falcon 9 launch dataset (90 rows, 17 columns)
│   ├── spacex_web_scraped.csv  # Scraped Wikipedia Falcon 9 launch history table (321 rows)
│   └── api_metadata.json       # Metadata recording API endpoint, retrieval timestamp, and schema
├── processed/
│   ├── dataset_part_2.csv      # Cleaned dataset with target 'Class' and date features (90 rows, 19 columns)
│   ├── dataset_part_3.csv      # One-hot encoded feature matrix for scikit-learn models (90 rows, 81 columns)
│   └── spacex.db               # SQLite database containing the launches table for SQL analysis
└── README.md                   # This documentation file
```

## Data Dictionary (`dataset_part_2.csv`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `FlightNumber` | Integer | Chronological launch index (1 to 90) |
| `Date` | Datetime | Launch date (YYYY-MM-DD) |
| `BoosterVersion` | String | Booster version family (`Falcon 9`) |
| `PayloadMass` | Float | Payload mass carried to orbit in kilograms (kg) |
| `Orbit` | String | Target orbit trajectory (e.g., LEO, ISS, GTO, VLEO, PO, SSO) |
| `LaunchSite` | String | Launch complex (CCAFS SLC 40, KSC LC 39A, VAFB SLC 4E) |
| `Outcome` | String | Raw landing outcome (e.g., `True ASDS`, `False ASDS`, `None None`) |
| `Flights` | Integer | Total number of flights executed by this specific booster core |
| `GridFins` | Boolean/Int | Whether aerodynamic titanium grid fins were equipped (1=True, 0=False) |
| `Reused` | Boolean/Int | Whether the core was previously flown (1=True, 0=False) |
| `Legs` | Boolean/Int | Whether landing legs were equipped (1=True, 0=False) |
| `LandingPad` | String | Identification code of ground pad or autonomous spaceport drone ship |
| `Block` | Integer | Rocket block version number (1 to 5) |
| `ReusedCount` | Integer | Number of times this booster core has been reused |
| `Serial` | String | Booster core serial identifier (e.g., `B1049`, `B1051`) |
| `Longitude` | Float | Launch site geographic longitude |
| `Latitude` | Float | Launch site geographic latitude |
| `Year` | Integer | Extracted launch year (2010 to 2020) |
| `Class` | Integer | Binary target variable: 1 for successful landing, 0 for failure/expenditure |

## Ground Truth Landing Success Distribution

- **Total Missions:** 90
- **Successful Landings (`Class = 1`):** 60 (66.7%)
- **Unsuccessful / Expended (`Class = 0`):** 30 (33.3%)
