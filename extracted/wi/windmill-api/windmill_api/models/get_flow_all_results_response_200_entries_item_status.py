from enum import Enum


class GetFlowAllResultsResponse200EntriesItemStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    QUEUED = "queued"
    RUNNING = "running"
    SKIPPED = "skipped"
    SUCCESS = "success"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
