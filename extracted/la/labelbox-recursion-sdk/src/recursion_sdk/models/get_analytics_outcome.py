from enum import StrEnum

class GetAnalyticsOutcome(StrEnum):
    COMPLETED = "completed"
    FAIL = "fail"
    FAILED = "failed"
    IN_FLIGHT = "in_flight"
    NOT_APPLICABLE = "not_applicable"
    PASS = "pass"
    PENDING = "pending"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
