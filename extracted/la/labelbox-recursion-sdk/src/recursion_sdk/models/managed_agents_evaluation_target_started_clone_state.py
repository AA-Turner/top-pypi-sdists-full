from enum import StrEnum

class ManagedAgentsEvaluationTargetStartedCloneState(StrEnum):
    READY = "ready"
    SANDBOXLESS = "sandboxless"

    def __str__(self) -> str:
        return str(self.value)
