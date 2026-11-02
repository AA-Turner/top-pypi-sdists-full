from enum import Enum


class SuspendOnlyIdlePolicyMode(str, Enum):
    SUSPEND_ONLY = "suspend_only"

    def __str__(self) -> str:
        return str(self.value)
