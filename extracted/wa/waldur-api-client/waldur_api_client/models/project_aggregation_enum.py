from enum import Enum


class ProjectAggregationEnum(str, Enum):
    MEAN = "mean"
    SUM = "sum"

    def __str__(self) -> str:
        return str(self.value)
