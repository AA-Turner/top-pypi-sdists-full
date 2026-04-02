from enum import Enum


class InvoiceStateEnum(str, Enum):
    CANCELED = "canceled"
    CREATED = "created"
    PAID = "paid"
    PENDING = "pending"
    PENDING_FINALIZATION = "pending_finalization"

    def __str__(self) -> str:
        return str(self.value)
