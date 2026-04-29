from enum import Enum


class TriggeredJobStatus(str, Enum):
    SKIPPED_ALREADY_COVERED = "skipped_already_covered"
    SKIPPED_CONCURRENCY_LIMIT = "skipped_concurrency_limit"
    SKIPPED_FRESH = "skipped_fresh"
    SKIPPED_MINUTES_LIMIT = "skipped_minutes_limit"
    SKIPPED_ORG_CONCURRENCY_LIMIT = "skipped_org_concurrency_limit"
    SKIPPED_OUT_OF_INTERVAL = "skipped_out_of_interval"
    SKIPPED_TRIAL_EXPIRED = "skipped_trial_expired"
    SKIPPED_UPSTREAM_PENDING = "skipped_upstream_pending"
    TRIGGERED = "triggered"

    def __str__(self) -> str:
        return str(self.value)
