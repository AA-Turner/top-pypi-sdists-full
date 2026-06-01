from typing import Literal, cast

OidcProvider = Literal["google", "microsoft"]

OIDC_PROVIDER_VALUES: set[OidcProvider] = {
    "google",
    "microsoft",
}


def check_oidc_provider(value: str) -> OidcProvider:
    if value in OIDC_PROVIDER_VALUES:
        return cast(OidcProvider, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OIDC_PROVIDER_VALUES!r}")
