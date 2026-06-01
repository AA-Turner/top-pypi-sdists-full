from typing import Literal, cast

ListContextsSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_CONTEXTS_SORT_VALUES: set[ListContextsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_contexts_sort(value: str) -> ListContextsSort:
    if value in LIST_CONTEXTS_SORT_VALUES:
        return cast(ListContextsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_CONTEXTS_SORT_VALUES!r}")
