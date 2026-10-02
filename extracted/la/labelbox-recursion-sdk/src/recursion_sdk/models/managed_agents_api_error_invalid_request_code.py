from enum import StrEnum

class ManagedAgentsApiErrorInvalidRequestCode(StrEnum):
    INVALID_REQUEST = "invalid_request"

    def __str__(self) -> str:
        return str(self.value)
