from enum import Enum


class LimitPeriodEnum(str, Enum):
    ANNUAL = "annual"
    MONTH = "month"
    QUARTERLY = "quarterly"
    TOTAL = "total"

    def __str__(self) -> str:
        return str(self.value)
