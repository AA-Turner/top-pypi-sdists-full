from enum import Enum


class ComparatorEnum(str, Enum):
    GE = "ge"
    LE = "le"

    def __str__(self) -> str:
        return str(self.value)
