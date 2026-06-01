from typing import Literal, cast

SSOConnectionGroupRoleMappingsAdditionalProperty = Literal["ADMIN", "MEMBER", "OWNER", "VIEWER"]

SSO_CONNECTION_GROUP_ROLE_MAPPINGS_ADDITIONAL_PROPERTY_VALUES: set[SSOConnectionGroupRoleMappingsAdditionalProperty] = {
    "ADMIN",
    "MEMBER",
    "OWNER",
    "VIEWER",
}


def check_sso_connection_group_role_mappings_additional_property(
    value: str,
) -> SSOConnectionGroupRoleMappingsAdditionalProperty:
    if value in SSO_CONNECTION_GROUP_ROLE_MAPPINGS_ADDITIONAL_PROPERTY_VALUES:
        return cast(SSOConnectionGroupRoleMappingsAdditionalProperty, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SSO_CONNECTION_GROUP_ROLE_MAPPINGS_ADDITIONAL_PROPERTY_VALUES!r}"
    )
