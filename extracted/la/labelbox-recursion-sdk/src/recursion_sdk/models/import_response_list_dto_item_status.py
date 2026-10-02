from enum import StrEnum

class ImportResponseListDtoItemStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"
    PENDING = "pending"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
