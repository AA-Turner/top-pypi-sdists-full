from enum import Enum


class ExecutionStateEnum(str, Enum):
    ERRED = "Erred"
    OK = "OK"
    PROCESSING = "Processing"
    SCHEDULED = "Scheduled"

    def __str__(self) -> str:
        return str(self.value)
