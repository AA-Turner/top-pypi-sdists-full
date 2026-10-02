from enum import StrEnum

class ManagedAgentsAutomationDefinitionScheduleStatusSynchronization(StrEnum):
    ERROR = "error"
    PENDING = "pending"
    SYNCED = "synced"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
