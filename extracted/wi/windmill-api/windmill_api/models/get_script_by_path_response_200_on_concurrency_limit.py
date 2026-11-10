from enum import Enum


class GetScriptByPathResponse200OnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
