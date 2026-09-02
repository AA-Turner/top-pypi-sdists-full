from enum import Enum


class DataMetricKind(str, Enum):
    DIMENSION = "dimension"
    MEASURE = "measure"

    def __str__(self) -> str:
        return str(self.value)
