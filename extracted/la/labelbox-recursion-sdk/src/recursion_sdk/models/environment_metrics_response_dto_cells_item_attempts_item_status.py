from enum import StrEnum

class EnvironmentMetricsResponseDtoCellsItemAttemptsItemStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    GRADING = "grading"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
