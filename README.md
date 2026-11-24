# Courier and Parcel Tracking Management System
Scenario 26 • Register 116

## Start on Windows
1. Extract the ZIP. In VS Code choose File → Open Folder → courier. Open Terminal → New Terminal.
2. Run `java --version` and `python --version`. Use JDK 17 or newer and Python 3.10 or newer. If your Python command is py, first enter `$env:COURIER_PYTHON='py'` and use py for the Python commands below.
3. Run `java CourierApp.java`. Choose **3** to list records. Choose **8** and enter **DEMO-001** to see a completed shipment. Choose **9** for the four summary reports. Choose **0** to exit.
4. Generate charts with `python -m pip install -r analysis/requirements.txt`, then `python analysis/charts.py`. Open the PNG files in analysis/output.

## Book and deliver
Choose 4. Enter sender 1, receiver 2, type Books, weight 1.2, destination Erode, zone regional and service express. Expected charge INR 150. Copy your new CP tracking number. Use 5 to assign staff ID 1. Use 6 twice, first entering In Transit and then Out for Delivery, with a location each time. Use 7 to record Failed with a reason, then 7 again for Delivered. Use 8 for the complete history.

## Data and implementation
The included data/courier.db is a working SQLite database with nine synthetic shipments. No database server or password is needed. Java handles console operations, pricing, identifiers and promised dates. Python's standard sqlite3 module handles SQL through store.py. Analysis reads the same database. The assignment leaves rates and service times open. Project defaults are documented in the SRS.

To build a separate copy from SQL, run the following from this folder in PowerShell (use a new filename):
```
python -c "import sqlite3,pathlib; d=sqlite3.connect('practice.db'); d.executescript(pathlib.Path('sql/schema.sql').read_text()); d.executescript(pathlib.Path('sql/sample_data.sql').read_text()); d.close()"
```
To run Java against that practice copy set `$env:COURIER_DB='practice.db'`. Remove the override with `Remove-Item Env:COURIER_DB` before using the packaged data again. The chart script always reads data/courier.db.

## Submission map
docs contains the SRS, diagrams, database design and four subject write-ups. Software_Engineering.docx contains the test table. samples contains actual test transcripts from a separate fresh database and the analysis output from the nine demo shipments. The tracking number and booking date change each run. For GitHub upload the extracted folder contents, including README, SQL, charts and synthetic data.
