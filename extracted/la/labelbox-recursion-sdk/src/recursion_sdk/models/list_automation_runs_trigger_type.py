from enum import StrEnum

class ListAutomationRunsTriggerType(StrEnum):
    GITHUB = "github"
    MANUAL = "manual"
    SCHEDULE = "schedule"
    SLACK = "slack"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
