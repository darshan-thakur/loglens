## Steps to set up the project

1. Run `make deps` in terminal.
2. Set/ensure correct database urls in `.env` file as per your system.
3. Run `make set_db` in terminal.
4. Run `make start` to run the server and start using api on localhost:8000.

NOTE: Steps 1-3 are one time setup. For subsequent runs direct step 4 can be executed.

Run `make ingest` to run ingest the file into database.

## Problem Statement

### REST API for Log File Data Access and Analysis

#### Problem Description:
You are given a directory containing log files with the format as below:
```
Timestamp\tLevel\tComponent\tMessage
2025-05-07 10:00:00\tINFO\tUserAuth\tUser 'john.doe' logged in successfully.
2025-05-07 10:00:15\tWARNING\tGeoIP\tCould not resolve IP address '192.168.1.100'.
2025-05-07 10:00:20\tERROR\tPayment\tTransaction failed for user 'jane.doe'.
2025-05-07 10:00:25\tINFO\tUserAuth\tUser 'alice.smith' logged out.
```
Your task is to develop a REST API using Python (with a framework like Flask or FastAPI) that allows users to access and analyze the data from these log files.\
Read and Parse Log Files: The API should be able to read log files from a specified directory. The log file format is the same as described above. The API should parse the timestamp, level, component, and message from each log entry.
##### API Endpoints: Implement the following API endpoints:

- GET /logs:\
Should return all log entries in a structured format (e.g., JSON).\
Should support optional query parameters for filtering:
    - level: Filter by log level (e.g., ?level=ERROR).
    - component: Filter by component (e.g., ?component=UserAuth).
    - start_time: Filter logs after this timestamp (e.g., ?start_time=2025-05-07 10:00:10).
    - end_time: Filter logs before this timestamp (e.g., ?end_time=2025-05-07 10:00:25).
- GET /logs/stats:\
Should return statistics about the log data, including:
Total number of log entries.
Counts of log entries per level.
Counts of log entries per component.
- GET /logs/{log_id}:\
Should return a specific log entry based on a unique log_id. You'll need to generate unique IDs for each log entry as you parse the files.

##### Data Handling:
The API should efficiently handle potentially large log files. Consider using techniques like pagination if needed (though it's not strictly required for this exercise).
##### Error Handling:
The API should return appropriate HTTP status codes and error messages for invalid requests (e.g., invalid query parameters, log ID not found).