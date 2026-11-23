from enum import Enum


class StaleProviderValueFreshness(str, Enum):
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
