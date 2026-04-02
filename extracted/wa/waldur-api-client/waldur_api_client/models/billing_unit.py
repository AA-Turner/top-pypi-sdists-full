from enum import Enum


class BillingUnit(str, Enum):
    DAY = "day"
    HALF_MONTH = "half_month"
    HOUR = "hour"
    MONTH = "month"
    QUANTITY = "quantity"
    QUARTER = "quarter"

    def __str__(self) -> str:
        return str(self.value)
