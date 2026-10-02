from enum import StrEnum

class TuningRunResponseDtoStatus(StrEnum):
    AGGREGATING = "aggregating"
    CANCELLED = "cancelled"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    EXECUTING = "executing"
    FAILED = "failed"
    PENDING = "pending"
    WAITING_CHILDREN = "waiting_children"
    WAITING_EXTERNAL = "waiting_external"

    def __str__(self) -> str:
        return str(self.value)
