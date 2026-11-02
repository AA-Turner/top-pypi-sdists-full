from enum import StrEnum

class CIStatus(StrEnum):
    FAILURE = "failure"
    NONE = "none"
    PENDING = "pending"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
