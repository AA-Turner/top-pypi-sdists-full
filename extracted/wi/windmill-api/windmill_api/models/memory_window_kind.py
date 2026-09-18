from enum import Enum


class MemoryWindowKind(str, Enum):
    WINDOW = "window"

    def __str__(self) -> str:
        return str(self.value)
