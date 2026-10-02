from enum import StrEnum

class ManagedAgentsApiErrorSlackChannelsRejectedCode(StrEnum):
    SLACK_CHANNELS_REJECTED = "slack_channels_rejected"

    def __str__(self) -> str:
        return str(self.value)
