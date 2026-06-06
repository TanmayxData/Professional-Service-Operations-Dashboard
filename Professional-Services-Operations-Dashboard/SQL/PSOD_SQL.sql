-- create database PSOD;

use PSOD;



-- Q1. How many projects do we have?


SELECT COUNT(*) AS Total_Projects FROM projects_cleaned;



-- Q2. How many active projects are running?


SELECT COUNT(*) AS Active_Projects FROM projects_cleaned
WHERE Status = 'Active';



-- Q3. How many delayed projects are there?


SELECT COUNT(*) AS Delayed_Projects FROM projects_cleaned
WHERE Status = 'Delayed';



-- Q4. What is the total project revenue?


SELECT SUM(Project_Value) AS Total_Revenue
FROM projects_cleaned;



-- Q5. What is the average project value?


SELECT ROUND(AVG(Project_Value),2) AS Average_Project_Value
FROM projects_cleaned;



-- Q6. What is the average project duration?


SELECT ROUND(AVG(DATEDIFF(End_Date, Start_Date)),2) AS Average_Project_Duration_Days FROM projects_cleaned;



-- Q7. What is the project status distribution?


SELECT Status,COUNT(*) AS Project_Count FROM projects_cleaned
GROUP BY Status;



-- Q8. Which clients generate the most revenue?


SELECT c.Client_Name, SUM(p.Project_Value) AS Revenue FROM projects_cleaned p
JOIN clients_cleaned c
ON p.Client_ID = c.Client_ID
GROUP BY c.Client_Name
ORDER BY Revenue DESC;



-- Q9. Which industries generate the most revenue?


SELECT c.Industry, SUM(p.Project_Value) AS Revenue FROM projects_cleaned p
JOIN clients_cleaned c
ON p.Client_ID = c.Client_ID
GROUP BY c.Industry
ORDER BY Revenue DESC;



-- Q10. Which projects have the highest value?


SELECT Project_ID, Project_Value FROM projects_cleaned
ORDER BY Project_Value DESC
LIMIT 10;



-- Q11. How many billable hours were worked?


SELECT SUM(Hours_Worked) AS Total_Billable_Hours FROM timelogs_cleaned
WHERE Billable = 'Yes';



-- Q12. How many non-billable hours were worked?


SELECT SUM(Hours_Worked) AS Total_NonBillable_Hours FROM timelogs_cleaned
WHERE Billable = 'No';



-- Q13. How many hours did each employee work?


SELECT Employee_ID, SUM(Hours_Worked) AS Total_Hours_Worked FROM timelogs_cleaned
GROUP BY Employee_ID
ORDER BY Total_Hours_Worked DESC;



-- Q14. Which employees have the highest billable hours?


SELECT Employee_ID, SUM(Hours_Worked) AS Billable_Hours FROM timelogs_cleaned
WHERE Billable = 'Yes'
GROUP BY Employee_ID
ORDER BY Billable_Hours DESC;



-- Q15. What is each employee's utilization rate?
-- Assumption: 160 hours available per month


SELECT Employee_ID, ROUND((SUM(Hours_Worked) / 160) * 100,2) AS Utilization_Percentage FROM timelogs_cleaned
GROUP BY Employee_ID
ORDER BY Utilization_Percentage DESC;



-- Q16. Which clients consume the most consulting hours?


SELECT c.Client_Name, SUM(t.Hours_Worked) AS Total_Hours FROM timelogs_cleaned t
JOIN projects_cleaned p
ON t.Project_ID = p.Project_ID
JOIN clients_cleaned c
ON p.Client_ID = c.Client_ID
GROUP BY c.Client_Name
ORDER BY Total_Hours DESC;



-- Q17. What is the labor cost by employee?


SELECT e.Employee_Name, SUM(t.Hours_Worked * e.Hourly_Cost) AS Labor_Cost FROM timelogs_cleaned t
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
GROUP BY e.Employee_Name
ORDER BY Labor_Cost DESC;



-- Q18. What is the labor cost by project?


SELECT p.Project_ID, SUM(t.Hours_Worked * e.Hourly_Cost) AS Labor_Cost FROM timelogs_cleaned t
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
JOIN projects_cleaned p
ON t.Project_ID = p.Project_ID
GROUP BY p.Project_ID
ORDER BY Labor_Cost DESC;



-- Q19. What is the profitability of each project?
-- Profit = Revenue - Labor Cost


SELECT p.Project_ID, p.Project_Value, SUM(t.Hours_Worked * e.Hourly_Cost) AS Labor_Cost,
(p.Project_Value - SUM(t.Hours_Worked * e.Hourly_Cost)) AS Profit FROM projects_cleaned p
JOIN timelogs_cleaned t
ON p.Project_ID = t.Project_ID
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
GROUP BY
p.Project_ID,
p.Project_Value
ORDER BY Profit DESC;



-- Q20. What is the budget variance for each project?
-- Actual Hours - Budget Hours


SELECT
p.Project_ID,
p.Budget_Hours,
SUM(t.Hours_Worked) AS Actual_Hours,
SUM(t.Hours_Worked) - p.Budget_Hours
AS Budget_Variance
FROM projects_cleaned p
JOIN timelogs_cleaned t
ON p.Project_ID = t.Project_ID
GROUP BY
p.Project_ID,
p.Budget_Hours
ORDER BY Budget_Variance DESC;



-- Q21. Which projects exceeded their budget hours?


SELECT
p.Project_ID,
p.Budget_Hours,
SUM(t.Hours_Worked) AS Actual_Hours
FROM projects_cleaned p
JOIN timelogs_cleaned t
ON p.Project_ID = t.Project_ID
GROUP BY
p.Project_ID,
p.Budget_Hours
HAVING SUM(t.Hours_Worked) > p.Budget_Hours;



-- Q22. What is the workload distribution across employees?


SELECT
e.Employee_Name,
e.Role,
SUM(t.Hours_Worked) AS Total_Hours
FROM timelogs_cleaned t
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
GROUP BY
e.Employee_Name,
e.Role
ORDER BY Total_Hours DESC;



-- Q23. Which employee roles generate the most billable hours?


SELECT
e.Role,
SUM(t.Hours_Worked) AS Billable_Hours
FROM timelogs_cleaned t
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
WHERE t.Billable = 'Yes'
GROUP BY e.Role
ORDER BY Billable_Hours DESC;



-- Q24. Revenue by project status


SELECT
Status,
SUM(Project_Value) AS Revenue
FROM projects_cleaned
GROUP BY Status
ORDER BY Revenue DESC;



-- Q25. Top 10 most profitable projects


SELECT p.Project_ID, (p.Project_Value - SUM(t.Hours_Worked * e.Hourly_Cost)) AS Profit FROM projects_cleaned p
JOIN timelogs_cleaned t
ON p.Project_ID = t.Project_ID
JOIN employees_cleaned e
ON t.Employee_ID = e.Employee_ID
GROUP BY p.Project_ID, p.Project_Value
ORDER BY Profit DESC
LIMIT 10;