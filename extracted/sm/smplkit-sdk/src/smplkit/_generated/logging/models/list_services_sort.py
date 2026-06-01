from typing import Literal, cast

ListServicesSort = Literal["-name", "name"]

LIST_SERVICES_SORT_VALUES: set[ListServicesSort] = {
    "-name",
    "name",
}


def check_list_services_sort(value: str) -> ListServicesSort:
    if value in LIST_SERVICES_SORT_VALUES:
        return cast(ListServicesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_SERVICES_SORT_VALUES!r}")
