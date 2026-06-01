"""JWKS endpoint — serves public signing keys for token verification.

Consumers use ``JWKSKeyProvider`` to auto-discover keys from this endpoint.
This file is scaffolded once and never overwritten.
"""

from fastapi import APIRouter

from ..dependencies.db import KeyRing
from ..models.jwks import JWKSResponse

router = APIRouter(tags=["jwks"])



@router.get("/.well-known/jwks.json", response_model=JWKSResponse)
async def jwks(key_ring: KeyRing) -> JWKSResponse:
    """Return public keys for all active signing keys in JWK format.

    Consumers cache this response and refresh automatically when
    they encounter an unknown ``kid`` in a token header.
    """
    jwks_data = await key_ring.jwks_dict()
    return JWKSResponse(keys=jwks_data["keys"])
