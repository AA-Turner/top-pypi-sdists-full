from enum import Enum


class GetJobResponse200Type0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
