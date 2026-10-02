from enum import StrEnum

class ManagedAgentsAutomationSlackTriggerType(StrEnum):
    SLACK = "slack"

    def __str__(self) -> str:
        return str(self.value)
