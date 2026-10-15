# SpaceX Falcon 9 Capstone: Troubleshooting & FAQs

This document addresses common errors, system warnings, and setup challenges encountered when executing this project.

---

## 1. Remote API Timeouts & Rate Limits

### Symptom:
```text
HTTPSConnectionPool(host='api.spacexdata.com', port=443): Read timed out. (read timeout=15)
```
### Why It Occurs:
The community-hosted SpaceX REST API v4 occasionally experiences server congestion or rate limiting.
### Built-in Solution:
Our `src/data_collection.py` script and `01_data_collection_api.ipynb` notebook include an automated fallback mechanism. If the live SpaceX API does not respond within the timeout threshold, the script gracefully downloads the verified IBM Capstone benchmark dataset snapshot (`dataset_part_1.csv`). The pipeline will never crash or fail due to external API hiccups.

---

## 2. Port Already in Use (Dash Dashboard)

### Symptom:
```text
OSError: [Errno 98] Address already in use: ('127.0.0.1', 8050)
```
### Solution:
Another process is already running on port `8050`. You can:
1. Specify an alternative port when launching `dashboard/app.py`:
   ```python
   app.run(debug=False, port=8055)
   ```
2. Or terminate the existing Python process holding the port on Windows:
   ```powershell
   Get-Process python | Stop-Process -Force
   ```

---

## 3. CartoDB Tiles API Key Warning (Folium)

### Symptom:
```text
UserWarning: CartoDB tiles now require an API key. Please provide one to continue using the tiles.
```
### Solution:
Modern versions of Folium require an API key for CartoDB tiles. In `src/generate_map.py` and `06_folium_launch_map.ipynb`, we use the open-source `tiles="OpenStreetMap"`, which requires no API key and renders without warnings.

---

## 4. SQLite Database Locks

### Symptom:
```text
sqlite3.OperationalError: database is locked
```
### Solution:
This happens if multiple scripts or Jupyter notebook kernels attempt to write to `data/spacex.db` concurrently.
- Restart the Jupyter kernel by selecting **Kernel -> Restart**.
- Ensure Python scripts use context managers or close connections explicitly (`conn.close()`).

---

## 5. Scikit-Learn Version Compatibility Warnings

### Symptom:
```text
FutureWarning: The default value of `n_init` will change from 10 to 'auto' in 1.4...
```
### Solution:
These are harmless deprecation warnings. All models in `src/train_model.py` explicitly pin random seeds and pass hyperparameter grids compatible with both scikit-learn 1.2+ and 1.7+.

---

## 6. How to Verify That All Outputs Exist

Run the following quick validation check in PowerShell:
```powershell
# Check raw and processed data
Test-Path data\raw\dataset_part_1.csv
Test-Path data\processed\dataset_part_2.csv
Test-Path data\processed\dataset_part_3.csv
Test-Path data\spacex.db

# Check visuals
Test-Path visuals\eda\01_launches_over_time.png
Test-Path visuals\folium\launch_sites_map.html
Test-Path visuals\dashboard\dashboard_screenshot.png
Test-Path visuals\model\best_model.pkl

# Check presentation files
Test-Path presentation\spacex_capstone.pptx
Test-Path presentation\spacex_capstone.pdf
Test-Path presentation\speaker_notes.md
```
All checks should return `True`.
