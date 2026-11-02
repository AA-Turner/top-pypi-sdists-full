from enum import Enum


class ListSqsTriggersResponse200ItemMode(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
