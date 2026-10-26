"""Personal expense tracker.

Records expenses by category, rejects invalid amounts, totals spending per
category, tracks the remaining monthly budget, finds the biggest expense and
checks a bank-sync password.
"""

import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

DEFAULT_MONTHLY_BUDGET = 20000
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


class ExpenseTracker:
    """Keeps a list of expenses and a monthly budget."""

    def __init__(self, monthly_budget=DEFAULT_MONTHLY_BUDGET):
        self.expenses = []
        self.monthly_budget = monthly_budget

    def add_expense(self, amount, category="Misc", note=""):
        """Record an expense. Return False if the amount is not positive."""
        if amount <= 0:
            print("Ignoring invalid amount", amount)
            return False
        self.expenses.append({
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat(),
        })
        return True

    def total_by_category(self):
        """Return a dict mapping each category to its total spending."""
        totals = {}
        for expense in self.expenses:
            category = expense["category"]
            totals[category] = totals.get(category, 0) + expense["amount"]
        return totals

    def set_budget(self, new_budget):
        """Set the monthly budget."""
        self.monthly_budget = new_budget

    def remaining_budget(self):
        """Return the budget left after all recorded expenses."""
        spent = sum(expense["amount"] for expense in self.expenses)
        return self.monthly_budget - spent

    def biggest_expense(self):
        """Return the largest expense, or None if there are none."""
        return max(self.expenses, key=lambda expense: expense["amount"],
                   default=None)

    def print_ledger(self):
        """Print every expense with a running number."""
        for number, expense in enumerate(self.expenses, start=1):
            print(number, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password against the one stored in BANK_SYNC_PASSWORD.

    The secret is read from the environment, never hard-coded. If it is not
    configured, every password is rejected.
    """
    expected = os.environ.get("BANK_SYNC_PASSWORD")
    if not expected:
        return False
    return hmac.compare_digest(password.encode(), expected.encode())


def export_report():
    """Create a unique, private report file path and return it."""
    os.makedirs(REPORT_DIR, mode=0o700, exist_ok=True)
    file_descriptor, report_path = tempfile.mkstemp(suffix=".txt",
                                                    dir=REPORT_DIR)
    os.close(file_descriptor)
    return report_path


def open_statement(path):
    """Open a statement file in the default application (no shell used)."""
    statement = Path(path).resolve()
    if not statement.is_file():
        raise FileNotFoundError(f"No such statement: {statement}")
    return webbrowser.open(statement.as_uri())


def main():
    """Run a short demonstration."""
    tracker = ExpenseTracker()
    print("Biggest expense before any entries:", tracker.biggest_expense())
    tracker.add_expense(450, "Food", "Lunch with team")
    tracker.add_expense(1200, "Travel", "Cab to airport")
    tracker.add_expense(-50, "Food")
    tracker.add_expense(300, "Food", "Groceries")
    tracker.add_expense(999, "Bills", "Internet")
    tracker.set_budget(5000)
    tracker.print_ledger()
    print("Totals:", tracker.total_by_category())
    print("Remaining budget:", tracker.remaining_budget())  # after set_budget
    print("Biggest expense:", tracker.biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(tracker.expenses),
          "expenses recorded against a budget of", tracker.monthly_budget)


if __name__ == "__main__":
    main()
