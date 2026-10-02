from enum import StrEnum

class TargetApiErrorUnauthorizedCode(StrEnum):
    UNAUTHORIZED = "unauthorized"

    def __str__(self) -> str:
        return str(self.value)
