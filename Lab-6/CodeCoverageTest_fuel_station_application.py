"""Tests focused on executing every statement in fuel_station.py."""

import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


@pytest.mark.parametrize(
    ("grade", "litres", "tier", "expected"),
    [
        ("regular", 8, "silver", 0),
        ("premium", 25, "silver", 1050),
        ("diesel", 25, "silver", 450),
        ("regular", 50, "gold", 3325),
    ],
)
def test_fuel_bill_statement_paths(grade, litres, tier, expected):
    assert fuel_bill(grade, litres, tier) == expected


@pytest.mark.parametrize(
    ("litres", "containers", "fleet", "expected"),
    [
        (30, 1, False, True),
        (50, 2, True, True),
        (70, 1, False, False),
    ],
)
def test_pump_allowed_statement_paths(litres, containers, fleet, expected):
    assert pump_allowed(litres, containers, fleet) is expected


@pytest.mark.parametrize(
    ("seconds", "card", "night", "expected"),
    [
        (90, True, False, "active"),
        (50, True, False, "warning"),
        (13, False, False, "timed_out"),
        (90, True, True, "active"),
    ],
)
def test_session_status_statement_paths(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected


def test_fuel_bill_invalid_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 10, "silver")


def test_fuel_bill_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")
