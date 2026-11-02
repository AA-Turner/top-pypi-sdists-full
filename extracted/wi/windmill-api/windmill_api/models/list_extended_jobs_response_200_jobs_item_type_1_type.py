from enum import Enum


class ListExtendedJobsResponse200JobsItemType1Type(str, Enum):
    QUEUEDJOB = "QueuedJob"

    def __str__(self) -> str:
        return str(self.value)
