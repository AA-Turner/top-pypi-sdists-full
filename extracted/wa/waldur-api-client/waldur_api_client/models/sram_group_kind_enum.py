from enum import Enum


class SramGroupKindEnum(str, Enum):
    CO = "co"
    GROUP = "group"

    def __str__(self) -> str:
        return str(self.value)
