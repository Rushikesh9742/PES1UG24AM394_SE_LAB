# Lab 6 – Code and Branch Coverage Analysis

## Application
Fuel Station application (`fuel_station.py`).

## What I did
For this lab, I wrote two separate pytest test files. The first file checks the application statements and normal/error cases. The second file checks the decision paths in the application using branch coverage.

I ran each test file separately with the `coverage` tool so that the two results could be checked independently.

## Test results
- Code coverage: 13 tests passed; 37 statements covered; 100% statement coverage.
- Branch coverage: 21 tests passed; 26 branches checked; 100% coverage; 0 partial branches.

Both results are also included as terminal screenshots in the `Screenshots` folder.

## Files included
- `fuel_station.py` – application being tested.
- `CodeCoverageTest_fuel_station_application.py` – tests for statement/code coverage.
- `BranchCoverageTest_fuel_station_application.py` – tests for branch coverage.
- `Screenshots/` – terminal evidence for both runs.
- `Lab6_Coverage_Report.pdf` – written report.

## Commands used

Code coverage:
```powershell
python -m coverage erase
python -m coverage run --source=fuel_station -m pytest -q CodeCoverageTest_fuel_station_application.py
python -m coverage report -m
```

Branch coverage:
```powershell
python -m coverage erase
python -m coverage run --branch --source=fuel_station -m pytest -q BranchCoverageTest_fuel_station_application.py
python -m coverage report -m
```
