from enum import Enum


class OfferingMergeAreaEnum(str, Enum):
    ACCOUNTS_AND_ACCESS = "accounts_and_access"
    BILLING_HISTORY = "billing_history"
    INVOICES = "invoices"
    OFFERING_CONFIGURATION = "offering_configuration"
    RESOURCES_AND_ORDERS = "resources_and_orders"

    def __str__(self) -> str:
        return str(self.value)
