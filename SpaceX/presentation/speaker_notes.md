# SpaceX Falcon 9 First Stage Landing Prediction: Complete Presentation Speaker Script

This document provides a beginner-friendly, slide-by-slide presentation script for delivering your 23-slide capstone presentation.

---

### Slide 1: Title Slide & Project Overview
"Good morning, everyone. Welcome to my presentation on the IBM Data Science Professional Certificate Capstone Project: SpaceX Falcon 9 First Stage Landing Prediction. In this project, I built an end-to-end data science and machine learning pipeline that collects, wrangles, visualizes, and models historical SpaceX Falcon 9 launches to predict whether a booster's first stage will land successfully. All source code, completed Jupyter notebooks, SQL scripts, interactive dashboards, and datasets are hosted in my GitHub repository at https://github.com/buildwithneel/Coursera-IBM-data-science-course."

---

### Slide 2: Executive Summary (Question 3)
"To begin with an executive summary: Falcon 9 launches cost roughly $62 million, whereas competitor launches frequently exceed $165 million. That staggering $103 million savings is made possible entirely by recovering and reusing the first-stage rocket booster. In this project, I analyzed 90 historical launches, where the overall landing success rate was 66.7%. Through exploratory data analysis, we uncovered a steep operational learning curve where landing success improved from 0% in early test years to over 84% in modern flights. Using machine learning, my best models—specifically tuned K-Nearest Neighbors and Logistic Regression—achieved an 83.33% accuracy rate and an 0.889 F1-score on held-out test data."

---

### Slide 3: Introduction & Business Problem (Question 4)
"Why does this matter commercially? When a rocket launches into space, the first-stage booster represents approximately 70% of the entire vehicle's manufacturing cost—roughly $30 million to $40 million. Historically, all rockets were expendable, discarded into the ocean after a single flight. By recovering boosters via drone ships or ground pads, SpaceX can reuse them multiple times and offer massive commercial discounts. For competitor launch providers or commercial satellite operators bidding on launch contracts, knowing in advance whether SpaceX will recover the booster allows them to predict SpaceX's pricing flexibility and calculate competitive bid margins."

---

### Slide 4: Project Architecture & Pipeline Flow (Question 14)
"Slide 4 illustrates our 5-tier project architecture. The pipeline begins with data ingestion via the SpaceX REST API v4 and Wikipedia web scraping, flows into data wrangling where we impute missing payload values and construct our binary target variable, transitions to analytical engines in SQLite, Folium, and Plotly Dash, and culminates in supervised machine learning classification. To ensure strict data integrity and prevent data leakage, feature scaling is fitted strictly on the 80% training split, keeping the 20% test partition completely held out."

---

### Slide 5: Data Collection Methodology & Lab Links (Question 5)
"For data collection, I extracted data from two complementary sources. First, I queried the public SpaceX REST API v4 past launches endpoint, unpacking nested JSON objects for payload masses, launch complexes, booster serial numbers, and core landing attempts. Second, I used BeautifulSoup to scrape historical Falcon 9 launch tables from Wikipedia, parsing 321 tabular flight records. Both completed Jupyter notebooks—Lab 1 for the API and Lab 2 for web scraping—are accessible via the direct GitHub links shown on the slide."

---

### Slide 6: Data Wrangling Methodology & Lab Link (Question 5)
"In the data wrangling phase (Lab 3), I audited the dataset for missing values. Missing payload masses in early test flights were imputed using the dataset mean of 6,104.95 kilograms. Next, I constructed our binary target variable, Class. If a booster achieved a successful touchdown on an Autonomous Spaceport Drone Ship, a ground pad, or controlled ocean water, Class was assigned 1. If the booster crashed, missed, or was expended without recovery, Class was assigned 0. Across our 90 flights, 60 were successful landings and 30 were failures, yielding a 66.7% baseline success rate. Finally, categorical variables were one-hot encoded into an 80-feature matrix for machine learning."

---

### Slide 7: Exploratory Data Analysis Methodology & Hypotheses (Question 6)
"In the exploratory data analysis phase (Lab 4), I formulated four core hypotheses: First, does booster landing success improve over time as SpaceX iterates on avionics and grid fin control? Second, do launch sites exhibit divergent success rates due to differing orbital azimuths? Third, does heavier payload mass reduce fuel reserves needed for landing burns? And fourth, do deep high-energy orbits like GTO show lower recovery rates than Low Earth Orbit? We used Pandas, Matplotlib, and Seaborn to test these hypotheses across 10 detailed visualizations."

---

### Slide 8: EDA Tasks 1 & 2: Launch Site vs Flight Number & Payload Mass (Question 8)
"On Slide 8, we evaluate IBM Capstone EDA Tasks 1 and 2. Task 1 on the left reveals that Cape Canaveral SLC 40 absorbed all early flights from 1 to 25 with experimental failures. Kennedy Space Center entered service around Flight 30 with predominantly successful touchdowns. Task 2 on the right demonstrates that heavy payloads exceeding 10,000 kilograms are launched exclusively from Florida complexes, whereas California's Vandenberg complex handles lighter payloads under 10,000 kg."

---

### Slide 9: EDA Tasks 3 & 4: Orbit Success Rate & Flight Number (Question 8)
"Slide 9 displays EDA Tasks 3 and 4. Task 3 shows that high-altitude orbits like ES-L1, GEO, HEO, and SSO achieved a 100% landing success rate, whereas GTO achieved only 51.8% success due to extreme re-entry velocities. Task 4 illustrates flight numbers versus orbit types: while early GTO and ISS flights experienced landing crashes, later flights beyond Flight 50 achieved near-perfect recovery across all orbits."

---

### Slide 10: EDA Tasks 5 & 6: Payload vs Orbit & Yearly Success Trend (Question 8)
"Slide 10 highlights EDA Tasks 5 and 6. Task 5 shows that heavy Starlink payloads are concentrated in Very Low Earth Orbit (VLEO) and achieved high recovery rates. Task 6 displays the yearly success trend line: landing success rose from 0% between 2010 and 2013, to 33.3% in 2014-2015, surging past 80% in 2017, and reaching 84.2% in 2020. The introduction of Block 5 boosters in 2018 established sustained high reliability."

---

### Slide 11: EDA Cadence & Overall Success Distribution (Question 8)
"Slide 11 reviews overall operational growth. Annual launch cadence expanded 19-fold, from 1 launch in 2010 to 19 launches in 2020. The donut chart on the right depicts our overall binary target balance: 60 successful landings, or 66.7%, versus 30 failed or expended attempts, or 33.3%."

---

### Slide 12: SQL Tasks 1 to 4: Launch Complexes & Payload Statistics (Question 9)
"Moving to SQL data analysis in Lab 5: Task 1 identified our three distinct launch sites: CCAFS SLC 40, KSC LC 39A, and VAFB SLC 4E. Task 2 queried the first five Cape Canaveral flights. Task 3 calculated total payload lifted: CCAFS lifted over 305,000 kilograms across 55 flights. Task 4 determined the average payload across all 90 flights as 6,105 kg, ranging from 350 kg to 15,600 kg."

---

### Slide 13: SQL Tasks 5 to 7: Milestones & Outcome Distributions (Question 9)
"Continuing SQL analysis: Task 5 identified the exact date of the world's first successful ground pad landing: December 22, 2015, by booster B1019 at Cape Canaveral. Task 6 queried drone ship successes carrying 4,000 to 6,000 kg, identifying boosters B1022, B1026, and B1048. Task 7 aggregated the 60 successful versus 30 failed mission outcomes."

---

### Slide 14: SQL Tasks 8 to 10: Max Payload, 2015 Outcomes & Rankings (Question 9)
"Completing our SQL queries: Task 8 identified Starlink Block 5 boosters carrying the maximum payload of 15,600 kg. Task 9 revealed monthly outcomes in 2015, showing experimental ocean splashes leading to the December RTLS breakthrough. Task 10 ranked recovery modes: Drone Ship landings (True ASDS) proved to be SpaceX's workhorse with 41 successful recoveries."

---

### Slide 15: Geospatial Analysis: Folium Launch Sites, Markers & Counts (Question 10)
"Slide 15 presents our interactive Folium map from Lab 6. We mapped all three launch complexes: CCAFS with 55 launches and a 60% success rate; KSC with 22 launches and a 77.3% success rate; and VAFB with 13 launches and a 76.9% success rate. The MarkerCluster plugin groups all 90 individual launches with green markers for successes and red markers for failures."

---

### Slide 16: Folium Distance & Proximity Analysis (Question 10)
"Slide 16 details our Haversine geodesic distance analysis. Every launchpad is situated within 0.95 to 1.5 kilometers of open water, ensuring that ascent failures drop harmlessly into the ocean. The complexes sit within 1 to 2 km of rail lines and highways for booster transport, while maintaining a safe 15 to 35 km buffer from urban population centers like Titusville and Lompoc."

---

### Slide 17: Interactive Dashboard: Plotly Dash (Question 11)
"Slide 17 highlights our interactive Plotly Dash analytics console from Lab 7. The dashboard allows users to dynamically filter flights by launch site, adjust payload mass from 0 to 16,000 kg, and toggle outcome categories. Reactive callbacks instantly update summary KPI cards, donut distributions, scatter plots, and yearly cadence bars."

---

### Slide 18: Predictive Analysis: Machine Learning Methodology (Question 7)
"Moving to predictive modeling in Lab 8, we formulated the task as a binary classification problem. To strictly prevent data leakage, we split our 80-feature dataset into an 80% training set and a 20% test set using stratified sampling, fitting StandardScaler strictly on the training partition. We implemented 10-fold stratified cross-validation inside GridSearchCV to tune Logistic Regression, Support Vector Machines, Decision Trees, and K-Nearest Neighbors."

---

### Slide 19: Model Comparison Table & Hyperparameters (Question 12)
"Slide 19 presents our empirical model comparison table. Both tuned K-Nearest Neighbors and Logistic Regression achieved the highest performance on our held-out test data, with 83.33% accuracy and an F1-score of 0.889. The optimal hyperparameters found by GridSearchCV are listed on the slide for each of the four algorithms."

---

### Slide 20: Confusion Matrix Results & Error Analysis (Question 12)
"Slide 20 provides the confusion matrix breakdown for all four models on the held-out test set of 18 flights. Both KNN and Logistic Regression correctly classified 12 out of 12 successful landings (100% recall) and 3 out of 6 failed attempts. Crucially, they produced ZERO False Negatives, meaning no successful booster recovery was missed."

---

### Slide 21: Feature Importance & Decision Drivers (Question 14 & 15)
"Slide 21 examines feature importance. GridFins and LandingLeg deployment are the strongest positive indicators of booster recovery. Transitioning to Block 5 boosters dramatically increased recovery odds. Conversely, heavy payloads destined for high-energy GTO orbits negatively impact recovery probability due to propellant limitations."

---

### Slide 22: Conclusions, Innovation & Future Roadmap (Question 13, 14, 15)
"In conclusion, booster reuse provides SpaceX with an insurmountable commercial cost advantage of roughly $103 million per flight. Our models demonstrate that booster recovery can be accurately predicted prior to launch. Key innovative findings included the 2,000 to 5,300 kg payload sweet spot and quantifying coastline safety buffer zones. For future work, incorporating real-time ocean wave heights and drone ship accelerometer telemetry could further refine landing predictions."

---

### Slide 23: References & Project Submission (Question 1 & 2)
"Thank you very much for your time. All source code, completed notebooks, SQL queries, interactive maps, dashboards, and deliverables are fully documented and accessible at my GitHub repository: https://github.com/buildwithneel/Coursera-IBM-data-science-course. I am now glad to answer any questions."
