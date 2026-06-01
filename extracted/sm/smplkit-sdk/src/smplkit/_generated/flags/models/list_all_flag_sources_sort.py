from typing import Literal, cast

ListAllFlagSourcesSort = Literal[
    "-created_at", "-environment", "-last_seen", "-service", "created_at", "environment", "last_seen", "service"
]

LIST_ALL_FLAG_SOURCES_SORT_VALUES: set[ListAllFlagSourcesSort] = {
    "-created_at",
    "-environment",
    "-last_seen",
    "-service",
    "created_at",
    "environment",
    "last_seen",
    "service",
}


def check_list_all_flag_sources_sort(value: str) -> ListAllFlagSourcesSort:
    if value in LIST_ALL_FLAG_SOURCES_SORT_VALUES:
        return cast(ListAllFlagSourcesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_ALL_FLAG_SOURCES_SORT_VALUES!r}")
