from enum import Enum


class GetRunProgressResponse200ItemStatus(str, Enum):
    FAILED = "failed"
    MATERIALIZED = "materialized"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
