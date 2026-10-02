from enum import StrEnum

class QaJobResponseDtoStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
