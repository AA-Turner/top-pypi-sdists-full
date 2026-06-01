"""JWKS response models."""

from typing import Any

from csrd.models import BaseModel


class JWKSResponse(BaseModel):
    """JSON Web Key Set response (RFC 7517)."""

    keys: list[dict[str, Any]]
