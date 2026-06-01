from typing import Literal, cast

SSODomainStatus = Literal["pending", "verified"]

SSO_DOMAIN_STATUS_VALUES: set[SSODomainStatus] = {
    "pending",
    "verified",
}


def check_sso_domain_status(value: str) -> SSODomainStatus:
    if value in SSO_DOMAIN_STATUS_VALUES:
        return cast(SSODomainStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SSO_DOMAIN_STATUS_VALUES!r}")
