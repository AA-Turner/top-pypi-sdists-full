from enum import Enum


class ExtendedJobsJobsItemType0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
