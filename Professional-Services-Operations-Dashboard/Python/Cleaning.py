import pandas as pd

# ==========================
# LOAD DATA
# ==========================

clients = pd.read_csv("Raw_Data/Clients.csv")
employees = pd.read_csv("Raw_Data/Employees.csv")
projects = pd.read_csv("Raw_Data/Projects.csv")
timelogs = pd.read_csv("Raw_Data/TimeLogs.csv")




# ==========================
# REMOVE DUPLICATES
# ==========================    

clients = clients.drop_duplicates()
employees = employees.drop_duplicates()
projects = projects.drop_duplicates()
timelogs = timelogs.drop_duplicates()

# ==========================
# REMOVE MISSING VALUES
# ==========================


clients = clients.dropna()
employees = employees.dropna()
projects = projects.dropna()
timelogs = timelogs.dropna()

# ==========================
# STANDARDIZE STATUS VALUES
# ==========================

projects["Status"] = projects["Status"].replace({
    "complete": "Completed",
    "completed": "Completed",
    "COMPLETE": "Completed",
    "ACTIVE": "Active",
    "active": "Active",
    "ON HOLD": "On Hold",
    "on hold": "On Hold",
    "DELAYED": "Delayed",
    "delayed": "Delayed"
})

# ==========================
# REMOVE INVALID EMPLOYEE IDs
# ==========================

valid_employee_ids = set(employees["Employee_ID"])

timelogs = timelogs[
    timelogs["Employee_ID"].isin(valid_employee_ids)
]

# ==========================
# REMOVE INVALID PROJECT IDs
# ==========================

valid_project_ids = set(projects["Project_ID"])

timelogs = timelogs[
    timelogs["Project_ID"].isin(valid_project_ids)
]

# ==========================
# REMOVE NEGATIVE HOURS
# ==========================

timelogs = timelogs[
    timelogs["Hours_Worked"] >= 0
]

# ==========================
# FIX DATES
# Convert DD-MM-YYYY
# To YYYY-MM-DD
# ==========================

projects["Start_Date"] = pd.to_datetime(
    projects["Start_Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

projects["End_Date"] = pd.to_datetime(
    projects["End_Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

timelogs["Date"] = pd.to_datetime(
    timelogs["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Remove invalid dates

projects = projects.dropna(
    subset=["Start_Date", "End_Date"]
)

timelogs = timelogs.dropna(
    subset=["Date"]
)

# Convert to standard format

projects["Start_Date"] = projects["Start_Date"].dt.strftime("%Y-%m-%d")

projects["End_Date"] = projects["End_Date"].dt.strftime("%Y-%m-%d")

timelogs["Date"] = timelogs["Date"].dt.strftime("%Y-%m-%d")




# ==========================
# SAVE CLEANED FILES
# ==========================

clients.to_csv(
    "Cleaned_Data/Clients_Cleaned.csv",
    index=False
)

employees.to_csv(
    "Cleaned_Data/Employees_Cleaned.csv",
    index=False
)

projects.to_csv(
    "Cleaned_Data/Projects_Cleaned.csv",
    index=False
)

timelogs.to_csv(
    "Cleaned_Data/TimeLogs_Cleaned.csv",
    index=False
)

# ==========================
# SUMMARY
# ==========================

print("\nData Cleaning Completed Successfully\n")

print("Cleaned files saved in Cleaned_Data folder.")