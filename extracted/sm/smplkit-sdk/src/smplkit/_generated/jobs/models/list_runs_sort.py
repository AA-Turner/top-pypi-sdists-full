from typing import Literal, cast

ListRunsSort = Literal[
    "-created_at",
    "-finished_at",
    "-job",
    "-scheduled_for",
    "-started_at",
    "-status",
    "-total_duration_ms",
    "created_at",
    "finished_at",
    "job",
    "scheduled_for",
    "started_at",
    "status",
    "total_duration_ms",
]

LIST_RUNS_SORT_VALUES: set[ListRunsSort] = {
    "-created_at",
    "-finished_at",
    "-job",
    "-scheduled_for",
    "-started_at",
    "-status",
    "-total_duration_ms",
    "created_at",
    "finished_at",
    "job",
    "scheduled_for",
    "started_at",
    "status",
    "total_duration_ms",
}


def check_list_runs_sort(value: str) -> ListRunsSort:
    if value in LIST_RUNS_SORT_VALUES:
        return cast(ListRunsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_RUNS_SORT_VALUES!r}")
