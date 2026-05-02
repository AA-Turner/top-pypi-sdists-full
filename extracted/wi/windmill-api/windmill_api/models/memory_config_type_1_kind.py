from enum import Enum


class MemoryConfigType1Kind(str, Enum):
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)
