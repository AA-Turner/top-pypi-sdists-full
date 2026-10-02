from enum import StrEnum

class ManagedAgentsAutomationRunTriggerType(StrEnum):
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
