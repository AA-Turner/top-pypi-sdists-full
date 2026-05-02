"""Unit tests for GenData date_sequence rule handler."""
import pytest
from datetime import date, timedelta

import pandas as pd

from flowtask.components.gendata.date_sequence import (
    DateSequenceRule,
    align_to_dow,
    generate_date_sequence,
)


class TestAlignToDow:
    """Tests for the align_to_dow helper function."""

    def test_align_monday_from_wednesday(self):
        """2024-01-03 (Wed) should shift to 2024-01-08 (Mon)."""
        result = align_to_dow(date(2024, 1, 3), 0)
        assert result == date(2024, 1, 8)
        assert result.weekday() == 0

    def test_align_already_on_target(self):
        """2024-01-01 (Mon) stays 2024-01-01 when dow=0."""
        result = align_to_dow(date(2024, 1, 1), 0)
        assert result == date(2024, 1, 1)

    def test_align_friday_from_monday(self):
        """2024-01-01 (Mon) should shift to 2024-01-05 (Fri) when dow=4."""
        result = align_to_dow(date(2024, 1, 1), 4)
        assert result == date(2024, 1, 5)
        assert result.weekday() == 4

    def test_align_sunday_from_saturday(self):
        """2024-01-06 (Sat) should shift to 2024-01-07 (Sun) when dow=6."""
        result = align_to_dow(date(2024, 1, 6), 6)
        assert result == date(2024, 1, 7)
        assert result.weekday() == 6

    def test_align_all_days(self):
        """Each dow=0..6 from a Monday base produces the correct weekday."""
        base = date(2024, 1, 1)  # Monday
        for dow in range(7):
            result = align_to_dow(base, dow)
            assert result.weekday() == dow
            assert result >= base


class TestDateSequenceRule:
    """Tests for the DateSequenceRule Pydantic model."""

    def test_valid_config(self):
        """Valid config creates a rule successfully."""
        rule = DateSequenceRule(
            column_name="test",
            firstdate=date(2024, 1, 1),
            lastdate=date(2024, 12, 31),
            interval=7,
            dow=0,
        )
        assert rule.column_name == "test"
        assert rule.interval == 7
        assert rule.dow == 0

    def test_string_dates(self):
        """String dates are parsed correctly."""
        rule = DateSequenceRule(
            column_name="test",
            firstdate="2024-01-01",
            lastdate="2024-12-31",
        )
        assert rule.firstdate == date(2024, 1, 1)
        assert rule.lastdate == date(2024, 12, 31)

    def test_invalid_interval(self):
        """interval < 1 raises validation error."""
        with pytest.raises(Exception):
            DateSequenceRule(
                column_name="test",
                firstdate=date(2024, 1, 1),
                lastdate=date(2024, 12, 31),
                interval=0,
            )

    def test_invalid_dow(self):
        """dow outside 0-6 raises validation error."""
        with pytest.raises(Exception):
            DateSequenceRule(
                column_name="test",
                firstdate=date(2024, 1, 1),
                lastdate=date(2024, 12, 31),
                dow=7,
            )

    def test_defaults(self):
        """Default values: interval=1, dow=None, date_format=None."""
        rule = DateSequenceRule(
            column_name="test",
            firstdate=date(2024, 1, 1),
            lastdate=date(2024, 1, 10),
        )
        assert rule.interval == 1
        assert rule.dow is None
        assert rule.date_format is None


class TestGenerateDateSequence:
    """Tests for the generate_date_sequence function."""

    def test_basic_daily(self):
        """Daily sequence from 2024-01-01 to 2024-01-10 produces 10 rows."""
        rule = DateSequenceRule(
            column_name="daily",
            firstdate=date(2024, 1, 1),
            lastdate=date(2024, 1, 10),
            interval=1,
        )
        series = generate_date_sequence(rule)
        assert len(series) == 10
        assert series.name == "daily"
        assert series.iloc[0] == date(2024, 1, 1)
        assert series.iloc[-1] == date(2024, 1, 10)

    def test_weekly_interval(self):
        """interval=7 produces weekly dates."""
        rule = DateSequenceRule(
            column_name="weekly",
            firstdate=date(2024, 1, 1),
            lastdate=date(2024, 1, 31),
            interval=7,
        )
        series = generate_date_sequence(rule)
        # Jan 1, 8, 15, 22, 29
        assert len(series) == 5
        for i in range(1, len(series)):
            diff = series.iloc[i] - series.iloc[i - 1]
            assert diff == timedelta(days=7)

    def test_dow_alignment_mondays(self):
        """dow=0 shifts start to first Monday and all dates are Mondays."""
        rule = DateSequenceRule(
            column_name="mondays",
            firstdate=date(2024, 1, 3),  # Wednesday
            lastdate=date(2024, 3, 31),
            interval=7,
            dow=0,
        )
        series = generate_date_sequence(rule)
        assert len(series) > 0
        # First date should be 2024-01-08 (first Monday after Jan 3)
        assert series.iloc[0] == date(2024, 1, 8)
        for d in series:
            assert d.weekday() == 0

    def test_dow_on_correct_day_no_shift(self):
        """If firstdate is already the target dow, no shift occurs."""
        rule = DateSequenceRule(
            column_name="mondays",
            firstdate=date(2024, 1, 1),  # Monday
            lastdate=date(2024, 1, 31),
            interval=7,
            dow=0,
        )
        series = generate_date_sequence(rule)
        assert series.iloc[0] == date(2024, 1, 1)

    def test_dow_all_days(self):
        """dow=0..6 each produce correct weekday alignment."""
        for dow in range(7):
            rule = DateSequenceRule(
                column_name=f"day_{dow}",
                firstdate=date(2024, 1, 1),
                lastdate=date(2024, 3, 31),
                interval=7,
                dow=dow,
            )
            series = generate_date_sequence(rule)
            assert len(series) > 0
            for d in series:
                assert d.weekday() == dow

    def test_single_day_range(self):
        """firstdate == lastdate with matching dow produces 1 row."""
        rule = DateSequenceRule(
            column_name="single",
            firstdate=date(2024, 1, 1),  # Monday
            lastdate=date(2024, 1, 1),
            interval=1,
            dow=0,
        )
        series = generate_date_sequence(rule)
        assert len(series) == 1
        assert series.iloc[0] == date(2024, 1, 1)

    def test_empty_when_range_too_short(self):
        """Range too short for dow alignment produces empty Series."""
        rule = DateSequenceRule(
            column_name="empty",
            firstdate=date(2024, 1, 1),  # Monday
            lastdate=date(2024, 1, 2),  # Tuesday
            interval=7,
            dow=5,  # Friday — first Friday is Jan 5, outside range
        )
        series = generate_date_sequence(rule)
        assert len(series) == 0

    def test_date_format(self):
        """date_format produces string output."""
        rule = DateSequenceRule(
            column_name="formatted",
            firstdate=date(2024, 1, 1),
            lastdate=date(2024, 1, 3),
            interval=1,
            date_format="%Y-%m-%d",
        )
        series = generate_date_sequence(rule)
        assert len(series) == 3
        assert series.iloc[0] == "2024-01-01"
        assert series.iloc[1] == "2024-01-02"
        assert series.iloc[2] == "2024-01-03"

    def test_date_format_custom(self):
        """Custom date_format like '%d/%m/%Y' works correctly."""
        rule = DateSequenceRule(
            column_name="custom_fmt",
            firstdate=date(2024, 1, 15),
            lastdate=date(2024, 1, 15),
            interval=1,
            date_format="%d/%m/%Y",
        )
        series = generate_date_sequence(rule)
        assert series.iloc[0] == "15/01/2024"

    def test_accepts_dict(self):
        """generate_date_sequence accepts a dict and converts to rule."""
        config = {
            "type": "date_sequence",
            "column_name": "from_dict",
            "firstdate": "2024-01-01",
            "lastdate": "2024-01-07",
            "interval": 1,
        }
        series = generate_date_sequence(config)
        assert len(series) == 7
        assert series.name == "from_dict"

    def test_realistic_weekly_mondays(self):
        """Realistic scenario: every Monday from 2024-01-01 to 2026-03-20."""
        rule = DateSequenceRule(
            column_name="weekly_date",
            firstdate=date(2024, 1, 1),
            lastdate=date(2026, 3, 20),
            interval=7,
            dow=0,
        )
        series = generate_date_sequence(rule)
        # 2024-01-01 is already a Monday
        assert series.iloc[0] == date(2024, 1, 1)
        assert series.iloc[-1] <= date(2026, 3, 20)
        # All should be Mondays
        for d in series:
            assert d.weekday() == 0
        # Verify interval
        for i in range(1, len(series)):
            assert series.iloc[i] - series.iloc[i - 1] == timedelta(days=7)
        # Approx 116-117 weeks
        assert 115 <= len(series) <= 118
