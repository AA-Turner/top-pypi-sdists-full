from enum import Enum


class BillingModeEnum(str, Enum):
    MONTHLY = "monthly"
    PREPAID = "prepaid"
    USAGE = "usage"

    def __str__(self) -> str:
        return str(self.value)
