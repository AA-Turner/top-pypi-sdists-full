from enum import Enum


class StaticMemoryTransformType(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
