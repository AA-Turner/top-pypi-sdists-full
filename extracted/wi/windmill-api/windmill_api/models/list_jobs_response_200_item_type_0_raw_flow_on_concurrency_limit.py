from enum import Enum


class ListJobsResponse200ItemType0RawFlowOnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
