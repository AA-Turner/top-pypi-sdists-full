from typing import Literal, cast

ListAllLoggerSourcesSort = Literal[
    "-created_at", "-environment", "-last_seen", "-service", "created_at", "environment", "last_seen", "service"
]

LIST_ALL_LOGGER_SOURCES_SORT_VALUES: set[ListAllLoggerSourcesSort] = {
    "-created_at",
    "-environment",
    "-last_seen",
    "-service",
    "created_at",
    "environment",
    "last_seen",
    "service",
}


def check_list_all_logger_sources_sort(value: str) -> ListAllLoggerSourcesSort:
    if value in LIST_ALL_LOGGER_SOURCES_SORT_VALUES:
        return cast(ListAllLoggerSourcesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_ALL_LOGGER_SOURCES_SORT_VALUES!r}")
