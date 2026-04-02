from enum import Enum


class DiscountTypeEnum(str, Enum):
    DISCOUNT = "discount"
    SPECIAL_PRICE = "special_price"

    def __str__(self) -> str:
        return str(self.value)
