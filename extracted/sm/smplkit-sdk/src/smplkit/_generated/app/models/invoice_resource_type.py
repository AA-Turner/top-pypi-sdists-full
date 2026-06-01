from typing import Literal, cast

InvoiceResourceType = Literal["invoice"]

INVOICE_RESOURCE_TYPE_VALUES: set[InvoiceResourceType] = {
    "invoice",
}


def check_invoice_resource_type(value: str) -> InvoiceResourceType:
    if value in INVOICE_RESOURCE_TYPE_VALUES:
        return cast(InvoiceResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INVOICE_RESOURCE_TYPE_VALUES!r}")
