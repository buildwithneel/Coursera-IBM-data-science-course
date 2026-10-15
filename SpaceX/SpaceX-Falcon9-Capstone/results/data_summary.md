# SpaceX Falcon 9 Dataset Summary & Data Wrangling Report

## 1. Dataset Dimensions
- **Raw Dataset Size:** 90 rows, 17 columns
- **Processed Dataset Size (`dataset_part_2.csv`):** 90 rows, 19 columns
- **One-Hot Encoded ML Matrix (`dataset_part_3.csv`):** 90 rows, 81 columns (including target `Class`)
- **Cleaning Strategy:** Handled missing `PayloadMass` values via mean imputation (6104.96 kg). Zero rows were removed to preserve historical launch sequences.

## 2. Target Variable Definition (`Class`)
- **Definition:** First-stage landing success indicator.
  - `Class = 1` (Success): Successful recovery on Drone Ship (`True ASDS`), Ground Pad (`True RTLS`), or Ocean Water (`True Ocean`).
  - `Class = 0` (Failure / Uncontrolled): Unsuccessful attempt (`False ASDS`, `False RTLS`, `False Ocean`) or no landing attempt / destroyed (`None None`, `None ASDS`).
- **Total Successful Landings:** 60 / 90 (66.7%)
- **Total Unsuccessful Launches:** 30 / 90 (33.3%)

## 3. Landing Outcomes Breakdown
| Landing Outcome Type | Description | Count | Class Assignment |
| :--- | :--- | :--- | :--- |
| `True ASDS` | Stage 1 landing result | 41 | `1` |
| `None None` | Stage 1 landing result | 19 | `0` |
| `True RTLS` | Stage 1 landing result | 14 | `1` |
| `False ASDS` | Stage 1 landing result | 6 | `0` |
| `True Ocean` | Stage 1 landing result | 5 | `1` |
| `False Ocean` | Stage 1 landing result | 2 | `0` |
| `None ASDS` | Stage 1 landing result | 2 | `0` |
| `False RTLS` | Stage 1 landing result | 1 | `0` |

## 4. Launch Site Statistics & Success Rates
| Launch Site | Total Launches | Successful Landings | Success Rate |
| :--- | :--- | :--- | :--- |
| **CCAFS SLC 40** | 55 | 33 | 60.0% |
| **KSC LC 39A** | 22 | 17 | 77.3% |
| **VAFB SLC 4E** | 13 | 10 | 76.9% |

## 5. Orbit Distribution
| Orbit Target | Number of Missions |
| :--- | :--- |
| **GTO** | 27 |
| **ISS** | 21 |
| **VLEO** | 14 |
| **PO** | 9 |
| **LEO** | 7 |
| **SSO** | 5 |
| **MEO** | 3 |
| **ES-L1** | 1 |
| **HEO** | 1 |
| **SO** | 1 |
| **GEO** | 1 |

## 6. Payload Statistics (kg)
- **Minimum Payload:** 350.0 kg
- **Average Payload:** 6105.0 kg
- **Maximum Payload:** 15600.0 kg
- **Standard Deviation:** 4694.7 kg

## 7. Machine Learning Features (`dataset_part_3.csv`)
- Total binary and numerical features: **80**
- Features include: Flight number, normalized payload mass, booster reuse flags, leg deployment, grid fins, and one-hot encoded categories for `Orbit`, `LaunchSite`, `LandingPad`, and core `Serial`.
