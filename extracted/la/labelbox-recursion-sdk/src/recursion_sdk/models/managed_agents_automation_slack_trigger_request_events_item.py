from enum import StrEnum

class ManagedAgentsAutomationSlackTriggerRequestEventsItem(StrEnum):
    APP_MENTION = "app_mention"
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
