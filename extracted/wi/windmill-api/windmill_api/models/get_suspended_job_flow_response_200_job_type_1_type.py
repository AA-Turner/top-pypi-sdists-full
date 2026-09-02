from enum import Enum


class GetSuspendedJobFlowResponse200JobType1Type(str, Enum):
    QUEUEDJOB = "QueuedJob"

    def __str__(self) -> str:
        return str(self.value)
