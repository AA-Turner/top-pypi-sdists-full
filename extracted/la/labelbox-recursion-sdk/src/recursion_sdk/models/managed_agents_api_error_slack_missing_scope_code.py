from enum import StrEnum

class ManagedAgentsApiErrorSlackMissingScopeCode(StrEnum):
    SLACK_MISSING_SCOPE = "slack_missing_scope"

    def __str__(self) -> str:
        return str(self.value)
