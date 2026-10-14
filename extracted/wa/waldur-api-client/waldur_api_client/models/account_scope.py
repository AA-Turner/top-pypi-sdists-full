from enum import Enum


class AccountScope(str, Enum):
    OFFERING = "offering"
    PROVIDER = "provider"

    def __str__(self) -> str:
        return str(self.value)
