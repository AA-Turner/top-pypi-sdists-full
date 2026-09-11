from enum import Enum


class TableLoadStatus(str, Enum):
    FAILED = "failed"
    LOADED = "loaded"

    def __str__(self) -> str:
        return str(self.value)
