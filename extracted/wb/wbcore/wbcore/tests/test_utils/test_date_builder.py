import re
from operator import add, sub

import pytest

from wbcore.utils.date_builder import (
    BusinessDay,
    Day,
    Hour,
    HourEnd,
    HourStart,
    Minute,
    MinuteEnd,
    MinuteStart,
    Month,
    MonthEnd,
    MonthStart,
    Quarter,
    QuarterEnd,
    QuarterStart,
    Second,
    SecondEnd,
    SecondStart,
    Week,
    WeekEnd,
    WeekStart,
    Year,
    YearEnd,
    YearStart,
)


class TestDateBuilder:
    @pytest.mark.parametrize(
        "component,name",
        [
            (SecondStart, "second_start"),
            (SecondEnd, "second_end"),
            (MinuteStart, "minute_start"),
            (MinuteEnd, "minute_end"),
            (HourStart, "hour_start"),
            (HourEnd, "hour_end"),
            (WeekStart, "week_start"),
            (WeekEnd, "week_end"),
            (MonthStart, "month_start"),
            (MonthEnd, "month_end"),
            (QuarterStart, "quarter_start"),
            (QuarterEnd, "quarter_end"),
            (YearStart, "year_start"),
            (YearEnd, "year_end"),
        ],
    )
    def test_component_str(self, component, name):
        assert str(component) == name

    @pytest.mark.parametrize(
        "offset, name",
        [
            (Second, "seconds"),
            (Minute, "minutes"),
            (Hour, "hours"),
            (Day, "days"),
            (BusinessDay, "bdays"),
            (Week, "weeks"),
            (Month, "months"),
            (Quarter, "quarters"),
            (Year, "years"),
        ],
    )
    @pytest.mark.parametrize("amount", [None, 2])
    def test_offset_str(self, offset, name, amount):
        if amount:
            assert str(offset(amount)) == f"{amount}{name}"
        else:
            assert str(offset) == f"1{name}"

    @pytest.mark.parametrize(
        "component",
        [
            SecondStart,
            SecondEnd,
            MinuteStart,
            MinuteEnd,
            HourStart,
            HourEnd,
            WeekStart,
            WeekEnd,
            MonthStart,
            MonthEnd,
            QuarterStart,
            QuarterEnd,
            YearStart,
            YearEnd,
        ],
    )
    @pytest.mark.parametrize("offset", [Second, Minute, Hour, Day, BusinessDay, Week, Month, Quarter, Year])
    @pytest.mark.parametrize("op", [add, sub])
    def test_component_with_offset(self, component, offset, op):
        results = re.findall("([a-z_]*)([+-]{1})([0-9a-z]*)", str(op(component, offset)))
        assert (
            len(results[0]) == 3
        )  # We expect three groups to be found, 1 for the component, 1 for the operator, and 1 for the offset

    @pytest.mark.parametrize(
        "component",
        [
            (SecondStart),
            (SecondEnd),
            (MinuteStart),
            (MinuteEnd),
            (HourStart),
            (HourEnd),
            (WeekStart),
            (WeekEnd),
            (MonthStart),
            (MonthEnd),
            (QuarterStart),
            (QuarterEnd),
            (YearStart),
            (YearEnd),
        ],
    )
    def test_repr(self, component):
        assert str(component) == repr(component)
