from enum import Enum


class StaticMemoryTransformValueType2Kind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
