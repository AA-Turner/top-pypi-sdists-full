from typing import Literal, cast

GroupResourceType = Literal["group"]

GROUP_RESOURCE_TYPE_VALUES: set[GroupResourceType] = {
    "group",
}


def check_group_resource_type(value: str) -> GroupResourceType:
    if value in GROUP_RESOURCE_TYPE_VALUES:
        return cast(GroupResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GROUP_RESOURCE_TYPE_VALUES!r}")
