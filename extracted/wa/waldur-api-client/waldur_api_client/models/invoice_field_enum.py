from enum import Enum


class InvoiceFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    COMPENSATIONS = "compensations"
    CUSTOMER = "customer"
    CUSTOMER_DETAILS = "customer_details"
    DUE_DATE = "due_date"
    INCURRED_COSTS = "incurred_costs"
    INVOICE_DATE = "invoice_date"
    ISSUER_DETAILS = "issuer_details"
    ITEMS = "items"
    MONTH = "month"
    NUMBER = "number"
    PAYMENT_URL = "payment_url"
    PRICE = "price"
    REFERENCE_NUMBER = "reference_number"
    STATE = "state"
    TAX = "tax"
    TOTAL = "total"
    URL = "url"
    UUID = "uuid"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
