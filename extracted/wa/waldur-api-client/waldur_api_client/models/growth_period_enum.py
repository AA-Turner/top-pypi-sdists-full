from enum import Enum


class GrowthPeriodEnum(str, Enum):
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
