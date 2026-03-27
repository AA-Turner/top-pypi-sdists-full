"""Tests for cron expression evaluator (#969)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from anteroom.services.cron import min_interval_seconds, parse_cron


class TestParseCron:
    def test_every_minute(self) -> None:
        c = parse_cron("* * * * *")
        assert c.minutes == frozenset(range(60))

    def test_specific_values(self) -> None:
        c = parse_cron("0 12 1 6 3")
        assert c.minutes == frozenset({0})
        assert c.hours == frozenset({12})
        assert c.days == frozenset({1})
        assert c.months == frozenset({6})
        assert c.dows == frozenset({3})

    def test_range(self) -> None:
        c = parse_cron("1-5 * * * *")
        assert c.minutes == frozenset({1, 2, 3, 4, 5})

    def test_step(self) -> None:
        c = parse_cron("*/15 * * * *")
        assert c.minutes == frozenset({0, 15, 30, 45})

    def test_list(self) -> None:
        c = parse_cron("0,30 * * * *")
        assert c.minutes == frozenset({0, 30})

    def test_range_with_step(self) -> None:
        c = parse_cron("1-10/3 * * * *")
        assert c.minutes == frozenset({1, 4, 7, 10})

    def test_alias_hourly(self) -> None:
        c = parse_cron("@hourly")
        assert c.minutes == frozenset({0})
        assert c.hours == frozenset(range(24))

    def test_alias_daily(self) -> None:
        c = parse_cron("@daily")
        assert c.minutes == frozenset({0})
        assert c.hours == frozenset({0})

    def test_alias_weekly(self) -> None:
        c = parse_cron("@weekly")
        assert c.dows == frozenset({0})  # Sunday

    def test_alias_monthly(self) -> None:
        c = parse_cron("@monthly")
        assert c.days == frozenset({1})


class TestParseCronErrors:
    def test_wrong_field_count(self) -> None:
        with pytest.raises(ValueError, match="5 fields"):
            parse_cron("* * *")

    def test_value_out_of_range_minute(self) -> None:
        with pytest.raises(ValueError, match="outside"):
            parse_cron("60 * * * *")

    def test_value_out_of_range_hour(self) -> None:
        with pytest.raises(ValueError, match="outside"):
            parse_cron("* 25 * * *")

    def test_value_out_of_range_day(self) -> None:
        with pytest.raises(ValueError, match="outside"):
            parse_cron("* * 32 * *")

    def test_value_out_of_range_month(self) -> None:
        with pytest.raises(ValueError, match="outside"):
            parse_cron("* * * 13 *")

    def test_invalid_step(self) -> None:
        with pytest.raises(ValueError, match="invalid step"):
            parse_cron("*/0 * * * *")

    def test_invalid_value(self) -> None:
        with pytest.raises(ValueError, match="invalid value"):
            parse_cron("abc * * * *")

    def test_inverted_range(self) -> None:
        with pytest.raises(ValueError, match="outside"):
            parse_cron("5-1 * * * *")


class TestNextOccurrence:
    def test_next_minute(self) -> None:
        c = parse_cron("30 * * * *")
        after = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
        nxt = c.next_occurrence(after)
        assert nxt == datetime(2025, 1, 1, 12, 30, tzinfo=timezone.utc)

    def test_next_hour(self) -> None:
        c = parse_cron("0 14 * * *")
        after = datetime(2025, 1, 1, 15, 0, tzinfo=timezone.utc)
        nxt = c.next_occurrence(after)
        assert nxt == datetime(2025, 1, 2, 14, 0, tzinfo=timezone.utc)

    def test_next_day(self) -> None:
        c = parse_cron("0 0 15 * *")
        after = datetime(2025, 1, 16, 0, 0, tzinfo=timezone.utc)
        nxt = c.next_occurrence(after)
        assert nxt == datetime(2025, 2, 15, 0, 0, tzinfo=timezone.utc)

    def test_month_boundary(self) -> None:
        c = parse_cron("0 0 1 3 *")
        after = datetime(2025, 3, 2, 0, 0, tzinfo=timezone.utc)
        nxt = c.next_occurrence(after)
        assert nxt == datetime(2026, 3, 1, 0, 0, tzinfo=timezone.utc)

    def test_impossible_raises(self) -> None:
        """Feb 30 never exists — should raise after 4-year cap."""
        c = parse_cron("0 0 30 2 *")
        after = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
        with pytest.raises(ValueError, match="No matching datetime"):
            c.next_occurrence(after)

    def test_leap_year(self) -> None:
        c = parse_cron("0 0 29 2 *")
        after = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
        nxt = c.next_occurrence(after)
        assert nxt.month == 2 and nxt.day == 29

    def test_dow_filter(self) -> None:
        """0 = Sunday in cron."""
        c = parse_cron("0 12 * * 0")
        after = datetime(2025, 1, 6, 0, 0, tzinfo=timezone.utc)  # Monday
        nxt = c.next_occurrence(after)
        assert nxt.weekday() == 6  # Python Sunday = 6


class TestCronEdgeCases:
    """Edge cases for cron parsing and evaluation."""

    def test_empty_segment_raises(self) -> None:
        with pytest.raises(ValueError, match="empty segment"):
            parse_cron(",5 * * * *")

    def test_non_digit_step_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid step"):
            parse_cron("*/abc * * * *")

    def test_non_digit_range_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid range"):
            parse_cron("a-b * * * *")

    def test_dow_sunday_is_zero(self) -> None:
        c = parse_cron("0 0 * * 0")
        assert 0 in c.dows

    def test_matches_specific_datetime(self) -> None:
        c = parse_cron("30 14 15 6 *")
        dt = datetime(2025, 6, 15, 14, 30, tzinfo=timezone.utc)
        assert c.matches(dt)

    def test_does_not_match_wrong_minute(self) -> None:
        c = parse_cron("30 14 * * *")
        dt = datetime(2025, 6, 15, 14, 29, tzinfo=timezone.utc)
        assert not c.matches(dt)

    def test_multiple_months(self) -> None:
        c = parse_cron("0 0 1 1,6,12 *")
        assert c.months == frozenset({1, 6, 12})


class TestMinInterval:
    def test_every_minute(self) -> None:
        c = parse_cron("* * * * *")
        assert min_interval_seconds(c) == 60

    def test_every_15_minutes(self) -> None:
        c = parse_cron("*/15 * * * *")
        assert min_interval_seconds(c) == 900

    def test_hourly(self) -> None:
        c = parse_cron("@hourly")
        assert min_interval_seconds(c) == 3600

    def test_daily(self) -> None:
        c = parse_cron("@daily")
        assert min_interval_seconds(c) == 86400
