from typing import Literal, cast

GroupMembershipResourceType = Literal["group_membership"]

GROUP_MEMBERSHIP_RESOURCE_TYPE_VALUES: set[GroupMembershipResourceType] = {
    "group_membership",
}


def check_group_membership_resource_type(value: str) -> GroupMembershipResourceType:
    if value in GROUP_MEMBERSHIP_RESOURCE_TYPE_VALUES:
        return cast(GroupMembershipResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GROUP_MEMBERSHIP_RESOURCE_TYPE_VALUES!r}")
