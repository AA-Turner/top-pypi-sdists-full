from enum import Enum


class MetricGoalPeriodEnum(str, Enum):
    MONTH = "month"
    QUARTER = "quarter"
    ROLLING_30D = "rolling_30d"

    def __str__(self) -> str:
        return str(self.value)
