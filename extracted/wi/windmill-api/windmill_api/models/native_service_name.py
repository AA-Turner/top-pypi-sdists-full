from enum import Enum


class NativeServiceName(str, Enum):
    NEXTCLOUD = "nextcloud"

    def __str__(self) -> str:
        return str(self.value)
