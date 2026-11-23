from enum import Enum


class FreshBillingUsageFreshness(str, Enum):
    FRESH = "fresh"

    def __str__(self) -> str:
        return str(self.value)
