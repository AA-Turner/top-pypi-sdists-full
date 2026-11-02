from enum import Enum


class MemoryManualKind(str, Enum):
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)
