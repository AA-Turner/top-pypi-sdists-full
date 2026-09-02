from enum import Enum


class MaterializedPartitionStatus(str, Enum):
    FAILED = "failed"
    MATERIALIZED = "materialized"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
