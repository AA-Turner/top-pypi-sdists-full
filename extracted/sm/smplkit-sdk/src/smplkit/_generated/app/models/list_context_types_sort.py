from typing import Literal, cast

ListContextTypesSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_CONTEXT_TYPES_SORT_VALUES: set[ListContextTypesSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_context_types_sort(value: str) -> ListContextTypesSort:
    if value in LIST_CONTEXT_TYPES_SORT_VALUES:
        return cast(ListContextTypesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_CONTEXT_TYPES_SORT_VALUES!r}")
