from enum import StrEnum

class ManagedAgentsPushDeviceTokenKind(StrEnum):
    APP = "app"
    LIVE_ACTIVITY = "live_activity"
    PUSH_TO_START = "push_to_start"
    WIDGET = "widget"

    def __str__(self) -> str:
        return str(self.value)
