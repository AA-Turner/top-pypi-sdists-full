from enum import StrEnum

class ManagedAgentsOutcomeEvaluationResult(StrEnum):
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    MAX_ITERATIONS_REACHED = "max_iterations_reached"
    NEEDS_REVISION = "needs_revision"
    SATISFIED = "satisfied"

    def __str__(self) -> str:
        return str(self.value)
