"""Tests designed to exercise both outcomes of every decision branch."""

import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


@pytest.mark.parametrize(
    ("grade", "litres", "tier", "expected"),
    [
        ("unknown", 10, "silver", None),  # exception branch tested separately
        ("regular", -1, "silver", None),  # exception branch tested separately
        ("regular", 10, "silver", 0),     # extra <= 0
        ("regular", 20, "silver", 1050),  # extra > 0, non-diesel
        ("diesel", 25, "silver", 450),    # diesel rate
        ("regular", 50, "silver", 40 * 99),# extra > 30, non-gold
        ("regular", 50, "gold", 35 * 95), # gold discount
        ("diesel", 60, "gold", 40 * 80),  # gold does not add diesel coverage
    ],
)
def test_fuel_bill_decision_branches(grade, litres, tier, expected):
    if grade == "unknown":
        with pytest.raises(ValueError):
            fuel_bill(grade, litres, tier)
    elif litres < 0:
        with pytest.raises(ValueError):
            fuel_bill(grade, litres, tier)
    else:
        assert fuel_bill(grade, litres, tier) == expected


@pytest.mark.parametrize(
    ("litres", "containers", "fleet", "expected"),
    [
        (200, 3, True, True),   # fleet within limit
        (201, 1, True, False),  # fleet above limit
        (60, 1, False, True),   # non-fleet allowed
        (61, 1, False, False),  # non-fleet over litres limit
        (30, 2, False, False),  # too many containers
    ],
)
def test_pump_allowed_decision_branches(litres, containers, fleet, expected):
    assert pump_allowed(litres, containers, fleet) is expected


@pytest.mark.parametrize(
    ("seconds", "card", "night", "expected"),
    [
        (60, True, False, "active"),
        (45, True, False, "warning"),
        (44, True, False, "timed_out"),
        (30, False, False, "active"),
        (15, False, False, "warning"),
        (14, False, False, "timed_out"),
        (90, True, True, "active"),
        (75, True, True, "warning"),
    ],
)
def test_session_status_decision_branches(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected
