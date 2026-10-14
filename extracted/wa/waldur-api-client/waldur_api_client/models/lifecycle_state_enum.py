from enum import Enum


class LifecycleStateEnum(str, Enum):
    CLOSED = "closed"
    DECIDING = "deciding"
    EVALUATING = "evaluating"
    RESULTS_PUBLISHED = "results_published"

    def __str__(self) -> str:
        return str(self.value)
