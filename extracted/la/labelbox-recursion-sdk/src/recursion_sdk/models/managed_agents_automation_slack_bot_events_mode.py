from enum import StrEnum

class ManagedAgentsAutomationSlackBotEventsMode(StrEnum):
    ALLOW_EXTERNAL = "allow_external"
    IGNORE = "ignore"

    def __str__(self) -> str:
        return str(self.value)
