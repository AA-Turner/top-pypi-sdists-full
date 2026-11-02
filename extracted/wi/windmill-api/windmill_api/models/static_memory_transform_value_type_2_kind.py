from enum import Enum


class StaticMemoryTransformValueType2Kind(str, Enum):
    COMPACTION = "compaction"

    def __str__(self) -> str:
        return str(self.value)
