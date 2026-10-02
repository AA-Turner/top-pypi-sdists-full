from enum import StrEnum

class ManagedAgentsSessionExecutionState(StrEnum):
    COMPLETED = "completed"
    IDLE = "idle"
    PROVISIONING = "provisioning"
    QUEUED = "queued"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
