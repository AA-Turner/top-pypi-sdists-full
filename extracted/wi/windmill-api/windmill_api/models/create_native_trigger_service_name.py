from enum import Enum


class CreateNativeTriggerServiceName(str, Enum):
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
