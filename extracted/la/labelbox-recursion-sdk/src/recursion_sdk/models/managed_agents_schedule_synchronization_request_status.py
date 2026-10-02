from enum import StrEnum

class ManagedAgentsScheduleSynchronizationRequestStatus(StrEnum):
    ERROR = "error"
    PENDING = "pending"
    SYNCED = "synced"

    def __str__(self) -> str:
        return str(self.value)
