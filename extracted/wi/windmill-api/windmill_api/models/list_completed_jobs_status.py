from enum import Enum


class ListCompletedJobsStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    SKIPPED = "skipped"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
