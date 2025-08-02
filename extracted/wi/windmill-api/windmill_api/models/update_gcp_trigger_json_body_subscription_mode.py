from enum import Enum


class UpdateGcpTriggerJsonBodySubscriptionMode(str, Enum):
    CREATE_UPDATE = "create_update"
    EXISTING = "existing"

    def __str__(self) -> str:
        return str(self.value)
