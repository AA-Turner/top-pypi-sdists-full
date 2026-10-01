from enum import Enum


class DestinationKind(str, Enum):
    SLACK_WEBHOOK = "slack_webhook"

    def __str__(self) -> str:
        return str(self.value)
