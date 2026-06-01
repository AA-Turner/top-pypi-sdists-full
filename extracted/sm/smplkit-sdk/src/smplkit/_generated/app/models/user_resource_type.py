from typing import Literal, cast

UserResourceType = Literal["user"]

USER_RESOURCE_TYPE_VALUES: set[UserResourceType] = {
    "user",
}


def check_user_resource_type(value: str) -> UserResourceType:
    if value in USER_RESOURCE_TYPE_VALUES:
        return cast(UserResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_RESOURCE_TYPE_VALUES!r}")
