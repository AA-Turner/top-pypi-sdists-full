from enum import StrEnum

class RunConfigFileClashInvalidRequestErrorDtoCode(StrEnum):
    INVALID_REQUEST = "invalid_request"

    def __str__(self) -> str:
        return str(self.value)
