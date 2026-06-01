from typing import Literal, cast

ListMetricRollupsSort = Literal["-bucket", "bucket"]

LIST_METRIC_ROLLUPS_SORT_VALUES: set[ListMetricRollupsSort] = {
    "-bucket",
    "bucket",
}


def check_list_metric_rollups_sort(value: str) -> ListMetricRollupsSort:
    if value in LIST_METRIC_ROLLUPS_SORT_VALUES:
        return cast(ListMetricRollupsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_METRIC_ROLLUPS_SORT_VALUES!r}")
