from enum import Enum


class ProcessingStatusCode(str, Enum):
    """Possible statuses of a pipeline task."""

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
