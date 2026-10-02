from enum import StrEnum

class TargetApiErrorRateLimitExceededCode(StrEnum):
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
