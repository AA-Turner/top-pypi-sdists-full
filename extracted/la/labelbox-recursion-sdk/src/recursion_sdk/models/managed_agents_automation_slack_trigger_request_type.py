from enum import StrEnum

class ManagedAgentsAutomationSlackTriggerRequestType(StrEnum):
    SLACK = "slack"

    def __str__(self) -> str:
        return str(self.value)
