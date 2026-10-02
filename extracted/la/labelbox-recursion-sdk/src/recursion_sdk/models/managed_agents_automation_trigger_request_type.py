from enum import StrEnum

class ManagedAgentsAutomationTriggerRequestType(StrEnum):
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
