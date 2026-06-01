from typing import Literal, cast

ServiceResourceType = Literal["service"]

SERVICE_RESOURCE_TYPE_VALUES: set[ServiceResourceType] = {
    "service",
}


def check_service_resource_type(value: str) -> ServiceResourceType:
    if value in SERVICE_RESOURCE_TYPE_VALUES:
        return cast(ServiceResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SERVICE_RESOURCE_TYPE_VALUES!r}")
