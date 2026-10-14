from enum import Enum


class InvoicePolicyEnum(str, Enum):
    ALL_MONTHS = "all_months"
    OPEN_MONTH = "open_month"

    def __str__(self) -> str:
        return str(self.value)
