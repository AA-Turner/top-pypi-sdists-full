from enum import Enum


class MemoryConfigType2Kind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
