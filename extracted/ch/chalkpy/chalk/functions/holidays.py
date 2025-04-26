from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Literal, Optional, Union

from typing_extensions import TypeAlias


class DayOfWeek(int, Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


@dataclass(frozen=True)
class HolidayDayOfWeek:
    """A holiday that occurs on a specific day of the week, like the first Monday of January (New Year's Day)"""

    name: str
    """The name of the holiday"""

    month: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """The month in which the holiday occurs, 1 to 12"""

    day_of_week: DayOfWeek
    """The day of the week on which the holiday occurs"""

    nth_week: Literal[-1, 1, 2, 3, 4, 5]
    """The week of the month in which the holiday occurs. -1 means the last week of the month"""

    start_date: Optional[date] = None
    """The day in which the holiday is observed"""


@dataclass(frozen=True)
class HolidayDayOfMonth:
    """A holiday that occurs on a specific day of the month, like the 25th of December (Christmas Day)"""

    name: str
    """The name of the holiday"""

    month: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """The month in which the holiday occurs, 1 to 12"""

    day_of_month: int
    """The day of the month on which the holiday occurs, 1 to 31"""

    nearest_workday: bool
    """If True, the holiday is observed on the nearest workday if it falls on a weekend"""

    start_date: Optional[date] = None
    """The first year in which the holiday is observed"""


Holiday: TypeAlias = Union[HolidayDayOfWeek, HolidayDayOfMonth]

USMemorialDay = HolidayDayOfWeek(
    name="Memorial Day",
    month=5,
    day_of_week=DayOfWeek.MONDAY,
    nth_week=-1,
)

USLaborDay = HolidayDayOfWeek(
    name="Labor Day",
    month=9,
    day_of_week=DayOfWeek.MONDAY,
    nth_week=1,
)

USColumbusDay = HolidayDayOfWeek(
    name="Columbus Day",
    month=10,
    day_of_week=DayOfWeek.MONDAY,
    nth_week=2,
)

USThanksgivingDay = HolidayDayOfWeek(
    name="Thanksgiving Day",
    month=11,
    day_of_week=DayOfWeek.THURSDAY,
    nth_week=4,
)

USMartinLutherKingJr = HolidayDayOfWeek(
    name="Birthday of Martin Luther King, Jr.",
    month=1,
    start_date=date(1986, 1, 1),
    day_of_week=DayOfWeek.MONDAY,
    nth_week=3,
)

USPresidentsDay = HolidayDayOfWeek(
    name="Washington’s Birthday",
    month=2,
    day_of_week=DayOfWeek.MONDAY,
    nth_week=3,
)

NewYearsDay = HolidayDayOfMonth(
    name="New Year's Day",
    month=1,
    day_of_month=1,
    nearest_workday=True,
)

JuneteenthNationalIndependenceDay = HolidayDayOfMonth(
    name="Juneteenth National Independence Day",
    month=6,
    start_date=date(2021, 6, 18),
    day_of_month=19,
    nearest_workday=True,
)

IndependenceDay = HolidayDayOfMonth(
    name="Independence Day",
    month=7,
    day_of_month=4,
    nearest_workday=True,
)

VeteransDay = HolidayDayOfMonth(
    name="Veterans Day",
    month=11,
    day_of_month=11,
    nearest_workday=True,
)

ChristmasDay = HolidayDayOfMonth(
    name="Christmas Day",
    month=12,
    day_of_month=25,
    nearest_workday=True,
)

USFederalHolidays = [
    NewYearsDay,
    USMartinLutherKingJr,
    USPresidentsDay,
    USMemorialDay,
    JuneteenthNationalIndependenceDay,
    IndependenceDay,
    USLaborDay,
    USColumbusDay,
    VeteransDay,
    USThanksgivingDay,
    ChristmasDay,
]
