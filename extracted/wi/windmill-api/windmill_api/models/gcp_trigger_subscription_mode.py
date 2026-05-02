from enum import Enum


class GcpTriggerSubscriptionMode(str, Enum):
    CREATE_UPDATE = "create_update"
    EXISTING = "existing"

    def __str__(self) -> str:
        return str(self.value)
