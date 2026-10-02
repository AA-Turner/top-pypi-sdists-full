from enum import StrEnum

class TargetApiErrorInternalErrorCode(StrEnum):
    INTERNAL_ERROR = "internal_error"

    def __str__(self) -> str:
        return str(self.value)
