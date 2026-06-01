from typing import Literal, cast

AddPaymentMethodDataType = Literal["payment_method"]

ADD_PAYMENT_METHOD_DATA_TYPE_VALUES: set[AddPaymentMethodDataType] = {
    "payment_method",
}


def check_add_payment_method_data_type(value: str) -> AddPaymentMethodDataType:
    if value in ADD_PAYMENT_METHOD_DATA_TYPE_VALUES:
        return cast(AddPaymentMethodDataType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ADD_PAYMENT_METHOD_DATA_TYPE_VALUES!r}")
