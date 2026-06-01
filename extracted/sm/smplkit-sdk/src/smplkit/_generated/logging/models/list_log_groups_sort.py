from typing import Literal, cast

ListLogGroupsSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_LOG_GROUPS_SORT_VALUES: set[ListLogGroupsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_log_groups_sort(value: str) -> ListLogGroupsSort:
    if value in LIST_LOG_GROUPS_SORT_VALUES:
        return cast(ListLogGroupsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LOG_GROUPS_SORT_VALUES!r}")
