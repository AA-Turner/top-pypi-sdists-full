# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SecretConnectionCreateParams", "Auth", "Config", "TokenBudget"]


class SecretConnectionCreateParams(TypedDict, total=False):
    auth: Required[Auth]
    """Write-only provider authentication.

    Supply a service account token for 1Password, a token for HashiCorp token auth,
    or a role ID and secret ID for HashiCorp AppRole.
    """

    name: Required[str]

    provider: Required[Literal["1password", "hashicorp_vault"]]

    config: Config

    project_id: Annotated[str, PropertyInfo(alias="projectId")]

    token_budget: Annotated[Optional[TokenBudget], PropertyInfo(alias="tokenBudget")]


class Auth(TypedDict, total=False):
    """Write-only provider authentication.

    Supply a service account token for 1Password, a token for HashiCorp token auth, or a role ID and secret ID for HashiCorp AppRole.
    """

    token: str
    """Write-only; never returned by the API."""

    mount: str

    role_id: Annotated[str, PropertyInfo(alias="roleId")]
    """Write-only; never returned by the API."""

    secret_id: Annotated[str, PropertyInfo(alias="secretId")]
    """Write-only; never returned by the API."""

    service_account_token: Annotated[str, PropertyInfo(alias="serviceAccountToken")]
    """Write-only; never returned by the API."""

    type: Literal["token", "approle"]


class Config(TypedDict, total=False):
    address: Required[str]

    ca_pem: Annotated[str, PropertyInfo(alias="caPem")]

    namespace: str


class TokenBudget(TypedDict, total=False):
    burst: Required[int]

    refill_per_second: Required[Annotated[float, PropertyInfo(alias="refillPerSecond")]]
    """Tokens per second, with at most three decimal places."""
