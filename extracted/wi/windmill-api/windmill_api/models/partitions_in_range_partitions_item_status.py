from enum import Enum


class PartitionsInRangePartitionsItemStatus(str, Enum):
    FAILED = "failed"
    MATERIALIZED = "materialized"
    MISSING = "missing"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
