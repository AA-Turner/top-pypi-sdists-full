from enum import StrEnum

class ManagedAgentsEventSourceSummaryType(StrEnum):
    CUSTOM_WEBHOOK = "custom_webhook"
    GITHUB_WEBHOOK = "github_webhook"
    SLACK_EVENTS_API = "slack_events_api"

    def __str__(self) -> str:
        return str(self.value)
