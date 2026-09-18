from enum import Enum


class StaticMemoryTransformValueType1Kind(str, Enum):
    WINDOW = "window"

    def __str__(self) -> str:
        return str(self.value)
