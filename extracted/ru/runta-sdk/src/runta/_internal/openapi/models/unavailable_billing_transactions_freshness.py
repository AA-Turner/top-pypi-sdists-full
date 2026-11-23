from enum import Enum


class UnavailableBillingTransactionsFreshness(str, Enum):
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
