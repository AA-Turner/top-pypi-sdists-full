from enum import Enum


class RuntimeImageBuildAttemptOutcome(str, Enum):
    FAILED = "failed"
    LEASE_EXPIRED = "lease_expired"
    RETRY_WAIT = "retry_wait"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
