from typing import Literal, cast

ListFlagSourcesSort = Literal[
    "-created_at", "-environment", "-last_seen", "-service", "created_at", "environment", "last_seen", "service"
]

LIST_FLAG_SOURCES_SORT_VALUES: set[ListFlagSourcesSort] = {
    "-created_at",
    "-environment",
    "-last_seen",
    "-service",
    "created_at",
    "environment",
    "last_seen",
    "service",
}


def check_list_flag_sources_sort(value: str) -> ListFlagSourcesSort:
    if value in LIST_FLAG_SOURCES_SORT_VALUES:
        return cast(ListFlagSourcesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_FLAG_SOURCES_SORT_VALUES!r}")
