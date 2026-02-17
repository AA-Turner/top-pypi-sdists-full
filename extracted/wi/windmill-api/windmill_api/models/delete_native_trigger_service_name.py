from enum import Enum


class DeleteNativeTriggerServiceName(str, Enum):
    GOOGLE = "google"
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
