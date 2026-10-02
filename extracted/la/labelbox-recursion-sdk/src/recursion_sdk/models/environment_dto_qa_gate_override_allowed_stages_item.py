from enum import StrEnum

class EnvironmentDtoQaGateOverrideAllowedStagesItem(StrEnum):
    LOCKING = "locking"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
