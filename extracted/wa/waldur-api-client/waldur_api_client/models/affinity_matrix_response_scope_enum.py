from enum import Enum


class AffinityMatrixResponseScopeEnum(str, Enum):
    ALL = "all"
    POOL = "pool"
    SUGGESTIONS = "suggestions"

    def __str__(self) -> str:
        return str(self.value)
