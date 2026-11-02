from enum import Enum


class GetNativeTriggerResponse200ServiceName(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
