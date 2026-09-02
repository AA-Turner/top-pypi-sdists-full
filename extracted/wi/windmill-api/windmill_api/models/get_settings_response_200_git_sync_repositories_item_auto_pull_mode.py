from enum import Enum


class GetSettingsResponse200GitSyncRepositoriesItemAutoPullMode(str, Enum):
    AUTO = "auto"
    POLLING = "polling"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
