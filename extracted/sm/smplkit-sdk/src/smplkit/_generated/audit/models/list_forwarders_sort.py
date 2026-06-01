from typing import Literal, cast

ListForwardersSort = Literal["-created_at", "-updated_at", "created_at", "updated_at"]

LIST_FORWARDERS_SORT_VALUES: set[ListForwardersSort] = {
    "-created_at",
    "-updated_at",
    "created_at",
    "updated_at",
}


def check_list_forwarders_sort(value: str) -> ListForwardersSort:
    if value in LIST_FORWARDERS_SORT_VALUES:
        return cast(ListForwardersSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_FORWARDERS_SORT_VALUES!r}")
