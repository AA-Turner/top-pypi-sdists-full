from enum import Enum


class AiDecisionType(str, Enum):
    AIDECISION = "aidecision"

    def __str__(self) -> str:
        return str(self.value)
