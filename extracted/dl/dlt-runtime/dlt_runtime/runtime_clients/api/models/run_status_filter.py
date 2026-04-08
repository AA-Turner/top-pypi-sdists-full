from enum import Enum


class RunStatusFilter(str, Enum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    OTHER = "other"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
