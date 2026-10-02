from enum import StrEnum

class ManagedAgentsApiErrorIdempotencyUnavailableCode(StrEnum):
    IDEMPOTENCY_UNAVAILABLE = "idempotency_unavailable"

    def __str__(self) -> str:
        return str(self.value)
