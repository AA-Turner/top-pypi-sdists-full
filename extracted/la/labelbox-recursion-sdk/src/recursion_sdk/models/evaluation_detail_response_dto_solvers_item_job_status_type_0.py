from enum import StrEnum

class EvaluationDetailResponseDtoSolversItemJobStatusType0(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
