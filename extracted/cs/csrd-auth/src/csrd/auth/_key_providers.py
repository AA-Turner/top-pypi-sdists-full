# ruff: noqa: B904
"""Built-in key provider implementations."""

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from fastapi import HTTPException
from pydantic import SecretStr
from starlette.status import HTTP_401_UNAUTHORIZED

from csrd.logging import auth_error_detail

from ._protocols import KeyCallback, KeyProvider, KeySource

logger = logging.getLogger(__name__)


@dataclass
class StaticKeyProvider:
    """A single fixed key — HMAC secret string, PEM-encoded public key, or raw bytes."""

    key: str | bytes | SecretStr

    def __call__(self, token_headers: dict[str, Any], app: Any) -> str | bytes:
        if isinstance(self.key, SecretStr):
            return self.key.get_secret_value()
        return self.key


@dataclass
class EnvKeyProvider:
    """Read the JWT key from ``app.state`` or a fallback settings loader.

    Parameters
    ----------
    state_key:
        Attribute name on ``app.state`` where a settings object with a
        ``jwt_secret`` field is stored. Defaults to ``"_versioning_settings"``.
    settings_loader:
        Zero-arg callable that returns a settings object with a
        ``jwt_secret`` attribute. Called when ``app.state`` lookup fails.
        If *None* and the state lookup also fails, a ``RuntimeError``
        is raised.
    """

    state_key: str = "_versioning_settings"
    settings_loader: Callable[[], Any] | None = None

    def __call__(self, token_headers: dict[str, Any], app: Any) -> str:
        settings = getattr(app.state, self.state_key, None)
        if settings is None and self.settings_loader is not None:
            settings = self.settings_loader()

        if settings is None:
            raise RuntimeError(
                "No JWT secret configured. Set the JWT_SECRET env var, "
                "pass key= to JWTAuthenticator, or use a KeyProvider."
            )

        jwt_key = getattr(settings, "jwt_secret", None)
        if jwt_key is None:
            raise RuntimeError(
                "No JWT secret configured. Set the JWT_SECRET env var, "
                "pass key= to JWTAuthenticator, or use a KeyProvider."
            )
        return jwt_key.get_secret_value() if isinstance(jwt_key, SecretStr) else str(jwt_key)


@dataclass
class JWKSKeyProvider:
    """Fetch signing keys from a JWKS (JSON Web Key Set) endpoint."""

    url: str
    cache_ttl: float = 300.0
    httpx_kwargs: dict[str, Any] = field(default_factory=dict)

    _jwk_set: Any = field(default=None, init=False, repr=False)
    _fetched_at: float = field(default=0.0, init=False, repr=False)

    async def __call__(self, token_headers: dict[str, Any], app: Any) -> Any:
        kid = token_headers.get("kid")
        alg = token_headers.get("alg", "RS256")

        key = self._find_key(kid, alg)
        if key is not None:
            return key

        await self._async_refresh()
        key = self._find_key(kid, alg)
        if key is not None:
            return key

        if kid:
            logger.debug("JWKS key lookup failed: no matching key for kid=%s", kid)
        else:
            logger.debug("JWKS key lookup failed: no keys available")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=auth_error_detail(
                f"No matching key found in JWKS (kid={kid})" if kid else "No keys in JWKS",
            ),
        )

    def _find_key(self, kid: str | None, alg: str) -> Any:
        if self._jwk_set is None or (time.monotonic() - self._fetched_at > self.cache_ttl):
            return None

        try:
            from jwt import PyJWKSet  # noqa: F401 — availability check
        except ImportError:
            raise RuntimeError(
                "JWKSKeyProvider requires PyJWT[crypto]. Install with: pip install 'PyJWT[crypto]'"
            ) from None

        for jwk in self._jwk_set.keys:
            jwk_kid = getattr(jwk, "key_id", None)
            if kid is not None and jwk_kid != kid:
                continue
            return jwk.key
        return None

    async def _async_refresh(self) -> None:
        if self._jwk_set is not None and time.monotonic() - self._fetched_at <= self.cache_ttl:
            return

        import httpx

        try:
            from jwt import PyJWKSet
        except ImportError:
            raise RuntimeError(
                "JWKSKeyProvider requires PyJWT[crypto]. Install with: pip install 'PyJWT[crypto]'"
            ) from None

        kwargs = {"timeout": 10.0, **self.httpx_kwargs}
        try:
            async with httpx.AsyncClient(**kwargs) as client:
                resp = await client.get(self.url)
            resp.raise_for_status()
            self._jwk_set = PyJWKSet.from_dict(resp.json())
            self._fetched_at = time.monotonic()
            logger.debug(
                "Refreshed JWKS from %s: %d key(s)",
                self.url,
                len(self._jwk_set.keys),
            )
        except Exception as exc:
            logger.warning("Failed to fetch JWKS from %s: %s", self.url, exc)
            if self._jwk_set is None:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Unable to fetch signing keys",
                )


@dataclass
class MultiKeyProvider:
    """Route to different keys by ``kid`` JWT header, or try all keys in order."""

    providers: dict[str, KeyProvider | str | bytes] | list[KeyProvider | str | bytes]

    def __call__(self, token_headers: dict[str, Any], app: Any) -> Any:
        kid = token_headers.get("kid")

        if isinstance(self.providers, dict):
            if kid is not None and kid in self.providers:
                return self._resolve_one(self.providers[kid], token_headers, app)

            for provider in self.providers.values():
                try:
                    return self._resolve_one(provider, token_headers, app)
                except Exception:
                    continue

            if kid:
                logger.debug("MultiKeyProvider: no key found for kid=%s", kid)
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=auth_error_detail(
                    f"No key found for kid={kid}" if kid else "No matching key",
                ),
            )

        last_exc: Exception | None = None
        for provider in self.providers:
            try:
                return self._resolve_one(provider, token_headers, app)
            except Exception as exc:
                last_exc = exc
                continue

        raise last_exc or HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=auth_error_detail("No matching key"),
        )

    @staticmethod
    def _resolve_one(
        provider: KeyProvider | str | bytes, token_headers: dict[str, Any], app: Any
    ) -> Any:
        if isinstance(provider, (str, bytes)):
            return provider
        if isinstance(provider, SecretStr):
            return provider.get_secret_value()
        return provider(token_headers, app)


@dataclass
class CallbackKeyProvider:
    """Delegate key resolution to any user-supplied function."""

    callback: KeyCallback

    def __call__(self, token_headers: dict[str, Any], app: Any) -> Any:
        return self.callback(token_headers, app)


# ── Coerce raw values into KeyProvider instances ────────────────────────


def _coerce_key_provider(key: KeySource | None) -> KeyProvider:
    if key is None:
        return EnvKeyProvider()
    if isinstance(key, KeyProvider):
        return key
    if isinstance(key, (str, bytes, SecretStr)):
        return StaticKeyProvider(key)
    if callable(key):
        return CallbackKeyProvider(key)
    raise TypeError(
        f"key must be a string, bytes, SecretStr, KeyProvider, or callable — "
        f"got {type(key).__name__}"
    )
