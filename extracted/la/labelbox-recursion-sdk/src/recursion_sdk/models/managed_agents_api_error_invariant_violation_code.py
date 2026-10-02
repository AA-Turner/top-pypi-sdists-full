from enum import StrEnum

class ManagedAgentsApiErrorInvariantViolationCode(StrEnum):
    INVARIANT_VIOLATION = "invariant_violation"

    def __str__(self) -> str:
        return str(self.value)
