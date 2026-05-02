from enum import Enum


class ListNativeTriggersServiceName(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
