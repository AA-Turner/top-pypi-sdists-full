from enum import StrEnum

class EvaluationExportResponseListDtoItemStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
