from enum import StrEnum

class ManagedAgentsApiErrorSlackRateLimitedCode(StrEnum):
    SLACK_RATE_LIMITED = "slack_rate_limited"

    def __str__(self) -> str:
        return str(self.value)
