import pandas as pd

# ==========================
# DATE FORMAT
# ==========================

DATE_FORMAT = "%d-%m-%Y"

# ==========================
# LOAD DATA
# ==========================

clients = pd.read_csv("Raw_Data/Clients.csv")
employees = pd.read_csv("Raw_Data/Employees.csv")
projects = pd.read_csv("Raw_Data/Projects.csv")
timelogs = pd.read_csv("Raw_Data/TimeLogs.csv")

# ==========================
# VALIDATION RESULTS
# ==========================

validation_results = []

# ==========================
# CLIENTS VALIDATION
# ==========================

missing_client_values = clients.isnull().sum().sum()

duplicate_client_ids = clients["Client_ID"].duplicated().sum()

validation_results.append(["Missing Client Values", missing_client_values])

validation_results.append(["Duplicate Client IDs", duplicate_client_ids])

# ==========================
# EMPLOYEES VALIDATION
# ==========================

missing_employee_values = employees.isnull().sum().sum()

duplicate_employee_ids = employees["Employee_ID"].duplicated().sum()

validation_results.append(["Missing Employee Values", missing_employee_values])

validation_results.append(["Duplicate Employee IDs", duplicate_employee_ids])

# ==========================
# PROJECTS VALIDATION
# ==========================

missing_project_values = projects.isnull().sum().sum()

duplicate_project_ids = projects["Project_ID"].duplicated().sum()

validation_results.append(["Missing Project Values", missing_project_values])

validation_results.append(["Duplicate Project IDs", duplicate_project_ids])

# --------------------------
# INVALID STATUS VALUES
# --------------------------

valid_status = [
    "Completed",
    "Active",
    "On Hold",
    "Delayed"
]

invalid_status_count = (~projects["Status"].isin(valid_status)).sum()

validation_results.append(["Invalid Status Values", invalid_status_count])

# --------------------------
# INVALID PROJECT DATES
# --------------------------

invalid_start_dates = pd.to_datetime(projects["Start_Date"], format=DATE_FORMAT, errors="coerce").isnull().sum()

invalid_end_dates = pd.to_datetime(projects["End_Date"], format=DATE_FORMAT, errors="coerce").isnull().sum()

validation_results.append(["Invalid Project Start Dates", invalid_start_dates])

validation_results.append(["Invalid Project End Dates", invalid_end_dates])

# ==========================
# TIMELOGS VALIDATION
# ==========================

missing_timelog_values = timelogs.isnull().sum().sum()

duplicate_log_ids = timelogs["Log_ID"].duplicated().sum()

validation_results.append(["Missing TimeLog Values", missing_timelog_values])

validation_results.append(["Duplicate Log IDs", duplicate_log_ids])

# --------------------------
# INVALID EMPLOYEE IDS
# --------------------------

valid_employee_ids = set(employees["Employee_ID"])

invalid_employee_ids = (~timelogs["Employee_ID"].isin(valid_employee_ids)).sum()

validation_results.append(["Invalid Employee IDs", invalid_employee_ids])

# --------------------------
# INVALID PROJECT IDS
# --------------------------

valid_project_ids = set(projects["Project_ID"])

invalid_project_ids = (~timelogs["Project_ID"].isin(valid_project_ids)).sum()

validation_results.append(["Invalid Project IDs", invalid_project_ids])

# --------------------------
# NEGATIVE HOURS
# --------------------------

negative_hours = (timelogs["Hours_Worked"] < 0).sum()

validation_results.append(["Negative Hours", negative_hours])

# --------------------------
# INVALID TIMELOG DATES
# --------------------------

invalid_timelog_dates = pd.to_datetime(timelogs["Date"], format=DATE_FORMAT, errors="coerce").isnull().sum()

validation_results.append(["Invalid TimeLog Dates", invalid_timelog_dates])

# ==========================
# CREATE REPORT
# ==========================

report_df = pd.DataFrame(validation_results, columns=["Validation_Check", "Count"])

# ==========================
# SAVE REPORT
# ==========================

report_df.to_csv("Validation_Report.csv",index=False)

# ==========================
# PRINT REPORT
# ==========================

print("\n" + "=" * 50)
print("VALIDATION REPORT")
print("=" * 50)

print(report_df)

print("\nValidation completed successfully.")
print(
    "\nReport saved to: Validation_Report.csv"
)