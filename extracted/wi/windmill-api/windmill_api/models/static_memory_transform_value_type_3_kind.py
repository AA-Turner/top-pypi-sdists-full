from enum import Enum


class StaticMemoryTransformValueType3Kind(str, Enum):
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
