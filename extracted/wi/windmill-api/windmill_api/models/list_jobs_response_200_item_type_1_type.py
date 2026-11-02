from enum import Enum


class ListJobsResponse200ItemType1Type(str, Enum):
    QUEUEDJOB = "QueuedJob"

    def __str__(self) -> str:
        return str(self.value)
