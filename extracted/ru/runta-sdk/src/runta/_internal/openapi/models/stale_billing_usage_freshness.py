from enum import Enum


class StaleBillingUsageFreshness(str, Enum):
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
