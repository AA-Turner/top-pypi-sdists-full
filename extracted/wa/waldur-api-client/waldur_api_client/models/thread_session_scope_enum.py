from enum import Enum


class ThreadSessionScopeEnum(str, Enum):
    OWN = "own"

    def __str__(self) -> str:
        return str(self.value)
