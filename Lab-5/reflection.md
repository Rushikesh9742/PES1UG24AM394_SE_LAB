# Reflection

## 1. What is static code analysis?

Static code analysis examines source code without running it, to find potential bugs, security vulnerabilities and style violations. Because it needs no execution or test data, it can catch problems early, such as the shell-injection risk in `os.system("xdg-open " + path)`, which never ran in the demo but was still dangerous.

## 2. What are the purposes of Pylint, Bandit and Flake8?

- **Pylint** is the strict code reviewer. It checks code quality and programming practice: naming, missing docstrings, broad exceptions, global statements and unused code. It also gives an overall score out of 10.
- **Bandit** is the security checker. It looks for insecure patterns such as shell execution, hard-coded passwords and unsafe temp-file handling, and rates each finding by severity and confidence.
- **Flake8** is the style checker. It enforces PEP 8 formatting: whitespace, blank lines and line length.

## 3. What improvements were achieved?

- **Pylint:** 5.27/10 to 10.00/10 (26 messages to none).
- **Bandit:** 4 findings (1 High, 2 Medium, 1 Low) to no issues.
- **Flake8:** 4 findings to none.

The main changes were replacing `os.system` with a shell-free call, switching from `tempfile.mktemp` to `mkstemp` and a non-hard-coded report folder, reading the sync password from an environment variable and comparing it safely, removing the broad `except Exception` and the `global` statement, renaming functions to snake_case, adding docstrings, and fixing the formatting issues. The program's output stayed byte-for-byte identical.

## 4. Why is static analysis useful?

It finds defects and risky patterns before the code is deployed, and it does so automatically and repeatably. It improves readability, maintainability and consistency across a team, and it provides measurable evidence of quality: the before and after reports show exactly what was fixed. It is cheap to run in a pre-commit hook or a CI pipeline, so problems are caught when they are easiest to fix.

## 5. What did this lab demonstrate?

The three tools complement each other. Pylint focuses on broad code quality, Bandit on security, and Flake8 on style, and each caught problems the others did not (for example, only Bandit flagged the injection risk, and only Pylint flagged the global state). Running them before and after the changes gave measurable verification that the code improved without changing its behavior.
