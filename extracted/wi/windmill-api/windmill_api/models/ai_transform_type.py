from enum import Enum


class AiTransformType(str, Enum):
    AI = "ai"

    def __str__(self) -> str:
        return str(self.value)
