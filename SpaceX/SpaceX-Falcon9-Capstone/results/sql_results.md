# SpaceX Falcon 9 SQL Data Analysis & Business Intelligence Report

This report details SQL queries executed against the processed SpaceX dataset in SQLite (`data/spacex.db`).
Each section outlines the analytical question, the executable SQL syntax, the actual result set, SQL syntax teaching, and operational takeaways.

## Query 1: Unique Launch Sites
**Business / Analytical Question:** What are the unique launch sites used in SpaceX Falcon 9 missions?

```sql
SELECT DISTINCT LaunchSite FROM SPACEXTBL;
```

### Result Set:
| LaunchSite   |
|:-------------|
| CCAFS SLC 40 |
| VAFB SLC 4E  |
| KSC LC 39A   |

**Beginner SQL Concept:** The `DISTINCT` keyword eliminates duplicate values, returning each launch site exactly once.

**Analytical Interpretation:** SpaceX operates 3 primary launch complexes: CCAFS SLC 40 (Florida), KSC LC 39A (Florida), and VAFB SLC 4E (California).

---

## Query 2: First 5 Records with Cape Canaveral Launch Sites
**Business / Analytical Question:** Display 5 records where launch site begins with the prefix 'CCA'.

```sql
SELECT FlightNumber, Date, LaunchSite, BoosterVersion, PayloadMass FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' LIMIT 5;
```

### Result Set:
|   FlightNumber | Date       | LaunchSite   | BoosterVersion   |   PayloadMass |
|---------------:|:-----------|:-------------|:-----------------|--------------:|
|              1 | 2010-06-04 | CCAFS SLC 40 | Falcon 9         |       6104.96 |
|              2 | 2012-05-22 | CCAFS SLC 40 | Falcon 9         |        525    |
|              3 | 2013-03-01 | CCAFS SLC 40 | Falcon 9         |        677    |
|              5 | 2013-12-03 | CCAFS SLC 40 | Falcon 9         |       3170    |
|              6 | 2014-01-06 | CCAFS SLC 40 | Falcon 9         |       3325    |

**Beginner SQL Concept:** The `WHERE` clause filters rows using pattern matching (`LIKE 'CCA%'` matches any string beginning with 'CCA'). `LIMIT 5` restricts output to the first 5 rows.

**Analytical Interpretation:** Cape Canaveral Air Force Station (CCAFS SLC 40) hosted the earliest historical test flights and commercial launches.

---

## Query 3: Total Payload Mass by Launch Site
**Business / Analytical Question:** Calculate the total payload mass carried from each launch site.

```sql
SELECT LaunchSite, SUM(PayloadMass) AS TotalPayloadMass_KG, COUNT(*) AS TotalLaunches FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalPayloadMass_KG DESC;
```

### Result Set:
| LaunchSite   |   TotalPayloadMass_KG |   TotalLaunches |
|:-------------|----------------------:|----------------:|
| CCAFS SLC 40 |                305151 |              55 |
| KSC LC 39A   |                167342 |              22 |
| VAFB SLC 4E  |                 76953 |              13 |

**Beginner SQL Concept:** `GROUP BY` aggregates data by each launch site. `SUM()` adds up total kilograms lifted, and `ORDER BY DESC` sorts the heaviest total payload first.

**Analytical Interpretation:** CCAFS SLC 40 has delivered the highest cumulative payload mass (305,151.4 kg) across its 55 missions.

---

## Query 4: Average Payload Mass by Booster Version Category
**Business / Analytical Question:** What is the average payload mass across all Falcon 9 missions?

```sql
SELECT BoosterVersion, ROUND(AVG(PayloadMass), 2) AS AveragePayload_KG, MIN(PayloadMass) AS MinPayload_KG, MAX(PayloadMass) AS MaxPayload_KG FROM SPACEXTBL GROUP BY BoosterVersion;
```

### Result Set:
| BoosterVersion   |   AveragePayload_KG |   MinPayload_KG |   MaxPayload_KG |
|:-----------------|--------------------:|----------------:|----------------:|
| Falcon 9         |             6104.96 |             350 |           15600 |

**Beginner SQL Concept:** `AVG()`, `MIN()`, and `MAX()` provide statistical summaries. `ROUND(..., 2)` formats the floating point number to two decimal places.

**Analytical Interpretation:** Average Falcon 9 payload across 90 historical launches is approximately 6,105.0 kg, ranging from 350 kg up to 15,600 kg.

---

## Query 5: First Successful Ground Pad Landing Date
**Business / Analytical Question:** What is the date of the very first successful landing on a ground pad (RTLS)?

```sql
SELECT MIN(Date) AS FirstSuccessfulGroundLandingDate, FlightNumber, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True RTLS';
```

### Result Set:
| FirstSuccessfulGroundLandingDate   |   FlightNumber | LaunchSite   | Outcome   |
|:-----------------------------------|---------------:|:-------------|:----------|
| 2015-12-22                         |             17 | CCAFS SLC 40 | True RTLS |

**Beginner SQL Concept:** `WHERE Outcome = 'True RTLS'` filters specifically for Return-to-Launch-Site ground pad touchdowns. `MIN(Date)` extracts the earliest chronological date.

**Analytical Interpretation:** The first successful ground-pad landing (RTLS) occurred on 2015-12-22 during Flight #17 from CCAFS SLC 40, marking a watershed moment in reusable rocketry.

---

## Query 6: Drone Ship Successes with Intermediate Payload Mass (4,000 to 6,000 kg)
**Business / Analytical Question:** List booster serials and dates that successfully landed on a drone ship carrying payload between 4,000 kg and 6,000 kg.

```sql
SELECT FlightNumber, Date, Serial, PayloadMass, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True ASDS' AND PayloadMass BETWEEN 4000 AND 6000;
```

### Result Set:
|   FlightNumber | Date       | Serial   |   PayloadMass | LaunchSite   | Outcome   |
|---------------:|:-----------|:---------|--------------:|:-------------|:----------|
|             21 | 2016-05-06 | B1022    |          4696 | CCAFS SLC 40 | True ASDS |
|             24 | 2016-08-14 | B1026    |          4600 | CCAFS SLC 40 | True ASDS |
|             29 | 2017-03-30 | B1021    |          5300 | KSC LC 39A   | True ASDS |
|             40 | 2017-10-11 | B1031    |          5200 | KSC LC 39A   | True ASDS |
|             55 | 2018-08-07 | B1046    |          5800 | CCAFS SLC 40 | True ASDS |
|             59 | 2018-12-03 | B1046    |          4000 | VAFB SLC 4E  | True ASDS |
|             70 | 2019-12-05 | B1059    |          5000 | CCAFS SLC 40 | True ASDS |

**Beginner SQL Concept:** The `BETWEEN` operator specifies an inclusive numeric range. `AND` requires both drone ship landing success and the mass window to hold simultaneously.

**Analytical Interpretation:** Identified 7 missions in the 4,000–6,000 kg window successfully recovered on Autonomous Spaceport Drone Ships (ASDS).

---

## Query 7: Mission Outcome Breakdown (Success vs Failure Counts)
**Business / Analytical Question:** What is the total count of successful first stage landings versus failed/expended attempts?

```sql
SELECT CASE WHEN Class = 1 THEN 'Successful Landing' ELSE 'Failure / Uncontrolled' END AS LandingStatus, COUNT(*) AS TotalCount, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM SPACEXTBL), 2) AS Percentage FROM SPACEXTBL GROUP BY Class ORDER BY TotalCount DESC;
```

### Result Set:
| LandingStatus          |   TotalCount |   Percentage |
|:-----------------------|-------------:|-------------:|
| Successful Landing     |           60 |        66.67 |
| Failure / Uncontrolled |           30 |        33.33 |

**Beginner SQL Concept:** `CASE WHEN` creates conditional labels for binary values. A scalar subquery `(SELECT COUNT(*) FROM SPACEXTBL)` computes total records dynamically to evaluate percentages.

**Analytical Interpretation:** First stage landing success stands at 66.67% (60 successful recoveries out of 90 attempts), demonstrating high technical maturity.

---

## Query 8: Booster Carrying Maximum Payload Mass
**Business / Analytical Question:** Which booster core(s) and flight numbers carried the maximum recorded payload mass?

```sql
SELECT FlightNumber, Date, Serial, LaunchSite, PayloadMass FROM SPACEXTBL WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXTBL);
```

### Result Set:
|   FlightNumber | Date       | Serial   | LaunchSite   |   PayloadMass |
|---------------:|:-----------|:---------|:-------------|--------------:|
|             69 | 2019-11-11 | B1048    | CCAFS SLC 40 |         15600 |
|             74 | 2020-01-29 | B1051    | CCAFS SLC 40 |         15600 |
|             77 | 2020-03-18 | B1048    | KSC LC 39A   |         15600 |

**Beginner SQL Concept:** A nested subquery `(SELECT MAX(PayloadMass) FROM SPACEXTBL)` dynamically finds the highest payload weight in kilograms and returns all matching missions.

**Analytical Interpretation:** The heaviest payloads lifted (15,600 kg) correspond to Starlink multi-satellite deployment missions.

---

## Query 9: Monthly Landing Outcomes in the Year 2015
**Business / Analytical Question:** List records showing month, outcome, booster serial, and launch site for flights conducted in the year 2015.

```sql
SELECT strftime('%m', Date) AS MonthNumber, Date, Serial, LaunchSite, Outcome, Class FROM SPACEXTBL WHERE strftime('%Y', Date) = '2015' ORDER BY Date;
```

### Result Set:
|   MonthNumber | Date       | Serial   | LaunchSite   | Outcome    |   Class |
|--------------:|:-----------|:---------|:-------------|:-----------|--------:|
|            01 | 2015-01-10 | B1012    | CCAFS SLC 40 | False ASDS |       0 |
|            02 | 2015-02-11 | B1013    | CCAFS SLC 40 | True Ocean |       1 |
|            04 | 2015-04-14 | B1015    | CCAFS SLC 40 | False ASDS |       0 |
|            04 | 2015-04-27 | B1016    | CCAFS SLC 40 | None None  |       0 |
|            06 | 2015-06-28 | B1018    | CCAFS SLC 40 | None ASDS  |       0 |
|            12 | 2015-12-22 | B1019    | CCAFS SLC 40 | True RTLS  |       1 |

**Beginner SQL Concept:** SQLite's `strftime('%m', Date)` extracts the two-digit month, and `strftime('%Y', Date)` filters exclusively for the year 2015.

**Analytical Interpretation:** In 2015, SpaceX conducted 6 orbital missions, performing ocean and early drone ship landing experiments.

---

## Query 10: Ranked Landing Outcomes Frequency
**Business / Analytical Question:** Rank all distinct landing outcome types by their frequency between 2010-06-04 and 2020-11-05 in descending order.

```sql
SELECT Outcome, COUNT(*) AS Frequency, CASE WHEN Outcome LIKE 'True%' THEN 'Success' ELSE 'Failure / Unrecovered' END AS Classification FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2020-11-05' GROUP BY Outcome ORDER BY Frequency DESC;
```

### Result Set:
| Outcome     |   Frequency | Classification        |
|:------------|------------:|:----------------------|
| True ASDS   |          41 | Success               |
| None None   |          19 | Failure / Unrecovered |
| True RTLS   |          14 | Success               |
| False ASDS  |           6 | Failure / Unrecovered |
| True Ocean  |           5 | Success               |
| None ASDS   |           2 | Failure / Unrecovered |
| False Ocean |           2 | Failure / Unrecovered |
| False RTLS  |           1 | Failure / Unrecovered |

**Beginner SQL Concept:** `GROUP BY Outcome` groups identical outcomes together. `COUNT(*)` tallies occurrences, and `ORDER BY Frequency DESC` sorts the most common landing result at the top.

**Analytical Interpretation:** `True ASDS` (Autonomous Spaceport Drone Ship) is by far the most frequent landing outcome with 41 successful recoveries.

---

## Query 11: Launch Site Performance & Success Rate Comparison
**Business / Analytical Question:** Which launch site has conducted the most missions, and what is the landing success rate of each site?

```sql
SELECT LaunchSite, COUNT(*) AS TotalLaunches, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalLaunches DESC;
```

### Result Set:
| LaunchSite   |   TotalLaunches |   SuccessfulLandings |   SuccessRatePercentage |
|:-------------|----------------:|---------------------:|------------------------:|
| CCAFS SLC 40 |              55 |                   33 |                   60    |
| KSC LC 39A   |              22 |                   17 |                   77.27 |
| VAFB SLC 4E  |              13 |                   10 |                   76.92 |

**Beginner SQL Concept:** `SUM(Class)` counts total successes because `Class` is encoded as 1 (success) and 0 (failure). `AVG(Class) * 100.0` calculates the percentage success rate.

**Analytical Interpretation:** KSC LC 39A demonstrates the highest landing success rate at 77.27%, while CCAFS SLC 40 hosted the highest overall volume (55 launches).

---

## Query 12: Orbit Trajectory Analysis & Success Rate
**Business / Analytical Question:** What are the landing success rates for different orbit destinations?

```sql
SELECT Orbit, COUNT(*) AS MissionCount, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage, ROUND(AVG(PayloadMass), 2) AS AvgPayloadMass_KG FROM SPACEXTBL GROUP BY Orbit ORDER BY MissionCount DESC;
```

### Result Set:
| Orbit   |   MissionCount |   SuccessfulLandings |   SuccessRatePercentage |   AvgPayloadMass_KG |
|:--------|---------------:|---------------------:|------------------------:|--------------------:|
| GTO     |             27 |                   14 |                   51.85 |             5011.99 |
| ISS     |             21 |                   13 |                   61.9  |             3279.94 |
| VLEO    |             14 |                   12 |                   85.71 |            15315.7  |
| PO      |              9 |                    6 |                   66.67 |             7583.67 |
| LEO     |              7 |                    5 |                   71.43 |             3882.84 |
| SSO     |              5 |                    5 |                  100    |             2060    |
| MEO     |              3 |                    2 |                   66.67 |             3987    |
| SO      |              1 |                    0 |                    0    |             6104.96 |
| HEO     |              1 |                    1 |                  100    |              350    |
| GEO     |              1 |                    1 |                  100    |             6104.96 |
| ES-L1   |              1 |                    1 |                  100    |              570    |

**Beginner SQL Concept:** Grouping by target orbital trajectory (`Orbit`) reveals payload demands and recovery feasibility across low-Earth, geostationary, and deep-space missions.

**Analytical Interpretation:** High-altitude orbits like ES-L1, GEO, and HEO achieved 100% landing success, while heavy GTO missions presented higher recovery difficulty due to high reentry velocity.

---

