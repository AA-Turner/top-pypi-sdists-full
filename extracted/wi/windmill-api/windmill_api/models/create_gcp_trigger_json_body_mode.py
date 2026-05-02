from enum import Enum


class CreateGcpTriggerJsonBodyMode(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
