from enum import StrEnum

class ManagedAgentsSessionFailureCategory(StrEnum):
    CALLER_ERROR = "caller_error"
    INTERNAL = "internal"
    TRANSIENT = "transient"

    def __str__(self) -> str:
        return str(self.value)
