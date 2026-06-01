from typing import Literal, cast

ListForwarderDeliveriesSort = Literal["-created_at", "created_at"]

LIST_FORWARDER_DELIVERIES_SORT_VALUES: set[ListForwarderDeliveriesSort] = {
    "-created_at",
    "created_at",
}


def check_list_forwarder_deliveries_sort(value: str) -> ListForwarderDeliveriesSort:
    if value in LIST_FORWARDER_DELIVERIES_SORT_VALUES:
        return cast(ListForwarderDeliveriesSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_FORWARDER_DELIVERIES_SORT_VALUES!r}")
