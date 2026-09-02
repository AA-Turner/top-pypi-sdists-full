from enum import Enum


class JobType0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
