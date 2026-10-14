from enum import Enum


class StageEnum(str, Enum):
    EXECUTE = "execute"
    UNDO = "undo"

    def __str__(self) -> str:
        return str(self.value)
