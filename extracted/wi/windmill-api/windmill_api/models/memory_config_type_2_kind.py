from enum import Enum


class MemoryConfigType2Kind(str, Enum):
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
