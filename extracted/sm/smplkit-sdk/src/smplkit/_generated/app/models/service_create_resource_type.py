from typing import Literal, cast

ServiceCreateResourceType = Literal["service"]

SERVICE_CREATE_RESOURCE_TYPE_VALUES: set[ServiceCreateResourceType] = {
    "service",
}


def check_service_create_resource_type(value: str) -> ServiceCreateResourceType:
    if value in SERVICE_CREATE_RESOURCE_TYPE_VALUES:
        return cast(ServiceCreateResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SERVICE_CREATE_RESOURCE_TYPE_VALUES!r}")
