import pytest
from datetime import datetime, timedelta
from trendspy.timeframe_utils import *
from trendspy.timeframe_utils import _is_valid_date, _is_valid_format, _extract_time_parts, _decode_trend_datetime
# Тесты
def test_is_valid_date():
    assert _is_valid_date('2024-09-13') is True
    assert _is_valid_date('2024-09-13T22') is True
    assert _is_valid_date('2024/09/13') is False
    assert _is_valid_date('invalid') is False

def test_is_valid_format():
    assert _is_valid_format('1-H') is True
    assert _is_valid_format('5-y') is True
    assert _is_valid_format('10-m') is True
    assert _is_valid_format('invalid') is False

def test_extract_time_parts():
    assert _extract_time_parts('5-H') == (5, 'H')
    assert _extract_time_parts('10-d') == (10, 'd')
    assert _extract_time_parts('invalid') is None

def test_decode_trend_datetime():
    assert _decode_trend_datetime('2024-09-13T22') == datetime(2024, 9, 13, 22)
    assert _decode_trend_datetime('2024-09-13') == datetime(2024, 9, 13)

def test_convert_timeframe():
    assert convert_timeframe('now 1-H') == 'now 1-H'
    assert convert_timeframe('2024-09-12T23 5-H') == '2024-09-12T18 2024-09-12T23'
    assert convert_timeframe('2024-09-12T23 1-d') == '2024-09-11T23 2024-09-12T23'
    assert convert_timeframe('2024-09-12 1-y') == '2023-09-12 2024-09-12'
    assert convert_timeframe('2024-09-12T23 2024-09-13') == '2024-09-12T23 2024-09-14T00'
    assert convert_timeframe('2024-09-12 2024-09-13T12') == '2024-09-12T00 2024-09-13T12'
    with pytest.raises(ValueError):
        convert_timeframe('2024-09-12T23 invalid')
    with pytest.raises(ValueError):
        convert_timeframe('2024-09-12T23 8-d')
    with pytest.raises(ValueError):
        convert_timeframe('2024-09-12T23 all')

def test_month_diff():
    assert convert_timeframe('2024-09-12 1-m') == '2024-08-13 2024-09-12'


def test_convert_timeframe_range():
    assert timeframe_to_timedelta('now 1-H') == timedelta(seconds=60*60)
    assert timeframe_to_timedelta('now 5-H') == timedelta(seconds=5*60*60)

if __name__ == "__main__":
    pytest.main()