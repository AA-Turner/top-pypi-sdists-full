from enum import Enum


class MemoryOffKind(str, Enum):
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
