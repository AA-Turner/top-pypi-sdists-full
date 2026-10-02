from enum import Enum


class DiscountAggregationEnum(str, Enum):
    CUSTOMER = "customer"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return str(self.value)
