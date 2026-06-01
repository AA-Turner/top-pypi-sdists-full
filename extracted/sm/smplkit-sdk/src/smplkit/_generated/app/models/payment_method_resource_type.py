from typing import Literal, cast

PaymentMethodResourceType = Literal["payment_method"]

PAYMENT_METHOD_RESOURCE_TYPE_VALUES: set[PaymentMethodResourceType] = {
    "payment_method",
}


def check_payment_method_resource_type(value: str) -> PaymentMethodResourceType:
    if value in PAYMENT_METHOD_RESOURCE_TYPE_VALUES:
        return cast(PaymentMethodResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PAYMENT_METHOD_RESOURCE_TYPE_VALUES!r}")
