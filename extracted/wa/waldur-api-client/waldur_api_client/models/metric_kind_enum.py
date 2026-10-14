from enum import Enum


class MetricKindEnum(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"

    def __str__(self) -> str:
        return str(self.value)
