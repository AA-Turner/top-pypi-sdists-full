from typing import Literal, cast

ListPaymentMethodsSort = Literal[
    "-created_at", "-exp_year", "-is_default", "-updated_at", "created_at", "exp_year", "is_default", "updated_at"
]

LIST_PAYMENT_METHODS_SORT_VALUES: set[ListPaymentMethodsSort] = {
    "-created_at",
    "-exp_year",
    "-is_default",
    "-updated_at",
    "created_at",
    "exp_year",
    "is_default",
    "updated_at",
}


def check_list_payment_methods_sort(value: str) -> ListPaymentMethodsSort:
    if value in LIST_PAYMENT_METHODS_SORT_VALUES:
        return cast(ListPaymentMethodsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_PAYMENT_METHODS_SORT_VALUES!r}")
