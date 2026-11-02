from enum import Enum


class MemoryConfigType2Kind(str, Enum):
    COMPACTION = "compaction"

    def __str__(self) -> str:
        return str(self.value)
