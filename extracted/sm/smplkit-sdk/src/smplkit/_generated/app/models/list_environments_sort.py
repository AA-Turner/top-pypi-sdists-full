from typing import Literal, cast

ListEnvironmentsSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_ENVIRONMENTS_SORT_VALUES: set[ListEnvironmentsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_environments_sort(value: str) -> ListEnvironmentsSort:
    if value in LIST_ENVIRONMENTS_SORT_VALUES:
        return cast(ListEnvironmentsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_ENVIRONMENTS_SORT_VALUES!r}")
