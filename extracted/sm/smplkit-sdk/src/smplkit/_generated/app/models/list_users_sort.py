from typing import Literal, cast

ListUsersSort = Literal["-created_at", "-display_name", "-email", "created_at", "display_name", "email"]

LIST_USERS_SORT_VALUES: set[ListUsersSort] = {
    "-created_at",
    "-display_name",
    "-email",
    "created_at",
    "display_name",
    "email",
}


def check_list_users_sort(value: str) -> ListUsersSort:
    if value in LIST_USERS_SORT_VALUES:
        return cast(ListUsersSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_USERS_SORT_VALUES!r}")
