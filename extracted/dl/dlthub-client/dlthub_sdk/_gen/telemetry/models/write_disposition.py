from enum import Enum


class WriteDisposition(str, Enum):
    APPEND = "append"
    MERGE = "merge"
    REPLACE = "replace"

    def __str__(self) -> str:
        return str(self.value)
