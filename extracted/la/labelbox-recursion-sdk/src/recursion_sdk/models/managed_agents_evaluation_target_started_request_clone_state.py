from enum import StrEnum

class ManagedAgentsEvaluationTargetStartedRequestCloneState(StrEnum):
    READY = "ready"
    SANDBOXLESS = "sandboxless"

    def __str__(self) -> str:
        return str(self.value)
