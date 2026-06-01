"""Dependency factory functions for FastAPI auth integration."""

import inspect
from collections.abc import Callable
from typing import Any

from fastapi import Request

from csrd.context.platform import user_info_context
from csrd.models.claims import UserClaims

from ._authenticators import (
    CallbackAuthenticator,
    ChainedAuthenticator,
    JWTAuthenticator,
    RemoteAuthenticator,
    StaticAuthenticator,
)
from ._protocols import AuthCallback, Authenticator, KeySource


def create_bearer_dependency(
    authenticator: Authenticator | AuthCallback,
    *,
    token_finder: Callable[[], str] | None = None,
) -> Callable:
    """Build a FastAPI dependency from any :class:`Authenticator`.

    Parameters
    ----------
    authenticator:
        The authenticator instance or callback to use.
    token_finder:
        Zero-arg callable that extracts the bearer token from the
        current request context. When *None*, the token must be
        provided by a framework-level mechanism (e.g. the versioning
        dispatch middleware populates the contextvar automatically).
    """
    if not isinstance(
        authenticator,
        (
            JWTAuthenticator,
            StaticAuthenticator,
            RemoteAuthenticator,
            CallbackAuthenticator,
            ChainedAuthenticator,
        ),
    ) and callable(authenticator):
        authenticator = CallbackAuthenticator(authenticator)

    async def _bearer_dependency(request: Request) -> UserClaims:
        if token_finder is not None:
            token = token_finder()
        else:
            # Fallback: extract bearer token directly from the request.
            auth_header = request.headers.get("authorization", "")
            if auth_header.lower().startswith("bearer "):
                token = auth_header[7:].strip()
            else:
                token = auth_header.strip()
            if not token:
                from fastapi import HTTPException

                raise HTTPException(status_code=401, detail="Unauthorized")

        result = authenticator(request, token)
        if inspect.isawaitable(result):
            claims = await result
        else:
            claims = result

        user_info_context.set(claims)
        return claims

    return _bearer_dependency


def create_jwt_bearer(
    *,
    key: KeySource | None = None,
    algorithms: list[str] | None = None,
    audience: str | None = None,
    issuer: str | None = None,
    options: dict[str, Any] | None = None,
    claims_mapper: Callable[[dict[str, Any]], UserClaims] | None = None,
    token_finder: Callable[[], str] | None = None,
) -> Callable:
    """Convenience shortcut: build a JWT bearer dependency."""
    return create_bearer_dependency(
        JWTAuthenticator(
            key=key,
            algorithms=algorithms or ["HS256"],
            audience=audience,
            issuer=issuer,
            options=options or {},
            claims_mapper=claims_mapper,
        ),
        token_finder=token_finder,
    )
