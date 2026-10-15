# SpaceX Falcon 9 First Stage Landing Prediction: Complete Presentation Speaker Script

This document provides a beginner-friendly, slide-by-slide presentation script for delivering your 16-slide capstone presentation.

---

### Slide 1: Title Slide
**Spoken Words:**
"Good morning, everyone. Welcome to my presentation on the IBM Data Science Capstone Project: SpaceX Falcon 9 First Stage Landing Prediction. In this project, I built an end-to-end data science pipeline combining API data collection, web scraping, data wrangling, exploratory analysis, SQL data querying, geospatial visualization with Folium, an interactive Plotly Dash dashboard, and machine learning classification to predict whether a Falcon 9 booster will successfully land."

---

### Slide 2: Executive Summary
**Spoken Words:**
"To begin with an executive summary: Falcon 9 launches cost roughly $62 million, while competitor launches typically exceed $165 million. The key difference is booster reuse. In this project, I analyzed 90 historical launches, where the overall landing success rate was 66.7%. Through data analysis, we found that landing success improved dramatically over time as SpaceX iterated on its designs. By applying machine learning, my best models—specifically tuned K-Nearest Neighbors and Logistic Regression—achieved an 83.3% accuracy rate on held-out test data."

---

### Slide 3: Business Problem & Launch Economics
**Spoken Words:**
"Why does this matter commercially? When a rocket launches into space, the first stage booster represents roughly 70% of the vehicle's manufacturing cost. Historically, rockets were expendable—they were discarded into the ocean after a single flight. By recovering and reusing boosters, SpaceX drastically cuts launch costs. If an alternative launch provider or commercial satellite operator wants to bid against SpaceX, they need to know in advance whether SpaceX will be able to recover the booster. If SpaceX recovers the booster, they can offer steep discounts. Our predictive model provides this commercial forecasting capability."

---

### Slide 4: Data Collection Methodology
**Spoken Words:**
"For data collection, I gathered data from two primary sources. First, I queried the public SpaceX REST API v4, extracting launchpad details, payloads, rocket specifications, and landing core outcomes. Second, I used BeautifulSoup to scrape historical launch tables from Wikipedia, parsing flight numbers, dates, and booster versions. To ensure that the project is completely reproducible even if public endpoints change or experience rate limits, I implemented a fault-tolerant caching system that saves the raw data locally."

---

### Slide 5: Data Wrangling & Target Construction
**Spoken Words:**
"Next, in the data wrangling phase, I cleaned the dataset. Missing values in the payload mass column were imputed using the dataset mean of approximately 6,105 kilograms. Most importantly, I constructed our binary target variable, Class. If a booster successfully landed on a drone ship, ground pad, or ocean water, Class was assigned 1. If the booster crashed, missed, or was expended without recovery, Class was assigned 0. Across our 90 launches, 60 were successful landings and 30 were failures, yielding a 66.7% baseline success rate."

---

### Slide 6: Exploratory Data Analysis Methodology
**Spoken Words:**
"In the exploratory data analysis phase, I investigated several key questions: How does launch volume and landing success evolve over time? How do different launch sites perform? How does payload weight affect recovery? And does the target orbit impact landing feasibility? We used Matplotlib, Seaborn, and Pandas to uncover these patterns."

---

### Slide 7: EDA Results: Launch Cadence & Success Learning Curve
**Spoken Words:**
"Looking at the visualizations on Slide 7, we see two critical trends. On the left, launch volume expanded dramatically from just a couple of test launches in 2010 to nearly 20 launches per year by 2020. On the right, the yearly landing success rate exhibits a clear technical learning curve. In the early years from 2010 to 2013, the landing success rate was 0%. By 2017 to 2020, as SpaceX refined its titanium grid fins and automated drone ships, the success rate surged above 85%."

---

### Slide 8: EDA Results: Orbit Profile & Payload Dynamics
**Spoken Words:**
"On Slide 8, we explore orbit and payload relationships. High-altitude orbits such as ES-L1, GEO, and Sun-Synchronous Orbits achieved a 100% landing success rate. On the other hand, heavy Geostationary Transfer Orbit (GTO) missions exhibited mixed outcomes because the booster reenters the atmosphere at extreme hypersonic velocities, reducing fuel margins. Medium payloads between 2,000 and 6,000 kg had the highest consistency of successful touchdowns."

---

### Slide 9: SQL Analysis: Launch Complexes & Payload Statistics
**Spoken Words:**
"For SQL analysis, I created a local SQLite database and executed queries addressing key operational questions. Cape Canaveral Air Force Station (SLC 40) is SpaceX's primary workhorse, hosting 55 launches and lifting over 300,000 kilograms of payload. However, Kennedy Space Center (LC 39A) demonstrated the highest landing success rate at 77.3%. Across all missions, payloads ranged from 350 kg to 15,600 kg."

---

### Slide 10: SQL Analysis: Outcomes & Historical Milestones
**Spoken Words:**
"Our SQL queries also identified key historical milestones. The first successful ground pad landing occurred on December 22, 2015, at Cape Canaveral. Autonomous Spaceport Drone Ships (ASDS) proved to be the most common recovery method, accounting for 41 successful landings. The maximum payload lifted was 15,600 kilograms, carried by Block 5 boosters during multi-satellite Starlink launches."

---

### Slide 11: Geospatial Analysis: Interactive Folium Map
**Spoken Words:**
"In our geospatial analysis, I used Folium to build an interactive launch site map. Every launchpad is deliberately situated along the coastline, within 1 to 2 kilometers of the Atlantic or Pacific Ocean. This ensures that rockets launch over water rather than populated areas. The pads are also located near railways and highways for rocket transport, while maintaining a safe 10 to 30 kilometer buffer from urban centers."

---

### Slide 12: Interactive Dashboard: Plotly Dash
**Spoken Words:**
"On Slide 12, you see a screenshot of our running Plotly Dash interactive dashboard. The dashboard features dynamic filters: a launch site dropdown, a payload mass range slider, and an outcome selector. As the user adjusts these controls, Dash callbacks automatically update key metric cards and interactive charts, displaying real-time success percentages and payload distributions."

---

### Slide 13: Machine Learning Methodology & Leakage Prevention
**Spoken Words:**
"Moving to predictive modeling, I formulated the task as a binary classification problem. To strictly prevent data leakage, I split the data into an 80% training set and a 20% test set using stratified sampling before applying standard scaling. I implemented 10-fold stratified cross-validation inside GridSearchCV to tune four distinct algorithms: Logistic Regression, Support Vector Machines, Decision Trees, and K-Nearest Neighbors."

---

### Slide 14: Model Comparison & Test Set Evaluation
**Spoken Words:**
"Slide 14 presents our empirical modeling results. Both tuned K-Nearest Neighbors and Logistic Regression achieved the highest performance on our held-out test data, with an accuracy of 83.3% and an F1-score of 0.889. Looking at the confusion matrix, the models correctly predicted 11 out of 12 successful landings and 4 out of 6 failed attempts. The most influential features were grid fin deployment, landing leg availability, booster flight sequence, and target orbit."

---

### Slide 15: Conclusions, Innovation & Future Work
**Spoken Words:**
"In conclusion, booster reuse provides SpaceX with an enormous cost advantage of roughly $40 million per launch. Our machine learning models demonstrate that booster recovery can be accurately predicted using mission parameters. An innovative aspect of this project was combining geospatial distance metrics with operational telemetry. For future work, incorporating real-time ocean wave heights and weather telemetry at drone ship locations could further refine prediction accuracy."

---

### Slide 16: References & Submission
**Spoken Words:**
"Thank you very much for your time. All source code, Jupyter notebooks, SQL scripts, interactive maps, dashboards, and documentation are available in the project repository. I would be glad to answer any questions."
