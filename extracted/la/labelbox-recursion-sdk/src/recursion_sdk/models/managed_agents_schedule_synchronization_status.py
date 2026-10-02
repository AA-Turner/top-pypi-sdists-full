from enum import StrEnum

class ManagedAgentsScheduleSynchronizationStatus(StrEnum):
    ERROR = "error"
    PENDING = "pending"
    SYNCED = "synced"

    def __str__(self) -> str:
        return str(self.value)
