from enum import Enum


class OfferingMetricStateEnum(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
