from typing import Literal, cast

EnvironmentCreateResourceType = Literal["environment"]

ENVIRONMENT_CREATE_RESOURCE_TYPE_VALUES: set[EnvironmentCreateResourceType] = {
    "environment",
}


def check_environment_create_resource_type(value: str) -> EnvironmentCreateResourceType:
    if value in ENVIRONMENT_CREATE_RESOURCE_TYPE_VALUES:
        return cast(EnvironmentCreateResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ENVIRONMENT_CREATE_RESOURCE_TYPE_VALUES!r}")
