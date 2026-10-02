from enum import Enum


class SlurmPolicyDateProjectionStatusEnum(str, Enum):
    EXCEEDED = "exceeded"
    NEVER = "never"
    PROJECTED = "projected"

    def __str__(self) -> str:
        return str(self.value)
