from enum import Enum


class EditAmqpTriggerMode(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
