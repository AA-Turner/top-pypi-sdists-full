from enum import StrEnum

class ManagedAgentsLabelboxAudienceRequestKind(StrEnum):
    INTERNAL_SLACK_BINDING = "internal_slack_binding"
    SLACK_CONNECT_BINDING = "slack_connect_binding"

    def __str__(self) -> str:
        return str(self.value)
