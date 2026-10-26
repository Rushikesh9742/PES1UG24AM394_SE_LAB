# Issues Found in `expense_tracker.py`

Tools: Bandit (security), Pylint (quality), Flake8 (style). Ordered by severity, high and medium first.
"Before" reports are in `before/`, "after" reports in `after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection via `os.system` (Bandit B605, **High**) | Security | 61 | `os.system("xdg-open " + path)` runs through a shell, so a path such as `x; rm -rf ~` executes arbitrary commands. | Removed the shell entirely. `open_statement` resolves the path, checks it is a real file, and opens it with `webbrowser.open(file_uri)`. |
| Deprecated, race-prone `tempfile.mktemp` (Bandit B306, **Medium**) | Security | 55 | `mktemp` only returns a name without creating the file, so another process can create or symlink it first (TOCTOU race). | Replaced with `tempfile.mkstemp`, which atomically creates the file with safe permissions; the descriptor is closed and the path returned. |
| Hard-coded `/tmp` directory (Bandit B108, **Medium**) | Security | 8 | `REPORT_DIR = "/tmp/expense_reports"` is a predictable, world-writable location; also not portable to Windows. | `REPORT_DIR` now built from `tempfile.gettempdir()`, and `export_report` creates it with `os.makedirs(..., mode=0o700)`. |
| Hard-coded password (Bandit B105, Low) | Security | 5, 49-50 | `BANK_SYNC_PASSWORD = "demo-sync-pass"` is committed in source, and compared with `==` (timing side-channel). | Secret is read from the `BANK_SYNC_PASSWORD` environment variable; rejected if unset; compared with `hmac.compare_digest`. |
| Overly broad `except Exception` (Pylint W0718) | Bug / Quality | 39-42 | Catching every exception hides real bugs (e.g. a missing `"amount"` key would silently return `None`). | Removed the try/except; `max(..., default=None)` handles the only expected case (empty list). |
| Global mutable state + `global` statement (Pylint W0603, C0103) | Design | 6-7, 28-30, 33-35 | `expenses` and `monthly_budget` are module globals modified via `global`, which is hard to test and reason about. | Introduced an `ExpenseTracker` class holding `expenses` and `monthly_budget` as instance state. |
| `range(len(...))` loop (Pylint C0200) | Quality | 45-46 | Indexing by position is verbose and error-prone. | `for number, expense in enumerate(self.expenses, start=1)`. |
| Naming-style violations (Pylint C0103 x12) | Style | 7, 11, 20, 28, 33, 38, 44, 49, 53, 55, 59 | `addExpense`, `totalByCategory`, `setBudget`, `newBudget`, `reportPath`, etc. violate PEP 8 naming. | Renamed to `add_expense`, `total_by_category`, `set_budget`, `new_budget`, `report_path`, etc. |
| Missing docstrings (Pylint C0114 x1, C0116 x10) | Documentation | 1, 11-64 | Module and every function lack docstrings. | Added a module docstring and a docstring for every class, method and function. |
| Whitespace before `:` (Flake8 E203) | Style | 15 | `{"amount" : amount` | Reformatted dict literal as `"amount": amount`. |
| Missing blank line (Flake8 E302) | Style | 44 | Only 1 blank line before `def printLedger`. | Two blank lines between top-level definitions. |
| Inline comment spacing (Flake8 E261) | Style | 74 | Only one space before `# after setBudget`. | Two spaces before the inline comment. |
| Line too long, 93 > 79 (Flake8 E501) | Style | 77 | The final `print("Summary:" ...)` line exceeds the limit. | Wrapped the call over two lines. |
| Unguarded `main()` call (extra, not tool-reported) | Quality | 80 | `main()` runs on import, so importing the module (e.g. for tests) executes the demo. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.27/10 (26 messages) | **10.00/10** |
| Bandit | 4 issues (1 High, 2 Medium, 1 Low) | **0 issues** |
| Flake8 | 4 issues | **0 issues** |

Program output is byte-for-byte identical before and after (`before/program_output.txt` vs `after/program_output.txt`).
