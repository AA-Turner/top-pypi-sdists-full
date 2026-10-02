from enum import StrEnum

class ManagedAgentsHttpapiAutomationScheduleTriggerType(StrEnum):
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
