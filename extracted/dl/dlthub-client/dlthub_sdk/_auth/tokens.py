"""Reading claims off an access token."""

from __future__ import annotations

# Python internals
import time

# Other libraries
import jwt
from jwt import PyJWTError

# Current package
from dlthub_sdk._auth.types import TokenClaims
from dlthub_sdk.errors import NotAuthenticated

#: Treat a token this close to expiry as already expired, so a call cannot race
#: the deadline between the check and the request reaching the platform.
EXPIRY_MARGIN_SECONDS = 60


def decode_token(token: str | bytes) -> TokenClaims:
    """Read the claims out of an access token without verifying it.

    Args:
        token: The encoded JWT.

    Returns:
        Its claims.

    Raises:
        NotAuthenticated: The token does not decode, or omits a claim the
            platform always sets.
    """
    raw = token.encode("utf-8") if isinstance(token, str) else token
    try:
        payload = jwt.decode(
            raw,
            key="",
            algorithms=["EdDSA"],
            options={
                "verify_signature": False,
                "verify_exp": False,
                "verify_aud": False,
            },
        )
    except PyJWTError as e:
        raise NotAuthenticated("token could not be decoded") from e

    flags = payload.get("feature_flags") or []
    try:
        return TokenClaims(
            email=payload["email"],
            user_id=payload["sub"],
            expires_at=payload.get("exp"),
            feature_flags=tuple(f for f in flags if isinstance(f, str)),
        )
    except (KeyError, TypeError) as e:
        raise NotAuthenticated("token is missing a required claim") from e


def is_expiring(
    claims: TokenClaims, *, margin_seconds: int = EXPIRY_MARGIN_SECONDS
) -> bool:
    """Whether a token is expired, or close enough that it should be refreshed.

    Args:
        claims: The token's claims.
        margin_seconds: Treat expiry this many seconds early.

    Returns:
        ``True`` when it should be refreshed. A token carrying no ``exp`` never
        expires on its own, so this is ``False``.
    """
    if claims.expires_at is None:
        return False
    return claims.expires_at - margin_seconds <= time.time()
