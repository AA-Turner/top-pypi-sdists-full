from enum import Enum


class CreateWebsocketTriggerJsonBodyMode(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
