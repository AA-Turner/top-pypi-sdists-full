from enum import StrEnum

class ManagedAgentsOutcomeTerminalResult(StrEnum):
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    MAX_ITERATIONS_REACHED = "max_iterations_reached"
    SATISFIED = "satisfied"

    def __str__(self) -> str:
        return str(self.value)
