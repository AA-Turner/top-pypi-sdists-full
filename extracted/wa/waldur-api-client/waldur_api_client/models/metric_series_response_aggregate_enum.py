from enum import Enum


class MetricSeriesResponseAggregateEnum(str, Enum):
    LAST = "last"
    MAX = "max"
    MEAN = "mean"
    MIN = "min"

    def __str__(self) -> str:
        return str(self.value)
