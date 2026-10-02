from enum import StrEnum

class ManagedAgentsAutomationStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
