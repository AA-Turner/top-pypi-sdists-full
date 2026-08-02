from __future__ import annotations

from pydantic import Field

from polymarket.models.base import BaseModel
from polymarket.models.clob._validators import EpochMsOrIsoTimestamp


class ApiKeyCreds(BaseModel):
    key: str = Field(validation_alias="apiKey", repr=False)
    passphrase: str = Field(repr=False)
    secret: str = Field(repr=False)

    def __repr__(self) -> str:
        return "ApiKeyCreds(key=<redacted>, passphrase=<redacted>, secret=<redacted>)"

    def _repr_html_(self) -> str:
        from polymarket._jupyter import card

        return card(
            "ApiKeyCreds  ·  redacted",
            rows=[("key", "***"), ("passphrase", "***"), ("secret", "***")],
        )


class BuilderApiKeyInfo(BaseModel):
    """A builder API key as listed for an account — identity and lifecycle, no secret.

    Returned by ``fetch_builder_api_keys``. ``revoked_at`` is ``None`` while the key is
    active and set to the revocation time once revoked.
    """

    key: str
    created_at: EpochMsOrIsoTimestamp = Field(default=None, validation_alias="createdAt")
    revoked_at: EpochMsOrIsoTimestamp = Field(default=None, validation_alias="revokedAt")


__all__ = ["ApiKeyCreds", "BuilderApiKeyInfo"]
