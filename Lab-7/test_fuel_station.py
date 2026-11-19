import math
from hypothesis import given, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill


def _assert_value_or_clean_rejection(function, value, validator):
    """Malformed fuzz inputs may raise ValueError, but must not crash otherwise."""
    try:
        result = function(value)
    except ValueError:
        return
    validator(result)


def _valid_purchase(result):
    assert isinstance(result, tuple) and len(result) == 2
    grade, litres = result
    assert isinstance(grade, str) and grade
    assert isinstance(litres, (int, float))
    assert math.isfinite(litres) and litres >= 0


def _valid_average(result):
    assert isinstance(result, int)
    assert result >= 0


def _valid_bill(result):
    assert isinstance(result, (int, float))
    assert math.isfinite(result)
    assert result >= 0


@given(st.one_of(st.text(), st.none()))
def test_parse_purchase_no_crash(s):
    _assert_value_or_clean_rejection(parse_purchase, s, _valid_purchase)


@given(st.one_of(st.text(), st.none()))
def test_volume_average_no_crash(s):
    _assert_value_or_clean_rejection(volume_average, s, _valid_average)


@given(st.one_of(st.text(), st.none()))
def test_payable_bill_no_crash(s):
    _assert_value_or_clean_rejection(payable_bill, s, _valid_bill)
