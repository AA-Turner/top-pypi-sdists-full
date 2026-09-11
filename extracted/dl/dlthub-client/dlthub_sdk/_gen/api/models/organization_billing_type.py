from enum import Enum


class OrganizationBillingType(str, Enum):
    INVOICE = "invoice"
    STRIPE_LINK = "stripe_link"

    def __str__(self) -> str:
        return str(self.value)
