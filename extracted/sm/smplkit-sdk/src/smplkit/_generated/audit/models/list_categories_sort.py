from typing import Literal, cast

ListCategoriesSort = Literal["-key", "key"]

LIST_CATEGORIES_SORT_VALUES: set[ListCategoriesSort] = {
    "-key",
    "key",
}


def check_list_categories_sort(value: str) -> ListCategoriesSort:
    if value in LIST_CATEGORIES_SORT_VALUES:
        return cast(ListCategoriesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_CATEGORIES_SORT_VALUES!r}")
