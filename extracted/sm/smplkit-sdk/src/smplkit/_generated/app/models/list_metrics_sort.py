from typing import Literal, cast

ListMetricsSort = Literal["-recorded_at", "-value", "recorded_at", "value"]

LIST_METRICS_SORT_VALUES: set[ListMetricsSort] = {
    "-recorded_at",
    "-value",
    "recorded_at",
    "value",
}


def check_list_metrics_sort(value: str) -> ListMetricsSort:
    if value in LIST_METRICS_SORT_VALUES:
        return cast(ListMetricsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_METRICS_SORT_VALUES!r}")
