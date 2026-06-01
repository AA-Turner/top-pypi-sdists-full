from typing import Literal, cast

ListEventTypesSort = Literal["-key", "key"]

LIST_EVENT_TYPES_SORT_VALUES: set[ListEventTypesSort] = {
    "-key",
    "key",
}


def check_list_event_types_sort(value: str) -> ListEventTypesSort:
    if value in LIST_EVENT_TYPES_SORT_VALUES:
        return cast(ListEventTypesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_EVENT_TYPES_SORT_VALUES!r}")
