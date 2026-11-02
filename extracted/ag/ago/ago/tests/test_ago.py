from __future__ import print_function

import pytest
from datetime import datetime, timedelta, tzinfo

from ..ago import human
from ..ago import delta2dict
from ..ago import extract_components
from ..ago import format_components
from ..ago import get_delta_from_subject

# datetime objects
PRESENT = datetime.now()
PAST = PRESENT - timedelta(492, 58711, 45)  # days, secs, microseconds
FUTURE = PRESENT + timedelta(2, 12447, 967742)  # days, secs, microseconds

# timedelta objects
PAST_DELTA = PRESENT - PAST
FUTURE_DELTA = PRESENT - FUTURE
ONE_YEAR_FOUR_HOURS_DELTA = timedelta(365, 14400, 0)


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC.

    Adapted from Python's documentation about tzinfo objects:
    https://docs.python.org/2.7/library/datetime.html#tzinfo-objects
    """

    def __init__(self, offset):
        self._offset = timedelta(minutes=offset)

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return "Test"

    def dst(self, dt):
        return timedelta(0)


def test_human_passed_datetime_is_string():
    assert isinstance(human(PAST), str)


def test_human_passed_timedelta_is_string():
    assert isinstance(human(PAST_DELTA), str)


def test_delta2dict_is_dict():
    assert isinstance(delta2dict(PAST_DELTA), dict)


def test_ago_in_past_human():
    assert "ago" in human(PAST)


def test_in_in_future_human():
    assert "in" in human(FUTURE)


def test_no_coma_in_one_precision():
    assert "," not in human(PAST, precision=1)
    assert "," not in human(FUTURE, precision=1)


def test_coma_in_three_precision():
    assert "," in human(PAST, precision=3)
    assert "," in human(FUTURE, precision=3)


def test_coma_in_out_of_bounds_precision():
    assert "," in human(PAST, precision=10)
    assert "," in human(FUTURE, precision=10)


def test_zero_day_is_skipped_display_hour():
    _result = human(ONE_YEAR_FOUR_HOURS_DELTA, precision=2)
    assert "year" in _result
    # day is 0 so it is skipped, so we should show hours ...
    assert "hour" in _result


def test_one_day_singular():
    assert "s" not in human(timedelta(1))


def test_two_day_plural():
    assert "s" in human(timedelta(2))


def test_abbreviation():
    assert "2d ago" in human(timedelta(2), abbreviate=True)
    assert "3d, 12h ago" in human(timedelta(3.5), abbreviate=True)
    assert "2h, 24m ago" in human(timedelta(.1), abbreviate=True)
    assert "1y, 35d ago" in human(timedelta(400), abbreviate=True)


def test_timestamp_integer():
    result = human(1474485467933 / 1000, precision=6)
    assert "minute" in result
    assert "second" in result
    assert "ago" in result


def test_timestamp_float():
    result = human(1474485467933 / 1000.0, precision=6)
    assert "minute" in result
    assert "second" in result
    assert "ago" in result


def test_past_tense():
    output = human(
        PAST,
        past_tense="titanic sunk {} ago",
        future_tense="titanic will sink in {} from now",
    )
    assert "titanic sunk" in output


def test_future_tense():
    output = human(
        FUTURE,
        past_tense="titanic sunk {} ago",
        future_tense="titanic will sink in {} from now",
    )
    assert "titanic will sink in" in output


def test_valid_past_dict():
    past_dict = delta2dict(PAST_DELTA)
    assert past_dict["year"] == 1
    assert past_dict["day"] == 127
    assert past_dict["hour"] == 16
    assert past_dict["minute"] == 18
    assert past_dict["microsecond"] == 45


def test_valid_future_dict():
    past_dict = delta2dict(FUTURE_DELTA)
    assert past_dict["year"] == 0
    assert past_dict["day"] == 2
    assert past_dict["hour"] == 3
    assert past_dict["minute"] == 27
    assert past_dict["millisecond"] == 967
    assert past_dict["microsecond"] == 742


def test_timezone_support():
    # test a naive datetime with no timezone
    # (add an extra minute to ensure it stays over an hour ahead during test)
    dt = datetime.now() + timedelta(minutes=61)
    output = human(dt)
    assert output.startswith("in 1 hour")

    # test a timezone-aware datetime with a UTC-2 timezone
    dt = datetime.now(tz=FixedOffset(-120)) + timedelta(minutes=61)
    output = human(dt)
    assert output.startswith("in 1 hour")


# --- Tests for extract_components ---

def test_extract_components_returns_list():
    assert isinstance(extract_components(PAST_DELTA), list)


def test_extract_components_filters_zeros():
    # timedelta with only days and hours, no minutes/seconds
    td = timedelta(days=2, hours=3)
    components = extract_components(td)
    assert len(components) == 2
    assert components[0]["unit"] == "day"
    assert components[0]["value"] == 2
    assert components[1]["unit"] == "hour"
    assert components[1]["value"] == 3


def test_extract_components_empty_for_zero_delta():
    components = extract_components(timedelta(0))
    assert components == []


def test_extract_components_has_required_keys():
    components = extract_components(PAST_DELTA)
    for comp in components:
        assert "unit" in comp
        assert "abbr" in comp
        assert "value" in comp


# --- Tests for format_components ---

def test_format_components_returns_string():
    components = extract_components(PAST_DELTA)
    assert isinstance(format_components(components), str)


def test_format_components_precision_limits_output():
    components = extract_components(PAST_DELTA)
    result = format_components(components, precision=1)
    assert "," not in result


def test_format_components_abbreviate():
    components = extract_components(timedelta(days=2, hours=3))
    result = format_components(components, abbreviate=True)
    assert "2d" in result
    assert "3h" in result


def test_format_components_plural():
    components = extract_components(timedelta(days=2))
    result = format_components(components)
    assert "days" in result


def test_format_components_singular():
    components = extract_components(timedelta(days=1))
    result = format_components(components)
    assert "day" in result
    assert "days" not in result


def test_format_components_empty_list():
    result = format_components([])
    assert result == ""


# --- Tests for get_delta_from_subject ---

def test_get_delta_from_subject_timedelta():
    td = timedelta(hours=2)
    delta, is_past = get_delta_from_subject(td)
    assert delta == td
    assert is_past is True


def test_get_delta_from_subject_negative_timedelta():
    td = timedelta(hours=-2)
    delta, is_past = get_delta_from_subject(td)
    assert delta == td
    assert is_past is False


def test_get_delta_from_subject_datetime():
    past_dt = datetime.now() - timedelta(hours=2)
    delta, is_past = get_delta_from_subject(past_dt)
    assert is_past is True
    assert delta.days == 0
    assert delta.seconds // 3600 == 2


def test_get_delta_from_subject_future_datetime():
    future_dt = datetime.now() + timedelta(hours=2)
    delta, is_past = get_delta_from_subject(future_dt)
    assert is_past is False


def test_get_delta_from_subject_timestamp():
    import time
    ts = time.time() - 3600  # 1 hour ago
    delta, is_past = get_delta_from_subject(ts)
    assert is_past is True


def test_get_delta_from_subject_invalid_type():
    with pytest.raises(TypeError):
        get_delta_from_subject("not a valid type")


# --- Edge case: "just now" ---

def test_just_now():
    result = human(timedelta(0))
    assert result == "just now"


def test_just_now_with_custom_tense():
    # Even with custom tense, "just now" should be returned for zero delta
    result = human(timedelta(0), past_tense="custom {} ago")
    assert result == "just now"


# --- delta2dict with negative timedelta ---

def test_delta2dict_negative_timedelta():
    neg_delta = timedelta(hours=-2, minutes=-30)
    result = delta2dict(neg_delta)
    assert result["hour"] == 2
    assert result["minute"] == 30


# --- precision=0 ---

def test_precision_zero():
    result = human(PAST, precision=0)
    assert result == " ago"  # No components selected, so empty string in tense format


# --- precision=1 with various inputs ---

def test_precision_one_various():
    assert "," not in human(timedelta(days=5, hours=3, minutes=20), precision=1)
    assert "5 days ago" in human(timedelta(days=5, hours=3, minutes=20), precision=1)


def test_precision_one_abbreviate():
    result = human(timedelta(days=5, hours=3), precision=1, abbreviate=True)
    assert result == "5d ago"


def test_precision_one_future():
    result = human(datetime.now() + timedelta(days=3, hours=2), precision=1)
    assert result == "in 3 days"


def example_usage():
    """Test and example usage"""

    print("\nTest past tense:\n")
    print(delta2dict(PAST_DELTA))
    print("Commented " + human(PAST_DELTA, 1))
    print(human(PAST, past_tense="Commented {} ago"))

    print(human(ONE_YEAR_FOUR_HOURS_DELTA, past_tense="Posted {} ago"))

    print("\nTest future tense:\n")
    print(delta2dict(FUTURE_DELTA))
    print("Shutdown " + human(FUTURE_DELTA, 5))
    print(human(FUTURE, future_tense="Shutdown in {} from now"))
    print("")


if __name__ == "__main__":
    example_usage()
