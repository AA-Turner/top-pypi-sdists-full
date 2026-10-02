from enum import StrEnum

class ManagedAgentsOutcomeStatus(StrEnum):
    EVALUATING = "evaluating"
    PENDING = "pending"
    RUNNING = "running"
    TERMINAL = "terminal"

    def __str__(self) -> str:
        return str(self.value)
