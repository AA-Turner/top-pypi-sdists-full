from enum import Enum


class FreshBillingTransactionsFreshness(str, Enum):
    FRESH = "fresh"

    def __str__(self) -> str:
        return str(self.value)
