from enum import StrEnum

class TargetApiErrorNotFoundCode(StrEnum):
    NOT_FOUND = "not_found"

    def __str__(self) -> str:
        return str(self.value)
