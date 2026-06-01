"""Self-authentication dependency for the auth service.
The auth service issues JWTs but also needs to guard its own admin
endpoints (user lookup, role management).  This dependency verifies
tokens locally using the service's own key ring — no network call
required — and delegates authority checking to the library's
``require_authorities`` guard via ``user_info_context``.
This file is scaffolded once and never overwritten.
"""
from typing import Annotated
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from csrd.auth import require_authorities
from csrd.context.platform import user_info_context
from csrd.models.claims import UserClaims
from .token_service import TokenSvc
_http_bearer = HTTPBearer()
async def _get_verified_claims(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(_http_bearer)],
    token_svc: TokenSvc,
) -> UserClaims:
    """Extract and verify claims from the bearer token, set request context."""
    resp = await token_svc.verify_token(credentials.credentials)
    claims = UserClaims(
        sub=resp.claims.sub,
        user_name=resp.claims.user_name,
        authorities=resp.claims.authorities,
    )
    user_info_context.set(claims)
    return claims
VerifiedClaims = Annotated[UserClaims, Depends(_get_verified_claims)]
_require_admin = require_authorities("ADMIN")
async def _admin_guard(_claims: VerifiedClaims) -> UserClaims:
    """Verify token + require ADMIN authority via library guard."""
    await _require_admin()
    return _claims
AdminGuard = Annotated[UserClaims, Depends(_admin_guard)]
__all__ = ("AdminGuard", "VerifiedClaims")
