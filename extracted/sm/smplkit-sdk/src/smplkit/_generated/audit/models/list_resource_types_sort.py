from typing import Literal, cast

ListResourceTypesSort = Literal["-key", "key"]

LIST_RESOURCE_TYPES_SORT_VALUES: set[ListResourceTypesSort] = {
    "-key",
    "key",
}


def check_list_resource_types_sort(value: str) -> ListResourceTypesSort:
    if value in LIST_RESOURCE_TYPES_SORT_VALUES:
        return cast(ListResourceTypesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_RESOURCE_TYPES_SORT_VALUES!r}")
