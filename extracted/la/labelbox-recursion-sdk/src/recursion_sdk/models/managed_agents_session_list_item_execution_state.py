from enum import StrEnum

class ManagedAgentsSessionListItemExecutionState(StrEnum):
    COMPLETED = "completed"
    IDLE = "idle"
    PROVISIONING = "provisioning"
    QUEUED = "queued"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
