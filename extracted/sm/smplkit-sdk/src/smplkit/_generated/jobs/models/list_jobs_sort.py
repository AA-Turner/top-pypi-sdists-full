from typing import Literal, cast

ListJobsSort = Literal["-created_at", "-name", "-updated_at", "created_at", "name", "updated_at"]

LIST_JOBS_SORT_VALUES: set[ListJobsSort] = {
    "-created_at",
    "-name",
    "-updated_at",
    "created_at",
    "name",
    "updated_at",
}


def check_list_jobs_sort(value: str) -> ListJobsSort:
    if value in LIST_JOBS_SORT_VALUES:
        return cast(ListJobsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_JOBS_SORT_VALUES!r}")
