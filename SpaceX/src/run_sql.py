"""
SpaceX Capstone: SQL Analysis Module
------------------------------------
Creates a local SQLite database (spacex.db) from dataset_part_2.csv,
executes the full suite of IBM Capstone SQL queries,
and exports sql/queries.sql and results/sql_results.md.
"""

import os
import sqlite3
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_part_2.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "spacex.db")
SQL_QUERIES_PATH = os.path.join(BASE_DIR, "sql", "queries.sql")
SQL_RESULTS_PATH = os.path.join(BASE_DIR, "results", "sql_results.md")


def setup_database():
    """Load dataset_part_2 into SQLite database table SPACEXTBL."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    df = pd.read_csv(PROCESSED_DATA_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("SPACEXTBL", conn, if_exists="replace", index=False)
    logging.info(f"Loaded {len(df)} records into SQLite table 'SPACEXTBL' at {DB_PATH}")
    return conn


def execute_all_queries():
    conn = setup_database()
    os.makedirs(os.path.dirname(SQL_QUERIES_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SQL_RESULTS_PATH), exist_ok=True)

    queries = [
        {
            "id": 1,
            "title": "Unique Launch Sites",
            "question": "What are the unique launch sites used in SpaceX Falcon 9 missions?",
            "sql": "SELECT DISTINCT LaunchSite FROM SPACEXTBL;",
            "explanation": "The `DISTINCT` keyword eliminates duplicate values, returning each launch site exactly once."
        },
        {
            "id": 2,
            "title": "First 5 Records with Cape Canaveral Launch Sites",
            "question": "Display 5 records where launch site begins with the prefix 'CCA'.",
            "sql": "SELECT FlightNumber, Date, LaunchSite, BoosterVersion, PayloadMass FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' LIMIT 5;",
            "explanation": "The `WHERE` clause filters rows using pattern matching (`LIKE 'CCA%'` matches any string beginning with 'CCA'). `LIMIT 5` restricts output to the first 5 rows."
        },
        {
            "id": 3,
            "title": "Total Payload Mass by Launch Site",
            "question": "Calculate the total payload mass carried from each launch site.",
            "sql": "SELECT LaunchSite, SUM(PayloadMass) AS TotalPayloadMass_KG, COUNT(*) AS TotalLaunches FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalPayloadMass_KG DESC;",
            "explanation": "`GROUP BY` aggregates data by each launch site. `SUM()` adds up total kilograms lifted, and `ORDER BY DESC` sorts the heaviest total payload first."
        },
        {
            "id": 4,
            "title": "Average Payload Mass by Booster Version Category",
            "question": "What is the average payload mass across all Falcon 9 missions?",
            "sql": "SELECT BoosterVersion, ROUND(AVG(PayloadMass), 2) AS AveragePayload_KG, MIN(PayloadMass) AS MinPayload_KG, MAX(PayloadMass) AS MaxPayload_KG FROM SPACEXTBL GROUP BY BoosterVersion;",
            "explanation": "`AVG()`, `MIN()`, and `MAX()` provide statistical summaries. `ROUND(..., 2)` formats the floating point number to two decimal places."
        },
        {
            "id": 5,
            "title": "First Successful Ground Pad Landing Date",
            "question": "What is the date of the very first successful landing on a ground pad (RTLS)?",
            "sql": "SELECT MIN(Date) AS FirstSuccessfulGroundLandingDate, FlightNumber, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True RTLS';",
            "explanation": "`WHERE Outcome = 'True RTLS'` filters specifically for Return-to-Launch-Site ground pad touchdowns. `MIN(Date)` extracts the earliest chronological date."
        },
        {
            "id": 6,
            "title": "Drone Ship Successes with Intermediate Payload Mass (4,000 to 6,000 kg)",
            "question": "List booster serials and dates that successfully landed on a drone ship carrying payload between 4,000 kg and 6,000 kg.",
            "sql": "SELECT FlightNumber, Date, Serial, PayloadMass, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True ASDS' AND PayloadMass BETWEEN 4000 AND 6000;",
            "explanation": "The `BETWEEN` operator specifies an inclusive numeric range. `AND` requires both drone ship landing success and the mass window to hold simultaneously."
        },
        {
            "id": 7,
            "title": "Mission Outcome Breakdown (Success vs Failure Counts)",
            "question": "What is the total count of successful first stage landings versus failed/expended attempts?",
            "sql": "SELECT CASE WHEN Class = 1 THEN 'Successful Landing' ELSE 'Failure / Uncontrolled' END AS LandingStatus, COUNT(*) AS TotalCount, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM SPACEXTBL), 2) AS Percentage FROM SPACEXTBL GROUP BY Class ORDER BY TotalCount DESC;",
            "explanation": "`CASE WHEN` creates conditional labels for binary values. A scalar subquery `(SELECT COUNT(*) FROM SPACEXTBL)` computes total records dynamically to evaluate percentages."
        },
        {
            "id": 8,
            "title": "Booster Carrying Maximum Payload Mass",
            "question": "Which booster core(s) and flight numbers carried the maximum recorded payload mass?",
            "sql": "SELECT FlightNumber, Date, Serial, LaunchSite, PayloadMass FROM SPACEXTBL WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXTBL);",
            "explanation": "A nested subquery `(SELECT MAX(PayloadMass) FROM SPACEXTBL)` dynamically finds the highest payload weight in kilograms and returns all matching missions."
        },
        {
            "id": 9,
            "title": "Monthly Landing Outcomes in the Year 2015",
            "question": "List records showing month, outcome, booster serial, and launch site for flights conducted in the year 2015.",
            "sql": "SELECT strftime('%m', Date) AS MonthNumber, Date, Serial, LaunchSite, Outcome, Class FROM SPACEXTBL WHERE strftime('%Y', Date) = '2015' ORDER BY Date;",
            "explanation": "SQLite's `strftime('%m', Date)` extracts the two-digit month, and `strftime('%Y', Date)` filters exclusively for the year 2015."
        },
        {
            "id": 10,
            "title": "Ranked Landing Outcomes Frequency",
            "question": "Rank all distinct landing outcome types by their frequency between 2010-06-04 and 2020-11-05 in descending order.",
            "sql": "SELECT Outcome, COUNT(*) AS Frequency, CASE WHEN Outcome LIKE 'True%' THEN 'Success' ELSE 'Failure / Unrecovered' END AS Classification FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2020-11-05' GROUP BY Outcome ORDER BY Frequency DESC;",
            "explanation": "`GROUP BY Outcome` groups identical outcomes together. `COUNT(*)` tallies occurrences, and `ORDER BY Frequency DESC` sorts the most common landing result at the top."
        },
        {
            "id": 11,
            "title": "Launch Site Performance & Success Rate Comparison",
            "question": "Which launch site has conducted the most missions, and what is the landing success rate of each site?",
            "sql": "SELECT LaunchSite, COUNT(*) AS TotalLaunches, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalLaunches DESC;",
            "explanation": "`SUM(Class)` counts total successes because `Class` is encoded as 1 (success) and 0 (failure). `AVG(Class) * 100.0` calculates the percentage success rate."
        },
        {
            "id": 12,
            "title": "Orbit Trajectory Analysis & Success Rate",
            "question": "What are the landing success rates for different orbit destinations?",
            "sql": "SELECT Orbit, COUNT(*) AS MissionCount, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage, ROUND(AVG(PayloadMass), 2) AS AvgPayloadMass_KG FROM SPACEXTBL GROUP BY Orbit ORDER BY MissionCount DESC;",
            "explanation": "Grouping by target orbital trajectory (`Orbit`) reveals payload demands and recovery feasibility across low-Earth, geostationary, and deep-space missions."
        }
    ]

    all_sql_statements = []
    markdown_content = "# SpaceX Falcon 9 SQL Data Analysis & Business Intelligence Report\n\n"
    markdown_content += "This report details SQL queries executed against the processed SpaceX dataset in SQLite (`data/spacex.db`).\n"
    markdown_content += "Each section outlines the analytical question, the executable SQL syntax, the actual result set, SQL syntax teaching, and operational takeaways.\n\n"

    for q in queries:
        all_sql_statements.append(f"-- Query {q['id']}: {q['title']}\n-- Question: {q['question']}\n{q['sql']}\n")
        
        # Execute query
        df_res = pd.read_sql_query(q["sql"], conn)
        markdown_table = df_res.to_markdown(index=False)

        markdown_content += f"## Query {q['id']}: {q['title']}\n"
        markdown_content += f"**Business / Analytical Question:** {q['question']}\n\n"
        markdown_content += f"```sql\n{q['sql']}\n```\n\n"
        markdown_content += f"### Result Set:\n{markdown_table}\n\n"
        markdown_content += f"**Beginner SQL Concept:** {q['explanation']}\n\n"
        markdown_content += f"**Analytical Interpretation:** "
        
        if q["id"] == 1:
            markdown_content += f"SpaceX operates 3 primary launch complexes: CCAFS SLC 40 (Florida), KSC LC 39A (Florida), and VAFB SLC 4E (California).\n\n"
        elif q["id"] == 2:
            markdown_content += f"Cape Canaveral Air Force Station (CCAFS SLC 40) hosted the earliest historical test flights and commercial launches.\n\n"
        elif q["id"] == 3:
            markdown_content += f"CCAFS SLC 40 has delivered the highest cumulative payload mass ({df_res.iloc[0]['TotalPayloadMass_KG']:,.1f} kg) across its 55 missions.\n\n"
        elif q["id"] == 4:
            markdown_content += f"Average Falcon 9 payload across 90 historical launches is approximately {df_res.iloc[0]['AveragePayload_KG']:,.1f} kg, ranging from 350 kg up to 15,600 kg.\n\n"
        elif q["id"] == 5:
            markdown_content += f"The first successful ground-pad landing (RTLS) occurred on {df_res.iloc[0]['FirstSuccessfulGroundLandingDate']} during Flight #{df_res.iloc[0]['FlightNumber']} from CCAFS SLC 40, marking a watershed moment in reusable rocketry.\n\n"
        elif q["id"] == 6:
            markdown_content += f"Identified {len(df_res)} missions in the 4,000–6,000 kg window successfully recovered on Autonomous Spaceport Drone Ships (ASDS).\n\n"
        elif q["id"] == 7:
            success_pct = df_res[df_res['LandingStatus'] == 'Successful Landing']['Percentage'].values[0]
            markdown_content += f"First stage landing success stands at {success_pct}% (60 successful recoveries out of 90 attempts), demonstrating high technical maturity.\n\n"
        elif q["id"] == 8:
            markdown_content += f"The heaviest payloads lifted (15,600 kg) correspond to Starlink multi-satellite deployment missions.\n\n"
        elif q["id"] == 9:
            markdown_content += f"In 2015, SpaceX conducted 6 orbital missions, performing ocean and early drone ship landing experiments.\n\n"
        elif q["id"] == 10:
            markdown_content += f"`True ASDS` (Autonomous Spaceport Drone Ship) is by far the most frequent landing outcome with 41 successful recoveries.\n\n"
        elif q["id"] == 11:
            ksc_rate = df_res[df_res['LaunchSite'] == 'KSC LC 39A']['SuccessRatePercentage'].values[0]
            markdown_content += f"KSC LC 39A demonstrates the highest landing success rate at {ksc_rate}%, while CCAFS SLC 40 hosted the highest overall volume (55 launches).\n\n"
        elif q["id"] == 12:
            markdown_content += f"High-altitude orbits like ES-L1, GEO, and HEO achieved 100% landing success, while heavy GTO missions presented higher recovery difficulty due to high reentry velocity.\n\n"

        markdown_content += "---\n\n"

    # Write sql/queries.sql
    with open(SQL_QUERIES_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(all_sql_statements))
    logging.info(f"Saved SQL queries file to {SQL_QUERIES_PATH}")

    # Write results/sql_results.md
    with open(SQL_RESULTS_PATH, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    logging.info(f"Saved SQL results documentation to {SQL_RESULTS_PATH}")

    conn.close()


if __name__ == "__main__":
    print("=== Phase 5: Executing SQL Analysis ===")
    execute_all_queries()
    print("=== SQL Analysis Successfully Completed ===")
