from enum import Enum


class ListWsSpecificVersionsKind(str, Enum):
    RESOURCE = "resource"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
