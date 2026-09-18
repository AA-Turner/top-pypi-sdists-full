from enum import Enum


class MemoryConfigType3Kind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
