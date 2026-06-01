from typing import Literal, cast

ListProductsSort = Literal["-display_name", "-id", "display_name", "id"]

LIST_PRODUCTS_SORT_VALUES: set[ListProductsSort] = {
    "-display_name",
    "-id",
    "display_name",
    "id",
}


def check_list_products_sort(value: str) -> ListProductsSort:
    if value in LIST_PRODUCTS_SORT_VALUES:
        return cast(ListProductsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_PRODUCTS_SORT_VALUES!r}")
