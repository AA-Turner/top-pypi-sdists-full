from enum import StrEnum

class ManagedAgentsApiErrorSlackChannelsUnconfiguredCode(StrEnum):
    SLACK_CHANNELS_UNCONFIGURED = "slack_channels_unconfigured"

    def __str__(self) -> str:
        return str(self.value)
