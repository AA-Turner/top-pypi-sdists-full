from enum import StrEnum

class QaGateResponseArrayDtoItemBlockedStage(StrEnum):
    LOCKING = "locking"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
