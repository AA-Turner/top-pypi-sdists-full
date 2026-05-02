from datetime import timedelta

from cpsl.task_types import _parse_schedule_value


def test_parse_one_shot_schedule_value():
    delay, recurrence = _parse_schedule_value("5m")
    assert delay == timedelta(minutes=5)
    assert recurrence == 0


def test_parse_recurring_schedule_value():
    delay, recurrence = _parse_schedule_value("every 5 min")
    assert delay == timedelta(minutes=5)
    assert recurrence == 300
