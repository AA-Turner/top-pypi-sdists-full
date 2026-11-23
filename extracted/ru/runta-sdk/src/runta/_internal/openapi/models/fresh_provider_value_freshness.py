from enum import Enum


class FreshProviderValueFreshness(str, Enum):
    FRESH = "fresh"

    def __str__(self) -> str:
        return str(self.value)
