from enum import Enum


class LoadJobMetricState(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
