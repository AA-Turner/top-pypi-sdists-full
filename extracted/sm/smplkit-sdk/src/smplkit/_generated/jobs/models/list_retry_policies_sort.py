from typing import Literal, cast

ListRetryPoliciesSort = Literal["-created_at", "-name", "-updated_at", "created_at", "name", "updated_at"]

LIST_RETRY_POLICIES_SORT_VALUES: set[ListRetryPoliciesSort] = {
    "-created_at",
    "-name",
    "-updated_at",
    "created_at",
    "name",
    "updated_at",
}


def check_list_retry_policies_sort(value: str) -> ListRetryPoliciesSort:
    if value in LIST_RETRY_POLICIES_SORT_VALUES:
        return cast(ListRetryPoliciesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_RETRY_POLICIES_SORT_VALUES!r}")
