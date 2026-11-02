from enum import Enum


class GetSuspendedJobFlowResponse200JobType0Type(str, Enum):
    COMPLETEDJOB = "CompletedJob"

    def __str__(self) -> str:
        return str(self.value)
