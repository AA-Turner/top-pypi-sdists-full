from enum import Enum


class PaymentTypeEnum(str, Enum):
    FIXED_PRICE = "fixed_price"
    INVOICES = "invoices"
    PAYMENT_GW_MONTHLY = "payment_gw_monthly"

    def __str__(self) -> str:
        return str(self.value)
