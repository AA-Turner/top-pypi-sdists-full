from enum import Enum


class GetHubFlowByIdResponse200FlowValueOnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
