from enum import Enum


class ListRecentRunsResponse200ItemsItemRunsItemStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    RESOLVED = "resolved"
    RUNNING = "running"
    SUCCESS = "success"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
