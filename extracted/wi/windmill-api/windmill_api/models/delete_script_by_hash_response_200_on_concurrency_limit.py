from enum import Enum


class DeleteScriptByHashResponse200OnConcurrencyLimit(str, Enum):
    FAIL = "fail"
    QUEUE = "queue"

    def __str__(self) -> str:
        return str(self.value)
