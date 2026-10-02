from enum import StrEnum

class TargetApiErrorIdempotencyInProgressCode(StrEnum):
    IDEMPOTENCY_IN_PROGRESS = "idempotency_in_progress"

    def __str__(self) -> str:
        return str(self.value)
