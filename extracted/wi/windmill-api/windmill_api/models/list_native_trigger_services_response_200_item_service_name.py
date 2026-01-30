from enum import Enum


class ListNativeTriggerServicesResponse200ItemServiceName(str, Enum):
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
