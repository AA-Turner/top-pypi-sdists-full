from enum import StrEnum

class TargetApiErrorInvariantViolationCode(StrEnum):
    INVARIANT_VIOLATION = "invariant_violation"

    def __str__(self) -> str:
        return str(self.value)
