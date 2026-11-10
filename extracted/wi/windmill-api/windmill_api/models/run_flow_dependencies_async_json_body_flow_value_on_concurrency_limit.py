from enum import Enum


class RunFlowDependenciesAsyncJsonBodyFlowValueOnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
