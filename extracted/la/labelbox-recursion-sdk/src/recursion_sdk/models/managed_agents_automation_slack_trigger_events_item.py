from enum import StrEnum

class ManagedAgentsAutomationSlackTriggerEventsItem(StrEnum):
    APP_MENTION = "app_mention"
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
