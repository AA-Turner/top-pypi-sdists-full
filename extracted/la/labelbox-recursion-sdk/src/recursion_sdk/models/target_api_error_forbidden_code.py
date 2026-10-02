from enum import StrEnum

class TargetApiErrorForbiddenCode(StrEnum):
    FORBIDDEN = "forbidden"

    def __str__(self) -> str:
        return str(self.value)
