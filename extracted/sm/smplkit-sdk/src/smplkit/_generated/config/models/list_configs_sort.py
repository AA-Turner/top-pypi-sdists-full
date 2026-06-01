from typing import Literal, cast

ListConfigsSort = Literal["-created_at", "-key", "-name", "-updated_at", "created_at", "key", "name", "updated_at"]

LIST_CONFIGS_SORT_VALUES: set[ListConfigsSort] = {
    "-created_at",
    "-key",
    "-name",
    "-updated_at",
    "created_at",
    "key",
    "name",
    "updated_at",
}


def check_list_configs_sort(value: str) -> ListConfigsSort:
    if value in LIST_CONFIGS_SORT_VALUES:
        return cast(ListConfigsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_CONFIGS_SORT_VALUES!r}")
