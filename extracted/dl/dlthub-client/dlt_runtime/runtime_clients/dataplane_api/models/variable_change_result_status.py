from enum import Enum


class VariableChangeResultStatus(str, Enum):
    NOT_FOUND = "not_found"
    REMOVED = "removed"
    UPSERTED = "upserted"

    def __str__(self) -> str:
        return str(self.value)
