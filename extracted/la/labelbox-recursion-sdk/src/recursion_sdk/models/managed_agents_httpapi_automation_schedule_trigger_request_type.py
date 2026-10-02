from enum import StrEnum

class ManagedAgentsHttpapiAutomationScheduleTriggerRequestType(StrEnum):
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
