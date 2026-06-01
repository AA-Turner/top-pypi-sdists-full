from typing import Literal, cast

SSODomainResourceType = Literal["sso_domain"]

SSO_DOMAIN_RESOURCE_TYPE_VALUES: set[SSODomainResourceType] = {
    "sso_domain",
}


def check_sso_domain_resource_type(value: str) -> SSODomainResourceType:
    if value in SSO_DOMAIN_RESOURCE_TYPE_VALUES:
        return cast(SSODomainResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SSO_DOMAIN_RESOURCE_TYPE_VALUES!r}")
