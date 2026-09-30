from enum import Enum


class StaticMemoryTransformValueType4Kind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
