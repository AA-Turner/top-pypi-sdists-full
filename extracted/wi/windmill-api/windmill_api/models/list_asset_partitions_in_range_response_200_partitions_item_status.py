from enum import Enum


class ListAssetPartitionsInRangeResponse200PartitionsItemStatus(str, Enum):
    FAILED = "failed"
    MATERIALIZED = "materialized"
    MISSING = "missing"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
