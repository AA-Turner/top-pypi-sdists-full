from enum import Enum


class QosStrategyEnum(str, Enum):
    PROGRESSIVE = "progressive"
    THRESHOLD = "threshold"

    def __str__(self) -> str:
        return str(self.value)
