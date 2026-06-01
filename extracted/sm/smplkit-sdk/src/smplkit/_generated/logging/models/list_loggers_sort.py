from typing import Literal, cast

ListLoggersSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_LOGGERS_SORT_VALUES: set[ListLoggersSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_loggers_sort(value: str) -> ListLoggersSort:
    if value in LIST_LOGGERS_SORT_VALUES:
        return cast(ListLoggersSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LOGGERS_SORT_VALUES!r}")
