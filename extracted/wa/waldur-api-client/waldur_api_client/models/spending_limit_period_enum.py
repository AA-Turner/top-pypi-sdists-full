from enum import Enum


class SpendingLimitPeriodEnum(str, Enum):
    DAY = "day"
    MONTH = "month"
    QUARTER = "quarter"
    TOTAL = "total"
    WEEK = "week"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
