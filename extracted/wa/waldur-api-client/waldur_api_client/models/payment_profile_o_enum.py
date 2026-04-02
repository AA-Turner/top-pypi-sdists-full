from enum import Enum


class PaymentProfileOEnum(str, Enum):
    IS_ACTIVE = "is_active"
    NAME = "name"
    PAYMENT_TYPE = "payment_type"
    VALUE_0 = "-is_active"
    VALUE_1 = "-name"
    VALUE_2 = "-payment_type"

    def __str__(self) -> str:
        return str(self.value)
