from typing import Literal, cast

RetryOnReasonsItem = Literal["CONNECTION_ERROR", "NON_SUCCESS_STATUS", "TIMEOUT"]

RETRY_ON_REASONS_ITEM_VALUES: set[RetryOnReasonsItem] = {
    "CONNECTION_ERROR",
    "NON_SUCCESS_STATUS",
    "TIMEOUT",
}


def check_retry_on_reasons_item(value: str) -> RetryOnReasonsItem:
    if value in RETRY_ON_REASONS_ITEM_VALUES:
        return cast(RetryOnReasonsItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RETRY_ON_REASONS_ITEM_VALUES!r}")
