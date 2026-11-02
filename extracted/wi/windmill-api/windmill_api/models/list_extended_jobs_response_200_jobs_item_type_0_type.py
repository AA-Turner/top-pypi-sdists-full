from enum import Enum


class ListExtendedJobsResponse200JobsItemType0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
