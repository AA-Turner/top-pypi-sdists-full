from typing import Literal, cast

ListFlagsSort = Literal[
    "-created_at", "-key", "-name", "-type", "-updated_at", "created_at", "key", "name", "type", "updated_at"
]

LIST_FLAGS_SORT_VALUES: set[ListFlagsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-type",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "type",
    "updated_at",
}


def check_list_flags_sort(value: str) -> ListFlagsSort:
    if value in LIST_FLAGS_SORT_VALUES:
        return cast(ListFlagsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_FLAGS_SORT_VALUES!r}")
