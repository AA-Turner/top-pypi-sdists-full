from enum import Enum


class ListExtendedJobsResponse200JobsItemType1RawFlowOnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
