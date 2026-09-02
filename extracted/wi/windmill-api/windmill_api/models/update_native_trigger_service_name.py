from enum import Enum


class UpdateNativeTriggerServiceName(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
