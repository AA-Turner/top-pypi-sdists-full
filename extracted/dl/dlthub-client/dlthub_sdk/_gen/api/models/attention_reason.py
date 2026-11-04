from enum import Enum


class AttentionReason(str, Enum):
    EMPTY_RUN = "empty_run"
    FAILED = "failed"
    LONG_RUNNING = "long_running"

    def __str__(self) -> str:
        return str(self.value)
