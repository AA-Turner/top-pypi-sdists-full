from enum import Enum


class NativeTriggerServiceCallbackServiceName(str, Enum):
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
