from typing import Literal, cast

ListLoggerSourcesSort = Literal[
    "-created_at", "-environment", "-last_seen", "-service", "created_at", "environment", "last_seen", "service"
]

LIST_LOGGER_SOURCES_SORT_VALUES: set[ListLoggerSourcesSort] = {
    "-created_at",
    "-environment",
    "-last_seen",
    "-service",
    "created_at",
    "environment",
    "last_seen",
    "service",
}


def check_list_logger_sources_sort(value: str) -> ListLoggerSourcesSort:
    if value in LIST_LOGGER_SOURCES_SORT_VALUES:
        return cast(ListLoggerSourcesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LOGGER_SOURCES_SORT_VALUES!r}")
