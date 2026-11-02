from enum import Enum


class InputTransformType2Type(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
