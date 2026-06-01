"""Token service for JWT issuance and verification.

Encapsulates all JWT business logic: signing, verification, and
claims construction. Views call service methods and return the result.

This file is scaffolded once and never overwritten.
"""

import time
from typing import Any

import jwt as pyjwt
from fastapi import HTTPException
from jwt.algorithms import RSAAlgorithm

from csrd.auth import KeyRingManager

from ..models.auth import TokenResponse, VerifyClaims, VerifyResponse


class TokenService:
    """JWT token issuance and verification."""

    def __init__(self, key_ring: KeyRingManager, settings: Any) -> None:
        self._key_ring = key_ring
        self._settings = settings

    async def issue_token(
        self,
        *,
        user_id: str,
        username: str,
        roles: list[str],
    ) -> TokenResponse:
        """Create a signed JWT for the given user."""
        await self._key_ring.rotate_if_needed()
        kid, private_key = await self._key_ring.active_key()

        now = int(time.time())
        payload: dict[str, Any] = {
            "sub": user_id,
            "user_name": username,
            "authorities": roles,
            "iat": now,
            "exp": now + self._settings.jwt_ttl_seconds,
            "iss": self._settings.jwt_issuer,
            "aud": self._settings.jwt_audience,
        }

        token = pyjwt.encode(
            payload,
            private_key,
            algorithm=self._settings.jwt_algorithm,
            headers={"kid": kid},
        )

        return TokenResponse(access_token=token, expires_in=self._settings.jwt_ttl_seconds)

    async def verify_token(self, token: str) -> VerifyResponse:
        """Verify a JWT and return its claims. Raises on failure."""
        jwks = await self._key_ring.jwks_dict()

        try:
            unverified = pyjwt.get_unverified_header(token)
            kid = unverified.get("kid")

            jwk_data = next(
                (k for k in jwks["keys"] if k["kid"] == kid),
                None,
            )
            if jwk_data is None:
                raise HTTPException(status_code=401, detail="Unknown signing key")

            public_key = RSAAlgorithm.from_jwk(jwk_data)

            claims = pyjwt.decode(
                token,
                public_key,
                algorithms=[self._settings.jwt_algorithm],
                issuer=self._settings.jwt_issuer,
                audience=self._settings.jwt_audience,
            )
            return VerifyResponse(active=True, claims=VerifyClaims(**claims))

        except pyjwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired") from None
        except pyjwt.InvalidTokenError as exc:
            raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from None


__all__ = ("TokenService",)
