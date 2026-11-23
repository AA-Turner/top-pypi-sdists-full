from enum import Enum


class UnavailableProviderValueFreshness(str, Enum):
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
