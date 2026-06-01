from typing import Literal, cast

ListGroupMembershipsSort = Literal["-created_at", "-updated_at", "created_at", "updated_at"]

LIST_GROUP_MEMBERSHIPS_SORT_VALUES: set[ListGroupMembershipsSort] = {
    "-created_at",
    "-updated_at",
    "created_at",
    "updated_at",
}


def check_list_group_memberships_sort(value: str) -> ListGroupMembershipsSort:
    if value in LIST_GROUP_MEMBERSHIPS_SORT_VALUES:
        return cast(ListGroupMembershipsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_GROUP_MEMBERSHIPS_SORT_VALUES!r}")
