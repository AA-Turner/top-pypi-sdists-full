from enum import StrEnum

class ManagedAgentsSlackEventSourceRequestType(StrEnum):
    SLACK_EVENTS_API = "slack_events_api"

    def __str__(self) -> str:
        return str(self.value)
