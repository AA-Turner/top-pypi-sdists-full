from typing import Literal, cast

ListPlansSort = Literal["-display_name", "-id", "-sort_order", "display_name", "id", "sort_order"]

LIST_PLANS_SORT_VALUES: set[ListPlansSort] = {
    "-display_name",
    "-id",
    "-sort_order",
    "display_name",
    "id",
    "sort_order",
}


def check_list_plans_sort(value: str) -> ListPlansSort:
    if value in LIST_PLANS_SORT_VALUES:
        return cast(ListPlansSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_PLANS_SORT_VALUES!r}")
