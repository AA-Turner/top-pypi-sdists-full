# ruff: noqa: B904
"""Built-in authenticator implementations."""

import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import jwt as pyjwt
from fastapi import HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from csrd.logging import auth_error_detail
from csrd.models.claims import UserClaims

from ._key_providers import _coerce_key_provider
from ._protocols import AuthCallback, Authenticator, KeySource

logger = logging.getLogger(__name__)


def _default_claims_mapper(payload: dict[str, Any]) -> UserClaims:
    sub = payload.get("sub", "")
    user_name = (
        payload.get("user_name")
        or payload.get("preferred_username")
        or payload.get("email")
        or sub
        or ""
    )

    authorities = payload.get("authorities") or payload.get("roles") or []
    if isinstance(authorities, str):
        authorities = authorities.split()

    # Map iat (issued at) from Unix timestamp to datetime.
    # NOTE: Currently no external consumers expose iat/exp via API responses.
    # This mapping is defensive and future-proof but should be revisited once
    # auth-service or generic-service expose temporal claims in their verify/token endpoints.
    # If decomissioning is needed, this can be simplified or removed entirely.
    iat = None
    if "iat" in payload:
        try:
            iat_timestamp = payload["iat"]
            if isinstance(iat_timestamp, (int, float)):
                iat = datetime.fromtimestamp(iat_timestamp, tz=UTC)
        except (ValueError, OSError, TypeError):
            # Invalid timestamp; let UserClaims use default
            pass

    # Map exp (expiration) from Unix timestamp to datetime.
    exp = None
    if "exp" in payload:
        try:
            exp_timestamp = payload["exp"]
            if isinstance(exp_timestamp, (int, float)):
                exp = datetime.fromtimestamp(exp_timestamp, tz=UTC)
        except (ValueError, OSError, TypeError):
            # Invalid timestamp; let UserClaims use default
            pass

    kwargs = {
        "sub": sub,
        "user_name": user_name,
        "authorities": list(authorities),
    }
    if iat is not None:
        kwargs["iat"] = iat
    if exp is not None:
        kwargs["exp"] = exp

    return UserClaims(**kwargs)


@dataclass
class JWTAuthenticator:
    """Decode and verify a JWT token locally using PyJWT."""

    key: KeySource | None = None
    algorithms: list[str] = field(default_factory=lambda: ["HS256"])
    audience: str | None = None
    issuer: str | None = None
    options: dict[str, Any] = field(default_factory=dict)
    claims_mapper: Callable[[dict[str, Any]], UserClaims] | None = None

    def __post_init__(self) -> None:
        self._key_provider = _coerce_key_provider(self.key)

    async def verify_token(self, token: str, app: Any = None) -> UserClaims:
        """Decode and verify *token* without requiring a :class:`Request`.

        Parameters
        ----------
        token:
            The raw JWT string.
        app:
            Optional application instance passed through to the
            :class:`KeyProvider`.  Required when the configured key
            provider needs ``app`` (e.g. :class:`EnvKeyProvider`).

        Returns
        -------
        UserClaims
            The validated and mapped claims.

        Raises
        ------
        HTTPException
            On any validation failure (malformed, expired, invalid).
        """
        mapper = self.claims_mapper or _default_claims_mapper

        try:
            unverified_headers = pyjwt.get_unverified_header(token)
        except pyjwt.DecodeError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Malformed token")

        resolved = self._key_provider(unverified_headers, app)
        if inspect.isawaitable(resolved):
            resolved = await resolved

        decode_kwargs: dict[str, Any] = {
            "algorithms": self.algorithms,
            "options": dict(self.options),
        }
        if self.audience is not None:
            decode_kwargs["audience"] = self.audience
        if self.issuer is not None:
            decode_kwargs["issuer"] = self.issuer

        try:
            payload = pyjwt.decode(token, resolved, **decode_kwargs)
        except pyjwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=auth_error_detail("Token has expired"),
            )
        except pyjwt.InvalidTokenError as exc:
            logger.debug("JWT validation failed: %s", exc)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=auth_error_detail(f"Invalid token: {exc}"),
            )

        return mapper(payload)

    async def __call__(self, request: Request, token: str) -> UserClaims:
        return await self.verify_token(token, request.app)


@dataclass
class StaticAuthenticator:
    """Accept a fixed token value and return preconfigured claims."""

    token: str
    claims: UserClaims = field(default_factory=lambda: UserClaims(sub="static"))

    async def __call__(self, request: Request, token: str) -> UserClaims:
        import hmac

        if not hmac.compare_digest(token, self.token):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return self.claims


@dataclass
class RemoteAuthenticator:
    """Validate the token by calling an upstream HTTP endpoint."""

    url: str
    method: str = "GET"
    token_header: str = "Authorization"
    token_prefix: str = "Bearer "
    claims_mapper: Callable[[dict[str, Any]], UserClaims] | None = None
    httpx_client_kwargs: dict[str, Any] = field(default_factory=dict)
    client: Any = None

    async def __call__(self, request: Request, token: str) -> UserClaims:
        import httpx

        mapper = self.claims_mapper or _default_claims_mapper
        headers = {self.token_header: f"{self.token_prefix}{token}"}

        async def _do_request(c: httpx.AsyncClient) -> httpx.Response:
            try:
                return await c.request(self.method, self.url, headers=headers)
            except httpx.HTTPError as exc:
                logger.warning("Remote auth request failed: %s", exc)
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Authentication service unavailable",
                )

        if self.client is not None:
            resp = await _do_request(self.client)
        else:
            client_kwargs = {"timeout": 10.0, **self.httpx_client_kwargs}
            async with httpx.AsyncClient(**client_kwargs) as client:
                resp = await _do_request(client)

        if resp.status_code >= 400:
            logger.debug(
                "Remote auth rejected token: status=%d body=%s",
                resp.status_code,
                resp.text[:200],
            )
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token rejected by authentication service",
            )

        try:
            payload = resp.json()
        except Exception:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid response from authentication service",
            )

        if isinstance(payload, dict) and payload.get("active") is False:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token is not active",
            )

        return mapper(payload)


@dataclass
class CallbackAuthenticator:
    """Delegate authentication to an arbitrary user-provided function."""

    callback: AuthCallback

    async def __call__(self, request: Request, token: str) -> UserClaims:
        try:
            result = self.callback(request, token)
            if inspect.isawaitable(result):
                result = await result
        except HTTPException:
            raise
        except Exception as exc:
            logger.debug("Callback authenticator failed: %s", exc)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
            ) from exc

        if not isinstance(result, UserClaims):
            raise TypeError(
                f"Authenticator callback must return UserClaims, got {type(result).__name__}"
            )
        return result


@dataclass
class ChainedAuthenticator:
    """Try multiple authenticators in order; first success wins."""

    authenticators: list[Authenticator | Any] = field(default_factory=list)

    async def __call__(self, request: Request, token: str) -> UserClaims:
        last_exc: HTTPException | None = None
        for auth in self.authenticators:
            try:
                result = auth(request, token)
                if inspect.isawaitable(result):
                    result = await result
                return result
            except HTTPException as exc:
                last_exc = exc
                continue

        raise last_exc or HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="All authenticators failed",
        )
