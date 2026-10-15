# SpaceX Falcon 9 Capstone: Comprehensive Code Explanations

This document provides a line-by-line and function-by-function technical breakdown of every Python script and module in the project.

---

## 1. `src/data_collection.py`

### Key Responsibilities:
- Fetching historical rocket data from the public SpaceX REST API v4 (`https://api.spacexdata.com/v4/launches/past`).
- Implementing a timeout mechanism with graceful fallback to IBM's verified historical benchmark snapshot (`dataset_part_1.csv`).
- Scraping Wikipedia's historical Falcon 9 and Falcon Heavy launch tables via BeautifulSoup.

### Critical Functions:
- `fetch_spacex_api(timeout=15)`:
  - Issues an HTTP GET request with a custom `User-Agent`.
  - Parses the JSON response using `json.loads` or `response.json()`.
  - Saves raw data into `data/raw/spacex_api_raw.json`.
  - If a connection timeout or rate limit occurs, logs a warning and downloads the verified benchmark dataset from IBM Cloud Object Storage.
- `parse_api_launches(data)`:
  - Uses `pd.json_normalize` to flatten nested JSON fields.
  - Filters rows where `rocket == "5e9d0d95eda69973a6998c70"` (the unique ID for the Falcon 9 launch vehicle).
  - Unpacks the `cores` array to extract landing parameters (`landing_type`, `landing_success`, `reused_count`, `core` serial).
- `scrape_wikipedia_launches()`:
  - Queries `https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches`.
  - Parses HTML tables having class `wikitable`.
  - Loops through each `<tr>` element, filters flight number digits in the first column, and extracts launch site, payload mass, orbit, and mission outcome.

---

## 2. `src/data_wrangling.py`

### Key Responsibilities:
- Inspecting data dimensions, null counts, and column types.
- Imputing missing values in `PayloadMass` using the arithmetic mean.
- Defining and creating the binary target variable `Class`.
- One-hot encoding categorical variables for machine learning.

### Critical Logic:
```python
# Target Variable Construction Logic
landing_class = []
for outcome in df["Outcome"]:
    if isinstance(outcome, str) and outcome.startswith("True"):
        landing_class.append(1)  # Successful landing (ASDS, RTLS, Ocean)
    else:
        landing_class.append(0)  # Failure, crash, or expended
df["Class"] = landing_class
```
- **Why this logic?** In Falcon 9 operations, any landing labeled `True ASDS` (Autonomous Spaceport Drone Ship), `True RTLS` (Return to Launch Site ground pad), or `True Ocean` represents a soft touchdown where the booster survived or demonstrated controlled descent. Unsuccessful landings (`False ASDS`, `False RTLS`, `False Ocean`, `None None`, `None ASDS`) mean the booster crashed or was deliberately expended without recovery hardware.
- `features_one_hot = pd.get_dummies(features, columns=["Orbit", "LaunchSite", "LandingPad", "Serial"], drop_first=False)`:
  Converts categorical strings into binary indicator columns ($0$ or $1$) so linear and distance-based algorithms can compute dot products and Euclidean distances.

---

## 3. `src/eda.py`

### Key Responsibilities:
- Generates 10 distinct, publication-grade figures saved to `visuals/eda/`.
- Configures custom styling (`seaborn-v0_8-whitegrid`, high-contrast aerospace palette).

### Highlighted Plots:
1. `plot_launches_over_time()`: Renders yearly bar chart showing launch volume acceleration from 2010 to 2020.
2. `plot_launches_by_site()`: Displays launch frequency per complex, annotating total volume and percentages.
3. `plot_overall_landing_success()`: Donut/pie chart illustrating the 66.7% vs 33.3% landing outcome split.
4. `plot_flight_number_vs_launch_site()`: Seaborn scatter plot colored by landing outcome (`hue="Class"`).
5. `plot_payload_mass_vs_launch_site()`: Scatter plot examining payload capacity limits across Florida and California sites.
6. `plot_success_rate_by_orbit()`: Horizontal/vertical bar chart color-coded by recovery difficulty.
7. `plot_yearly_success_trend()`: Line chart showing the rising empirical learning curve over time.
8. `plot_correlation_heatmap()`: Pearson correlation matrix of numeric telemetry features.

---

## 4. `src/run_sql.py`

### Key Responsibilities:
- Establishes a local SQLite database (`data/spacex.db`).
- Inserts `dataset_part_2.csv` into table `SPACEXTBL`.
- Executes 12 analytical queries answering all IBM Capstone rubric questions.
- Exports `sql/queries.sql` and generates markdown report `results/sql_results.md`.

### Highlighted Query Implementations:
- **Unique Sites:** `SELECT DISTINCT LaunchSite FROM SPACEXTBL;`
- **Pattern Matching:** `SELECT * FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' LIMIT 5;`
- **Group Aggregations:** `SELECT LaunchSite, SUM(PayloadMass) AS TotalPayload FROM SPACEXTBL GROUP BY LaunchSite;`
- **Chronological Milestones:** `SELECT MIN(Date) FROM SPACEXTBL WHERE Outcome = 'True RTLS';`
- **Subqueries for Extremes:** `SELECT * FROM SPACEXTBL WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXTBL);`

---

## 5. `src/generate_map.py`

### Key Responsibilities:
- Constructs an interactive Leaflet-powered HTML map using `folium`.
- Adds launchpad markers, circular safety perimeters, and landing outcome clusters (`MarkerCluster`).
- Implements the Haversine formula to compute geodesic distances between coordinates.

### Haversine Formula Breakdown:
$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$
- $R = 6373.0\text{ km}$ (Earth radius).
- Converts latitude ($\phi$) and longitude ($\lambda$) from degrees to radians.
- Connects launchpads to coastlines, railways, highways, and cities using dashed and solid `folium.PolyLine` markers.

---

## 6. `dashboard/app.py`

### Key Responsibilities:
- Real-time interactive operations dashboard built with Plotly Dash.
- Layout defined with `html.Div`, `dcc.Dropdown`, `dcc.RangeSlider`, and `dcc.Graph`.
- Multi-input reactive Dash callback:
```python
@app.callback(
    [
        Output("kpi-container", "children"),
        Output("success-pie-chart", "figure"),
        Output("success-payload-scatter-chart", "figure"),
        Output("yearly-trend-chart", "figure")
    ],
    [
        Input("site-dropdown", "value"),
        Input("outcome-radio", "value"),
        Input("payload-slider", "value")
    ]
)
def update_dashboard(selected_site, selected_outcome, payload_range):
    # Filters dataframe dynamically and recalculates KPIs and Figures
```

---

## 7. `src/train_model.py`

### Key Responsibilities:
- Preprocessing and train/test partition without data leakage.
- Hyperparameter tuning using 10-Fold Stratified Cross-Validation (`GridSearchCV`).
- Training Logistic Regression, SVM, Decision Tree, and K-Nearest Neighbors.
- Computing accuracy, precision, recall, F1, ROC-AUC, and confusion matrices.
- Exporting serialized model `best_model.pkl` and documentation `results/model_evaluation.md`.

### Leakage Prevention Guarantee:
```python
# Split first!
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42, stratify=Y)

# Fit scaler strictly on training set!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Transform test set using train statistics
```
This ensures test set feature distributions (means and variances) are completely unobserved during training, guaranteeing authentic out-of-sample evaluation.
