from enum import Enum


class RecentRunStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    RESOLVED = "resolved"
    RUNNING = "running"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
