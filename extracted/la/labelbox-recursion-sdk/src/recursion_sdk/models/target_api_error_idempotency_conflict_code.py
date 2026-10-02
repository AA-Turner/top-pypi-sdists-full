from enum import StrEnum

class TargetApiErrorIdempotencyConflictCode(StrEnum):
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"

    def __str__(self) -> str:
        return str(self.value)
