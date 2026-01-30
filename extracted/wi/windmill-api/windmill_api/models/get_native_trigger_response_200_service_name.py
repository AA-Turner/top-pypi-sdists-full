from enum import Enum


class GetNativeTriggerResponse200ServiceName(str, Enum):
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
