"""Islo SDK client with automatic API key exchange and token refresh."""

from __future__ import annotations

import os
import typing

import httpx

from .base_client import AsyncBaseIslo, BaseIslo
from .core.logging import LogConfig, Logger
from .custom.auth import AsyncTokenProvider, SyncTokenProvider
from .environment import IsloEnvironment

_DEFAULT_BASE_URL = "https://api.islo.dev"
_DEFAULT_COMPUTE_URL = "https://ca.compute.islo.dev"
_ENV_API_KEY = "ISLO_API_KEY"
_ENV_BASE_URL = "ISLO_BASE_URL"
_ENV_COMPUTE_URL = "ISLO_COMPUTE_URL"


def _resolve_auth(
    base_url: str,
    api_key: str | None,
) -> SyncTokenProvider | None:
    """Resolve authentication: api_key (or ISLO_API_KEY env) → auto-refreshing provider."""
    resolved_key = api_key or os.environ.get(_ENV_API_KEY)
    if resolved_key is not None:
        return SyncTokenProvider(base_url, resolved_key)
    return None


def _resolve_async_auth(
    base_url: str,
    api_key: str | None,
    async_token: typing.Callable[[], typing.Awaitable[str]] | None,
) -> typing.Callable[[], typing.Awaitable[str]] | None:
    """Resolve async authentication: explicit async_token wins, else api_key → async provider."""
    if async_token is not None:
        return async_token
    resolved_key = api_key or os.environ.get(_ENV_API_KEY)
    if resolved_key is not None:
        return AsyncTokenProvider(base_url, resolved_key)
    return None


def _resolve_environment(
    *,
    base_url: str | None,
    compute_url: str | None,
    environment: IsloEnvironment | None,
) -> IsloEnvironment:
    """Resolve dual control/compute URLs with explicit values taking precedence."""
    if environment is not None and base_url is None and compute_url is None:
        return environment

    return IsloEnvironment(
        control=base_url
        or os.environ.get(_ENV_BASE_URL)
        or (environment.control if environment is not None else None)
        or _DEFAULT_BASE_URL,
        compute=compute_url
        or os.environ.get(_ENV_COMPUTE_URL)
        or (environment.compute if environment is not None else None)
        or _DEFAULT_COMPUTE_URL,
    )


class Islo(BaseIslo):
    """Islo sandbox platform client (synchronous).

    Provide an ``api_key`` and the client automatically exchanges it for
    a session JWT and refreshes it before expiry.

    .. code-block:: python

        client = Islo(api_key="ak_...")
        # or set ISLO_API_KEY env var
        client = Islo()

    Parameters
    ----------
    api_key : str, optional
        Islo API key. Exchanged for a short-lived JWT automatically.
        Falls back to the ``ISLO_API_KEY`` environment variable.
    base_url : str, optional
        Control-plane API base URL. Defaults to ``ISLO_BASE_URL`` env var or
        ``https://api.islo.dev``.
    compute_url : str, optional
        Compute-plane API base URL. Defaults to ``ISLO_COMPUTE_URL`` env var or
        ``https://ca.compute.islo.dev``.
    environment : IsloEnvironment, optional
        Fully resolved Fern environment. Explicit ``base_url`` and
        ``compute_url`` values override the corresponding URL.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        compute_url: str | None = None,
        environment: IsloEnvironment | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        follow_redirects: bool | None = True,
        httpx_client: httpx.Client | None = None,
        logging: LogConfig | Logger | None = None,
    ):
        resolved_environment = _resolve_environment(
            base_url=base_url,
            compute_url=compute_url,
            environment=environment,
        )
        resolved_token = _resolve_auth(resolved_environment.control, api_key)

        super().__init__(
            environment=resolved_environment,
            api_key=resolved_token,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
            logging=logging,
        )


class AsyncIslo(AsyncBaseIslo):
    """Islo sandbox platform client (asynchronous).

    Provide an ``api_key`` and the client automatically exchanges it for
    a session JWT and refreshes it before expiry.

    .. code-block:: python

        client = AsyncIslo(api_key="ak_...")
        # or set ISLO_API_KEY env var
        client = AsyncIslo()

    Parameters
    ----------
    api_key : str, optional
        Islo API key. Exchanged for a short-lived JWT automatically.
        Falls back to the ``ISLO_API_KEY`` environment variable.
    async_token : callable, optional
        Async callable returning a JWT. Use this to plug in custom
        async-aware token resolution; when provided, ``api_key`` is ignored.
    base_url : str, optional
        Control-plane API base URL. Defaults to ``ISLO_BASE_URL`` env var or
        ``https://api.islo.dev``.
    compute_url : str, optional
        Compute-plane API base URL. Defaults to ``ISLO_COMPUTE_URL`` env var or
        ``https://ca.compute.islo.dev``.
    environment : IsloEnvironment, optional
        Fully resolved Fern environment. Explicit ``base_url`` and
        ``compute_url`` values override the corresponding URL.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        compute_url: str | None = None,
        environment: IsloEnvironment | None = None,
        async_token: typing.Callable[[], typing.Awaitable[str]] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        follow_redirects: bool | None = True,
        httpx_client: httpx.AsyncClient | None = None,
        logging: LogConfig | Logger | None = None,
    ):
        resolved_environment = _resolve_environment(
            base_url=base_url,
            compute_url=compute_url,
            environment=environment,
        )
        resolved_async_token = _resolve_async_auth(resolved_environment.control, api_key, async_token)

        super().__init__(
            environment=resolved_environment,
            headers=headers,
            async_token=resolved_async_token,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
            logging=logging,
        )
