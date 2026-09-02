from enum import Enum


class Language(str, Enum):
    TYPESCRIPT = "Typescript"

    def __str__(self) -> str:
        return str(self.value)
