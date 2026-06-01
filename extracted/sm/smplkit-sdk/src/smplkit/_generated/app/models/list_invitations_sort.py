from typing import Literal, cast

ListInvitationsSort = Literal["-created_at", "-email", "-status", "created_at", "email", "status"]

LIST_INVITATIONS_SORT_VALUES: set[ListInvitationsSort] = {
    "-created_at",
    "-email",
    "-status",
    "created_at",
    "email",
    "status",
}


def check_list_invitations_sort(value: str) -> ListInvitationsSort:
    if value in LIST_INVITATIONS_SORT_VALUES:
        return cast(ListInvitationsSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_INVITATIONS_SORT_VALUES!r}")
