from enum import StrEnum

class TargetApiErrorInvalidRequestCode(StrEnum):
    INVALID_REQUEST = "invalid_request"

    def __str__(self) -> str:
        return str(self.value)
