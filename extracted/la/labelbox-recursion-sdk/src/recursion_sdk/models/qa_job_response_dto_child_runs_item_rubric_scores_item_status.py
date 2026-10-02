from enum import StrEnum

class QaJobResponseDtoChildRunsItemRubricScoresItemStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
