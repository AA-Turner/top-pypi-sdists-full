from typing import Literal, TypedDict

RetryProfiles = Literal["no_retry", "conservative", "aggressive", "resilient"] | None


class RetryProfile(TypedDict, total=False):
    retry_enabled: bool
    retry_attempts: int | None
    retry_backoff: float | None


RETRY_PROFILES: dict[RetryProfiles, RetryProfile] = {
    "no_retry": {"retry_enabled": False},
    "conservative": {"retry_enabled": True, "retry_attempts": 2, "retry_backoff": 0.5},
    "aggressive": {"retry_enabled": True, "retry_attempts": 5, "retry_backoff": 0.3},
    "resilient": {"retry_enabled": True, "retry_attempts": 7, "retry_backoff": 0.6},
}
