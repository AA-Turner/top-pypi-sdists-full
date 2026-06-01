from typing import Literal, cast

ListGroupsSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_GROUPS_SORT_VALUES: set[ListGroupsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_groups_sort(value: str) -> ListGroupsSort:
    if value in LIST_GROUPS_SORT_VALUES:
        return cast(ListGroupsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_GROUPS_SORT_VALUES!r}")
