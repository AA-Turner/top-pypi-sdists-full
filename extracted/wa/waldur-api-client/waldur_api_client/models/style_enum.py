from enum import Enum


class StyleEnum(str, Enum):
    DASHED = "dashed"
    DOTTED = "dotted"
    SOLID = "solid"

    def __str__(self) -> str:
        return str(self.value)
