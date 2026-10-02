from enum import StrEnum

class ManagedAgentsEvaluationRunFinishedRequestTerminalStatus(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
