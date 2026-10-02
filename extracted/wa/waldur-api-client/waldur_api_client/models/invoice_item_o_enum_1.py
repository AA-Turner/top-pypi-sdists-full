from enum import Enum


class InvoiceItemOEnum1(str, Enum):
    INVOICE_CUSTOMER_NAME = "invoice_customer_name"
    PROJECT_NAME = "project_name"
    RESOURCE_OFFERING_NAME = "resource_offering_name"
    UNIT_PRICE = "unit_price"
    VALUE_0 = "-invoice_customer_name"
    VALUE_1 = "-project_name"
    VALUE_2 = "-resource_offering_name"
    VALUE_3 = "-unit_price"

    def __str__(self) -> str:
        return str(self.value)
