from typing import Literal, cast

ListDiscountTiersSort = Literal["-percent_off", "-products_count", "percent_off", "products_count"]

LIST_DISCOUNT_TIERS_SORT_VALUES: set[ListDiscountTiersSort] = {
    "-percent_off",
    "-products_count",
    "percent_off",
    "products_count",
}


def check_list_discount_tiers_sort(value: str) -> ListDiscountTiersSort:
    if value in LIST_DISCOUNT_TIERS_SORT_VALUES:
        return cast(ListDiscountTiersSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DISCOUNT_TIERS_SORT_VALUES!r}")
