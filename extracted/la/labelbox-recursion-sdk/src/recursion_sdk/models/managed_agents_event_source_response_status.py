from enum import StrEnum

class ManagedAgentsEventSourceResponseStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
