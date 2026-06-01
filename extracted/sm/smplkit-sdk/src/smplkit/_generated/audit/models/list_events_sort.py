from typing import Literal, cast

ListEventsSort = Literal["-created_at", "-occurred_at", "created_at", "occurred_at"]

LIST_EVENTS_SORT_VALUES: set[ListEventsSort] = {
    "-created_at",
    "-occurred_at",
    "created_at",
    "occurred_at",
}


def check_list_events_sort(value: str) -> ListEventsSort:
    if value in LIST_EVENTS_SORT_VALUES:
        return cast(ListEventsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_EVENTS_SORT_VALUES!r}")
