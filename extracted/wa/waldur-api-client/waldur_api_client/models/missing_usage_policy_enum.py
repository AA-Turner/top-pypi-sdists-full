from enum import Enum


class MissingUsagePolicyEnum(str, Enum):
    NONE = "none"
    REUSE = "reuse"
    ZERO = "zero"

    def __str__(self) -> str:
        return str(self.value)
