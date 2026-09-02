from enum import Enum


class MemoryAutoKind(str, Enum):
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
