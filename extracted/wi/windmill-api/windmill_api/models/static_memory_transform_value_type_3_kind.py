from enum import Enum


class StaticMemoryTransformValueType3Kind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
