"""Supabase JWT verification (auth P1, PF-350).

The backend treats Supabase Auth (GoTrue) as the identity provider. A browser
or the accept page obtains a Supabase session; its access token is a JWT whose
`sub` claim is the Supabase `auth.users` id. We verify that token here and map
`sub` → `users.supabase_user_id`, lazily creating the mirror `users` row on
first sight.

Two verification modes, preferred order:

  1. **Asymmetric (RS256/ES256) via JWKS** — the modern Supabase default. We
     fetch the project's JWKS (`.../auth/v1/.well-known/jwks.json`) with
     PyJWT's `PyJWKClient` (which caches keys) and verify the signature against
     the matching public key. No shared secret lives in the backend.
  2. **Symmetric (HS256) fallback** — older projects sign with the shared
     `SUPABASE_JWT_SECRET`. Only used when no JWKS URL is configured.

Config (all server-side env vars):
  SUPABASE_URL           e.g. https://abcd.supabase.co  (JWKS URL derived from it)
  SUPABASE_JWKS_URL      explicit override for the JWKS endpoint (optional)
  SUPABASE_JWT_SECRET    HS256 fallback secret (optional)
  SUPABASE_JWT_AUD       expected `aud` claim, default "authenticated"
"""

import os
from functools import lru_cache
from typing import Any, Dict, Optional

import jwt
from jwt import PyJWKClient

# GoTrue stamps this on every user access token.
DEFAULT_AUDIENCE = "authenticated"


class SupabaseAuthError(Exception):
    """Raised when a Supabase JWT cannot be verified."""


def _jwks_url() -> Optional[str]:
    """Resolve the JWKS endpoint from explicit override or SUPABASE_URL."""
    explicit = os.getenv("SUPABASE_JWKS_URL")
    if explicit:
        return explicit
    base = os.getenv("SUPABASE_URL")
    if not base:
        return None
    return f"{base.rstrip('/')}/auth/v1/.well-known/jwks.json"


@lru_cache(maxsize=4)
def _jwk_client(url: str) -> PyJWKClient:
    """Cache one PyJWKClient per JWKS URL (it caches signing keys internally)."""
    return PyJWKClient(url)


def supabase_auth_configured() -> bool:
    """True if either JWKS or the HS256 secret is configured."""
    return bool(_jwks_url() or os.getenv("SUPABASE_JWT_SECRET"))


def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    """Verify a Supabase access token and return its decoded claims.

    Tries JWKS (asymmetric) first, then the HS256 shared-secret fallback.
    Raises SupabaseAuthError on any failure (bad signature, wrong audience,
    expired, or no verification method configured).
    """
    audience = os.getenv("SUPABASE_JWT_AUD", DEFAULT_AUDIENCE)

    jwks_url = _jwks_url()
    if jwks_url:
        try:
            signing_key = _jwk_client(jwks_url).get_signing_key_from_jwt(token)
            return jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256", "ES256"],
                audience=audience,
                options={"verify_aud": True},
            )
        except jwt.PyJWTError as exc:
            # Fall through to the HS256 path only if a secret is configured;
            # otherwise surface the JWKS failure directly.
            if not os.getenv("SUPABASE_JWT_SECRET"):
                raise SupabaseAuthError(f"JWKS verification failed: {exc}") from exc

    secret = os.getenv("SUPABASE_JWT_SECRET")
    if secret:
        try:
            return jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                audience=audience,
                options={"verify_aud": True},
            )
        except jwt.PyJWTError as exc:
            raise SupabaseAuthError(f"HS256 verification failed: {exc}") from exc

    raise SupabaseAuthError(
        "No Supabase verification method configured "
        "(set SUPABASE_URL/SUPABASE_JWKS_URL or SUPABASE_JWT_SECRET)."
    )


def extract_identity(claims: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Pull the InnoDay-relevant identity fields out of verified JWT claims."""
    meta = claims.get("user_metadata") or {}
    return {
        "supabase_user_id": claims.get("sub"),
        "email": claims.get("email") or meta.get("email"),
        "full_name": meta.get("full_name") or meta.get("name"),
        # Supabase puts the confirmation timestamp on the token; we used to drop
        # it, so there was no way to know whether the address was ever proven.
        # GoTrue emits `email_verified` in user_metadata and, on some versions,
        # a top-level `email_confirmed_at` -- accept either.
        "email_confirmed_at": (
            claims.get("email_confirmed_at") or meta.get("email_verified") or None
        ),
    }
