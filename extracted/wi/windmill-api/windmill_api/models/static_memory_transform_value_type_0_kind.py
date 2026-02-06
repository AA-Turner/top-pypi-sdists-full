from enum import Enum


class StaticMemoryTransformValueType0Kind(str, Enum):
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
