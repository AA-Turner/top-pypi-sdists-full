from enum import StrEnum

class ManagedAgentsApiErrorInternalErrorCode(StrEnum):
    INTERNAL_ERROR = "internal_error"

    def __str__(self) -> str:
        return str(self.value)
