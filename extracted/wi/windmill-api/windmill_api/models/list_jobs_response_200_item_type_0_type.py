from enum import Enum


class ListJobsResponse200ItemType0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
