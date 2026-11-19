# L6_L7_47 — Fuel Station

## Lab 7: Fuzz Testing (Hypothesis)

This folder keeps the original Lab 7 application in `original_buggy/fuel_station.py`, the completed Hypothesis tests in `test_fuel_station.py`, and the corrected application in `fuel_station.py`. `fixed_fuel_station.py` is an extra copy of the final corrected application for easy restoration. Lab 6 files are retained unchanged.

### 1. Install dependencies (Windows CMD)

```bat
python -m pip install hypothesis pytest
```

### 2. Run the original buggy application (optional demonstration)

```bat
copy original_buggy\fuel_station.py fuel_station.py
python fuel_station.py
```

Try inputs such as `diesel:25`, an empty volume CSV, or a normal bill input. The original code has weak input validation.

### 3. Run Hypothesis against the original buggy application

```bat
python -m pytest -v test_fuel_station.py
```

This run is expected to find failures. Capture a screenshot of the failing test output. Hypothesis chooses and shrinks generated inputs; the exact failing example can vary.

### 4. Restore the fixed application

```bat
copy /Y fixed_fuel_station.py fuel_station.py
```

### 5. Run the tests again

```bat
python -m pytest -v test_fuel_station.py
```

All three property-based tests should pass. Capture a screenshot of the passing output.

### What the tests check

- `parse_purchase`: arbitrary text/None either produces a well-formed grade and finite non-negative litres, or is rejected with `ValueError`.
- `volume_average`: arbitrary text/None either produces a non-negative integer average, or is rejected with `ValueError`.
- `payable_bill`: arbitrary text/None either produces a finite non-negative bill, or is rejected with `ValueError`.

### Submission screenshots

1. Original application run.
2. Hypothesis failing tests against the original buggy code.
3. Fixed application run.
4. Hypothesis passing tests after the fix.

The original buggy source is preserved in `original_buggy/`. Do not overwrite or delete it.
