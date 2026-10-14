from enum import Enum


class GoodDirectionEnum(str, Enum):
    DOWN = "down"
    NEUTRAL = "neutral"
    UP = "up"

    def __str__(self) -> str:
        return str(self.value)
