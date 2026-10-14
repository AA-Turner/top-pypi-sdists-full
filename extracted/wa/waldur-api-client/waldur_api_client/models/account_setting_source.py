from enum import Enum


class AccountSettingSource(str, Enum):
    DEFAULT = "default"
    OFFERING = "offering"
    PROVIDER = "provider"

    def __str__(self) -> str:
        return str(self.value)
