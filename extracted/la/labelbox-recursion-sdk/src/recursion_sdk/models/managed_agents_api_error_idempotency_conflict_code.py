from enum import StrEnum

class ManagedAgentsApiErrorIdempotencyConflictCode(StrEnum):
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"

    def __str__(self) -> str:
        return str(self.value)
