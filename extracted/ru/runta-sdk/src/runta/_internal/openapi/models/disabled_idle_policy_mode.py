from enum import Enum


class DisabledIdlePolicyMode(str, Enum):
    DISABLED = "disabled"

    def __str__(self) -> str:
        return str(self.value)
