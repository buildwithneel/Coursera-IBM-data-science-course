# SpaceX Falcon 9 Capstone: Project Architecture & Technical Design

This document details the software architecture, data pipelines, module interactions, and directory layout of the **SpaceX Falcon 9 First Stage Landing Prediction** system.

---

## 1. System Architecture Diagram

```mermaid
graph TD
    subgraph Ingestion["1. Data Ingestion Layer"]
        A1[SpaceX REST API v4\napi.spacexdata.com] -->|JSON Response| B1[parse_api_launches]
        A2[Wikipedia Historical Tables\nBeautifulSoup4 Scraper] -->|HTML Parsing| B2[spacex_web_scraped.csv]
        A3[IBM Capstone Benchmark Mirror] -->|Fail-Safe Cache| B1
        B1 --> C1[(data/raw/dataset_part_1.csv)]
    end

    subgraph Wrangling["2. Data Wrangling & Feature Engineering"]
        C1 --> D1[Missing Value Imputer\nMean Payload Imputation]
        D1 --> D2[Target Constructor\nClass: 1=Success, 0=Failure]
        D2 --> E1[(data/processed/dataset_part_2.csv)]
        D2 --> D3[One-Hot Encoder\npd.get_dummies 80 Features]
        D3 --> E2[(data/processed/dataset_part_3.csv)]
    end

    subgraph Analytics["3. Analytical Engines"]
        E1 --> F1[EDA Visualizer\nMatplotlib & Seaborn]
        F1 --> G1[visuals/eda/ 10 Figures]
        E1 --> F2[SQLite Engine\nSPACEXTBL]
        F2 --> G2[(data/spacex.db)]
        F2 --> G3[results/sql_results.md]
        E1 --> F3[Geospatial Engine\nFolium & Haversine Distance]
        F3 --> G4[visuals/folium/launch_sites_map.html]
        E1 --> F4[Interactive Web Dashboard\nPlotly Dash localhost:8050]
        F4 --> G5[visuals/dashboard/dashboard_screenshot.png]
    end

    subgraph Modeling["4. Predictive Machine Learning"]
        E2 --> H1[Stratified Train/Test Split\n80% Train, 20% Test, Seed=42]
        H1 --> H2[StandardScaler\nFit on Train Only - No Leakage]
        H2 --> H3[GridSearchCV\n10-Fold Stratified Cross-Validation]
        H3 --> I1[Logistic Regression]
        H3 --> I2[Support Vector Machine]
        H3 --> I3[Decision Tree Classifier]
        H3 --> I4[K-Nearest Neighbors]
        I1 & I2 & I3 & I4 --> J1[Held-Out Test Set Evaluation]
        J1 --> K1[visuals/model/model_comparison.png]
        J1 --> K2[visuals/model/confusion_matrices.png]
        J1 --> K3[visuals/model/feature_importance.png]
        J1 --> K4[(visuals/model/best_model.pkl)]
        J1 --> K5[results/model_evaluation.md]
    end

    subgraph Presentation["5. Deliverables & Presentation Layer"]
        G1 & G3 & G4 & G5 & K1 & K2 & K3 & K5 --> L1[presentation/spacex_capstone.pptx]
        G1 & G3 & G4 & G5 & K1 & K2 & K3 & K5 --> L2[presentation/spacex_capstone.pdf]
        L1 & L2 --> L3[presentation/speaker_notes.md]
    end
```

---

## 2. Directory Hierarchy

```text
SpaceX-Falcon9-Capstone/
│
├── README.md                           # Master GitHub documentation with badges and instructions
├── requirements.txt                    # Pinned library dependencies
├── .gitignore                          # Git exclude rules for cache, virtualenvs, and temp files
│
├── data/
│   ├── raw/
│   │   ├── dataset_part_1.csv          # Raw Falcon 9 launch dataset (90 rows, 17 columns)
│   │   ├── spacex_web_scraped.csv      # Wikipedia scraped launch records (321 rows)
│   │   └── api_metadata.json           # API retrieval timestamp, URL, and record metadata
│   ├── processed/
│   │   ├── dataset_part_2.csv          # Cleaned dataset with target 'Class' (90 rows, 19 columns)
│   │   └── dataset_part_3.csv          # One-hot encoded ML matrix (90 rows, 81 columns)
│   ├── spacex.db                       # Local SQLite relational database (table: SPACEXTBL)
│   └── README.md                       # Data dictionary and schema specifications
│
├── notebooks/
│   ├── 01_data_collection_api.ipynb    # API fetching, JSON unpacking, and error handling
│   ├── 02_web_scraping.ipynb           # BeautifulSoup table extraction from Wikipedia
│   ├── 03_data_wrangling.ipynb         # Missing value imputation and target engineering
│   ├── 04_eda_visualizations.ipynb     # Exploratory visualization cells and findings
│   ├── 05_sql_analysis.ipynb           # SQLite queries, aggregation, and interpretations
│   ├── 06_folium_launch_map.ipynb      # Interactive geographic map and distance calculation
│   └── 07_machine_learning.ipynb       # 4 classification algorithms, 10-fold CV, and evaluation
│
├── src/
│   ├── data_collection.py              # Ingests API data and web-scraped launch tables
│   ├── data_wrangling.py               # Imputes payload mass, creates Class, exports part 2 & 3
│   ├── eda.py                          # Renders 10 publication-quality charts in visuals/eda/
│   ├── run_sql.py                      # Creates SQLite DB, runs queries, writes results markdown
│   ├── generate_map.py                 # Constructs interactive HTML map with Folium
│   ├── generate_notebooks.py           # Programmatically builds all 7 Jupyter notebooks
│   ├── train_model.py                  # Trains, tunes, and evaluates scikit-learn models
│   └── create_presentation.py          # Builds PPTX, PDF, and speaker notes
│
├── sql/
│   └── queries.sql                     # All 12 executable SQL statements
│
├── dashboard/
│   └── app.py                          # Reactive Plotly Dash dashboard with callbacks
│
├── visuals/
│   ├── eda/                            # 10 High-resolution PNG figures (dpi=300)
│   ├── folium/                         # Interactive HTML map (launch_sites_map.html)
│   ├── dashboard/                      # Dashboard screenshot verified in headless browser
│   └── model/                          # Comparison charts, confusion matrices, serialized model
│
├── results/
│   ├── data_summary.md                 # Data wrangling summary and class distribution
│   ├── sql_results.md                  # Comprehensive SQL query results and teaching concepts
│   └── model_evaluation.md             # Model evaluation report with CV and test metrics
│
├── presentation/
│   ├── spacex_capstone.pptx            # 16-slide high-end aerospace presentation
│   ├── spacex_capstone.pdf             # Matching 16-page PDF document
│   └── speaker_notes.md                # Word-for-word speaker script for all 16 slides
│
└── docs/
    ├── beginner_guide.md               # Step-by-step beginner guide and concepts
    ├── project_architecture.md         # This technical architecture document
    ├── code_explanations.md            # Deep dive into source code modules
    └── troubleshooting.md              # Solutions for common execution errors
```
