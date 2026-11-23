from enum import Enum


class StaleBillingTransactionsFreshness(str, Enum):
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
