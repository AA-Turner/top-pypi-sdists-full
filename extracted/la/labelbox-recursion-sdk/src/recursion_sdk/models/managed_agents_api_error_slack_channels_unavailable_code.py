from enum import StrEnum

class ManagedAgentsApiErrorSlackChannelsUnavailableCode(StrEnum):
    SLACK_CHANNELS_UNAVAILABLE = "slack_channels_unavailable"

    def __str__(self) -> str:
        return str(self.value)
