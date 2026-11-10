from enum import Enum


class GetSuspendedJobFlowResponse200JobType1RawFlowOnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
