from enum import StrEnum

class OracleQaResultResponseDtoStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
