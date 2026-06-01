from typing import Literal, cast

SSOConnectionResourceType = Literal["sso_connection"]

SSO_CONNECTION_RESOURCE_TYPE_VALUES: set[SSOConnectionResourceType] = {
    "sso_connection",
}


def check_sso_connection_resource_type(value: str) -> SSOConnectionResourceType:
    if value in SSO_CONNECTION_RESOURCE_TYPE_VALUES:
        return cast(SSOConnectionResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SSO_CONNECTION_RESOURCE_TYPE_VALUES!r}")
