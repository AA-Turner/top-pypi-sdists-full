from enum import StrEnum

class QaJobPageResponseDtoItemsItemChildRunsItemRubricScoresItemStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
