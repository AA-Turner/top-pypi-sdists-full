"""Date sequence rule handler for GenData.

Generates a pandas Series of dates from firstdate to lastdate
with a configurable interval and optional day-of-week alignment.
"""
from datetime import date, timedelta
from typing import Optional, Union

import pandas as pd
from pydantic import BaseModel, Field, field_validator


class DateSequenceRule(BaseModel):
    """Rule for generating a sequence of dates.

    Attributes:
        type: Rule type identifier, must be 'date_sequence'.
        column_name: Name of the output Series/column.
        firstdate: Start of date range (inclusive).
        lastdate: End of date range (inclusive).
        interval: Step size in days (must be >= 1).
        dow: Day of week to align to (0=Monday, 6=Sunday).
            If set, sequence starts on the first matching day >= firstdate.
        date_format: Optional strftime format for output. If set, the Series
            contains formatted strings instead of date objects.
    """

    type: str = Field("date_sequence", description="Rule type identifier")
    column_name: str = Field(..., description="Name of the output column")
    firstdate: date = Field(..., description="Start of date range (inclusive)")
    lastdate: date = Field(..., description="End of date range (inclusive)")
    interval: int = Field(default=1, ge=1, description="Step size in days")
    dow: Optional[int] = Field(
        default=None,
        ge=0,
        le=6,
        description="Day of week to align to (0=Monday, 6=Sunday)",
    )
    date_format: Optional[str] = Field(
        default=None,
        description="strftime format for output (e.g. '%Y-%m-%d')",
    )

    @field_validator("firstdate", "lastdate", mode="before")
    @classmethod
    def parse_date_string(cls, v: Union[str, date]) -> date:
        """Accept both date objects and ISO-format strings."""
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v


def align_to_dow(start: date, dow: int) -> date:
    """Shift a date forward to the first occurrence of the target weekday.

    Args:
        start: The starting date.
        dow: Target day of week (0=Monday, 6=Sunday).

    Returns:
        The first date >= start whose weekday matches dow.
    """
    days_ahead = dow - start.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start + timedelta(days=days_ahead)


def generate_date_sequence(rule: Union[DateSequenceRule, dict]) -> pd.Series:
    """Generate a Series of dates per the rule configuration.

    Args:
        rule: A DateSequenceRule instance or a dict with the same fields.

    Returns:
        A pd.Series named after rule.column_name containing date values
        (or formatted strings if date_format is set).
    """
    if isinstance(rule, dict):
        rule = DateSequenceRule(**rule)

    start = rule.firstdate
    if rule.dow is not None:
        start = align_to_dow(start, rule.dow)

    dates: list[date] = []
    current = start
    while current <= rule.lastdate:
        dates.append(current)
        current += timedelta(days=rule.interval)

    series = pd.Series(dates, name=rule.column_name)
    if rule.date_format and not series.empty:
        series = series.apply(lambda d: d.strftime(rule.date_format))
    return series
