from enum import Enum


class SetWsSpecificJsonBodyItemKind(str, Enum):
    RESOURCE = "resource"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
