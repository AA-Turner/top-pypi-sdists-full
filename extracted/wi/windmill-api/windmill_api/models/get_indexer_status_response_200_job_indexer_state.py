from enum import Enum


class GetIndexerStatusResponse200JobIndexerState(str, Enum):
    NEVER_STARTED = "never_started"
    RUNNING = "running"
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
