# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SecretConnectionUpdateResponse", "TokenBudget"]


class TokenBudget(BaseModel):
    burst: int

    refill_per_second: float = FieldInfo(alias="refillPerSecond")
    """Tokens per second, with at most three decimal places."""


class SecretConnectionUpdateResponse(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    enabled: bool

    name: str

    provider: Literal["1password", "hashicorp_vault"]

    token_budget: Optional[TokenBudget] = FieldInfo(alias="tokenBudget", default=None)

    updated_at: datetime = FieldInfo(alias="updatedAt")

    vault_fingerprint: str = FieldInfo(alias="vaultFingerprint")
    """For 1Password, a SHA-256 diagnostic fingerprint of sorted accessible vault IDs.

    For HashiCorp Vault, a SHA-256 fingerprint of the normalized endpoint and
    namespace. Neither proves immutable account or server identity.
    """

    version: int
