-- Query 1: Unique Launch Sites
-- Question: What are the unique launch sites used in SpaceX Falcon 9 missions?
SELECT DISTINCT LaunchSite FROM SPACEXTBL;

-- Query 2: First 5 Records with Cape Canaveral Launch Sites
-- Question: Display 5 records where launch site begins with the prefix 'CCA'.
SELECT FlightNumber, Date, LaunchSite, BoosterVersion, PayloadMass FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' LIMIT 5;

-- Query 3: Total Payload Mass by Launch Site
-- Question: Calculate the total payload mass carried from each launch site.
SELECT LaunchSite, SUM(PayloadMass) AS TotalPayloadMass_KG, COUNT(*) AS TotalLaunches FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalPayloadMass_KG DESC;

-- Query 4: Average Payload Mass by Booster Version Category
-- Question: What is the average payload mass across all Falcon 9 missions?
SELECT BoosterVersion, ROUND(AVG(PayloadMass), 2) AS AveragePayload_KG, MIN(PayloadMass) AS MinPayload_KG, MAX(PayloadMass) AS MaxPayload_KG FROM SPACEXTBL GROUP BY BoosterVersion;

-- Query 5: First Successful Ground Pad Landing Date
-- Question: What is the date of the very first successful landing on a ground pad (RTLS)?
SELECT MIN(Date) AS FirstSuccessfulGroundLandingDate, FlightNumber, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True RTLS';

-- Query 6: Drone Ship Successes with Intermediate Payload Mass (4,000 to 6,000 kg)
-- Question: List booster serials and dates that successfully landed on a drone ship carrying payload between 4,000 kg and 6,000 kg.
SELECT FlightNumber, Date, Serial, PayloadMass, LaunchSite, Outcome FROM SPACEXTBL WHERE Outcome = 'True ASDS' AND PayloadMass BETWEEN 4000 AND 6000;

-- Query 7: Mission Outcome Breakdown (Success vs Failure Counts)
-- Question: What is the total count of successful first stage landings versus failed/expended attempts?
SELECT CASE WHEN Class = 1 THEN 'Successful Landing' ELSE 'Failure / Uncontrolled' END AS LandingStatus, COUNT(*) AS TotalCount, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM SPACEXTBL), 2) AS Percentage FROM SPACEXTBL GROUP BY Class ORDER BY TotalCount DESC;

-- Query 8: Booster Carrying Maximum Payload Mass
-- Question: Which booster core(s) and flight numbers carried the maximum recorded payload mass?
SELECT FlightNumber, Date, Serial, LaunchSite, PayloadMass FROM SPACEXTBL WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXTBL);

-- Query 9: Monthly Landing Outcomes in the Year 2015
-- Question: List records showing month, outcome, booster serial, and launch site for flights conducted in the year 2015.
SELECT strftime('%m', Date) AS MonthNumber, Date, Serial, LaunchSite, Outcome, Class FROM SPACEXTBL WHERE strftime('%Y', Date) = '2015' ORDER BY Date;

-- Query 10: Ranked Landing Outcomes Frequency
-- Question: Rank all distinct landing outcome types by their frequency between 2010-06-04 and 2020-11-05 in descending order.
SELECT Outcome, COUNT(*) AS Frequency, CASE WHEN Outcome LIKE 'True%' THEN 'Success' ELSE 'Failure / Unrecovered' END AS Classification FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2020-11-05' GROUP BY Outcome ORDER BY Frequency DESC;

-- Query 11: Launch Site Performance & Success Rate Comparison
-- Question: Which launch site has conducted the most missions, and what is the landing success rate of each site?
SELECT LaunchSite, COUNT(*) AS TotalLaunches, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage FROM SPACEXTBL GROUP BY LaunchSite ORDER BY TotalLaunches DESC;

-- Query 12: Orbit Trajectory Analysis & Success Rate
-- Question: What are the landing success rates for different orbit destinations?
SELECT Orbit, COUNT(*) AS MissionCount, SUM(Class) AS SuccessfulLandings, ROUND(AVG(Class) * 100.0, 2) AS SuccessRatePercentage, ROUND(AVG(PayloadMass), 2) AS AvgPayloadMass_KG FROM SPACEXTBL GROUP BY Orbit ORDER BY MissionCount DESC;
