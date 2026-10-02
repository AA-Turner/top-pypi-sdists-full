from enum import StrEnum

class ManagedAgentsApiErrorSlackReapprovalRequiredCode(StrEnum):
    SLACK_REAPPROVAL_REQUIRED = "slack_reapproval_required"

    def __str__(self) -> str:
        return str(self.value)
