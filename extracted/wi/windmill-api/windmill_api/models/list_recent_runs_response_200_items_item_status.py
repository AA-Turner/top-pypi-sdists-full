from enum import Enum


class ListRecentRunsResponse200ItemsItemStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    RUNNING = "running"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
