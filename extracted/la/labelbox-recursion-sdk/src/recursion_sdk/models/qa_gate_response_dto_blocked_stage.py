from enum import StrEnum

class QaGateResponseDtoBlockedStage(StrEnum):
    LOCKING = "locking"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
