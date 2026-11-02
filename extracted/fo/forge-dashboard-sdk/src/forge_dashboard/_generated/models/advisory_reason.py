from enum import StrEnum

class AdvisoryReason(StrEnum):
    FAILED = "failed"
    NOT_ENABLED = "not_enabled"
    REFUSED = "refused"
    SWITCHED_OFF = "switched_off"
    THROTTLED = "throttled"
    TOO_MANY = "too_many"

    def __str__(self) -> str:
        return str(self.value)
