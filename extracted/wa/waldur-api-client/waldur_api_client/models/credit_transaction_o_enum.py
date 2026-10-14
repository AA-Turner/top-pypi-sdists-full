from enum import Enum


class CreditTransactionOEnum(str, Enum):
    BILLING_PERIOD = "billing_period"
    CREATED = "created"
    VALUE_0 = "-billing_period"
    VALUE_1 = "-created"

    def __str__(self) -> str:
        return str(self.value)
