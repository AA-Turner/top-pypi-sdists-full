from typing import Literal, cast

ApiKeyResourceType = Literal["api_key"]

API_KEY_RESOURCE_TYPE_VALUES: set[ApiKeyResourceType] = {
    "api_key",
}


def check_api_key_resource_type(value: str) -> ApiKeyResourceType:
    if value in API_KEY_RESOURCE_TYPE_VALUES:
        return cast(ApiKeyResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {API_KEY_RESOURCE_TYPE_VALUES!r}")
