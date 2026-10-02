from enum import StrEnum

class ManagedAgentsApiErrorRateLimitedCode(StrEnum):
    RATE_LIMITED = "rate_limited"

    def __str__(self) -> str:
        return str(self.value)
