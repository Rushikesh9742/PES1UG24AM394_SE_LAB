import math

VALID_GRADES = {"regular", "premium", "diesel"}


def parse_purchase(text):
    """Parse 'grade:litres'; reject malformed or unsafe values with ValueError."""
    if not isinstance(text, str):
        raise ValueError("purchase must be text in grade:litres format")
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("Use the format grade:litres")
    grade_text, litres_text = parts
    grade = grade_text.strip().lower()
    if not grade or grade not in VALID_GRADES:
        raise ValueError("unknown or empty fuel grade")
    try:
        litres = float(litres_text.strip())
    except (TypeError, ValueError):
        raise ValueError("litres must be a number") from None
    if not math.isfinite(litres) or litres < 0:
        raise ValueError("litres must be a finite non-negative number")
    return grade.title(), litres


def volume_average(volumes_csv):
    """Return the floor average of a non-empty CSV of non-negative integers."""
    if not isinstance(volumes_csv, str) or not volumes_csv.strip():
        raise ValueError("provide one or more comma-separated volumes")
    tokens = volumes_csv.split(",")
    try:
        values = [int(token.strip()) for token in tokens]
    except (TypeError, ValueError):
        raise ValueError("volumes must be comma-separated integers") from None
    if not values or any(value < 0 for value in values):
        raise ValueError("volumes must be non-negative")
    return sum(values) // len(values)


def payable_bill(text):
    """Calculate bill plus 18% tax minus discount, with a zero lower bound."""
    if not isinstance(text, str):
        raise ValueError("bill input must be text in bill|discount format")
    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("Use the format bill|discount")
    try:
        bill = float(parts[0].strip())
        discount = float(parts[1].strip())
    except (TypeError, ValueError):
        raise ValueError("bill and discount must be numbers") from None
    if not math.isfinite(bill) or not math.isfinite(discount):
        raise ValueError("bill and discount must be finite numbers")
    if bill < 0 or discount < 0:
        raise ValueError("bill and discount must be non-negative")
    total = bill * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    try:
        print("Grade and Litres:", parse_purchase(user_input))
    except ValueError as exc:
        print("Invalid purchase:", exc)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    try:
        print("Average Volume:", volume_average(user_input))
    except ValueError as exc:
        print("Invalid volumes:", exc)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    try:
        print("Payable Bill:", payable_bill(user_input))
    except ValueError as exc:
        print("Invalid bill:", exc)


if __name__ == "__main__":
    main()
