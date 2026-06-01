from typing import Literal, cast

AccountResourceType = Literal["account"]

ACCOUNT_RESOURCE_TYPE_VALUES: set[AccountResourceType] = {
    "account",
}


def check_account_resource_type(value: str) -> AccountResourceType:
    if value in ACCOUNT_RESOURCE_TYPE_VALUES:
        return cast(AccountResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ACCOUNT_RESOURCE_TYPE_VALUES!r}")
