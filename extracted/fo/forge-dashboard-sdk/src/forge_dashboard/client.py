"""The hand-written client wrapper. Everything under
``forge_dashboard._generated`` is produced by openapi-python-client from
``openapi/openapi.yaml`` -- never edit it by hand, regenerate it instead
(see ``hack/fetch-spec.sh`` and ``CONTRIBUTING.md``). This module,
``errors.py`` and ``retry.py`` are the hand-written layer on top of it:
auth injection, retry and typed errors (rules/sdk-generation.md's
"Generated vs hand-written").
"""

from __future__ import annotations

import os

import httpx

from ._generated.api.health import get_version as _get_version
from ._generated.api.health import health as _get_health
from ._generated.client import Client as _GeneratedClient
from ._generated.models.health import Health
from ._generated.models.version import Version
from .errors import decode_error
from .retry import DEFAULT_RETRY_CONFIG, AsyncRetryTransport, RetryConfig, RetryTransport

#: The environment variable :class:`ForgeDashboardClient` falls back to
#: when no token is passed explicitly via ``api_token``. Not a hardcoded
#: credential -- it's the name of the env var to read one from.
API_TOKEN_ENV_VAR = "FORGE_DASHBOARD_API_TOKEN"  # noqa: S105 # nosec B105


class ForgeDashboardClient:
    """A forge-dashboard API client.

    Every operation except :meth:`health`, :meth:`get_version` and the two
    webhook receivers requires an authenticated session. forge-dashboard
    accepts either a browser's passkey session cookie or a personal API
    token (``Authorization: Bearer <token>``, minted via ``POST
    /api/tokens``) -- see the spec's ``auth`` tag. This wrapper only speaks
    the bearer-token half, the headless-friendly one: pass a token as
    *api_token* or set ``FORGE_DASHBOARD_API_TOKEN`` in the environment --
    the constructor argument wins when both are given.

    The underlying generated client is available as :attr:`raw` for any
    operation this wrapper doesn't have a dedicated method for; every
    generated ``forge_dashboard._generated.api.<tag>.<operation>`` module's
    ``sync_detailed``/``asyncio_detailed`` functions take it as their
    ``client`` argument.
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_token: str | None = None,
        retry: RetryConfig = DEFAULT_RETRY_CONFIG,
        httpx_client: httpx.Client | None = None,
        httpx_async_client: httpx.AsyncClient | None = None,
        raise_on_unexpected_status: bool = False,
    ) -> None:
        token = api_token if api_token is not None else os.environ.get(API_TOKEN_ENV_VAR)
        # HTTP header names are case-insensitive (RFC 7230) and httpx
        # normalizes lookups, so a casing mutant on "Authorization" below
        # is behaviorally equivalent -- pragma'd rather than chasing it.
        headers = {"Authorization": f"Bearer {token}"} if token else {}  # pragma: no mutate

        # headers isn't passed here, and base_url is never read back off
        # self._raw afterward either: this Client's own lazy httpx-client
        # construction is never reached -- set_httpx_client/
        # set_async_httpx_client below always override it -- so the base
        # URL and the auth header both have to be applied to whichever
        # client actually sends requests instead (see below). base_url is
        # on its own statement, pragma'd, so mutating that dead value
        # doesn't mask a real mutation of raise_on_unexpected_status on the
        # same line -- that one *is* read, by every generated operation's
        # _parse_response.
        self._raw = _GeneratedClient(base_url=base_url)  # pragma: no mutate - never read back, see comment above
        self._raw.raise_on_unexpected_status = raise_on_unexpected_status

        sync_client = httpx_client
        if sync_client is None:
            sync_client = httpx.Client(base_url=base_url, transport=RetryTransport(retry=retry))
        # Apply the bearer token directly to whichever client will actually
        # send requests -- a caller-supplied httpx_client bypasses the
        # generated Client's own lazy header construction, so the header
        # has to be set here rather than relying on that path.
        sync_client.headers.update(headers)
        self._raw.set_httpx_client(sync_client)

        async_client = httpx_async_client
        if async_client is None:
            async_client = httpx.AsyncClient(base_url=base_url, transport=AsyncRetryTransport(retry=retry))
        async_client.headers.update(headers)
        self._raw.set_async_httpx_client(async_client)

    @property
    def raw(self) -> _GeneratedClient:
        """The underlying generated ``Client``."""
        return self._raw

    def health(self) -> Health:
        """Liveness. Needs no session -- a good first call to prove the
        client reaches the server at all.

        Returns:
            The server's health status.
        """
        response = _get_health.sync_detailed(client=self._raw)
        if error := decode_error(response):
            raise error
        if response.parsed is None:
            # Not an assert -- holds under -O and doesn't trip bandit's
            # B101. health's only documented response is 200 Health, so
            # this only fires if the spec and server ever disagree.
            raise TypeError(f"unexpected health response body: {response.parsed!r}")
        return response.parsed

    async def ahealth(self) -> Health:
        """Async counterpart of :meth:`health`.

        Returns:
            The server's health status.
        """
        response = await _get_health.asyncio_detailed(client=self._raw)
        if error := decode_error(response):
            raise error
        if response.parsed is None:
            raise TypeError(f"unexpected health response body: {response.parsed!r}")
        return response.parsed

    def get_version(self) -> Version:
        """The running server's build version. Needs no session.

        Returns:
            The running server's build version.
        """
        response = _get_version.sync_detailed(client=self._raw)
        if error := decode_error(response):
            raise error
        if response.parsed is None:
            raise TypeError(f"unexpected getVersion response body: {response.parsed!r}")
        return response.parsed

    async def aget_version(self) -> Version:
        """Async counterpart of :meth:`get_version`.

        Returns:
            The running server's build version.
        """
        response = await _get_version.asyncio_detailed(client=self._raw)
        if error := decode_error(response):
            raise error
        if response.parsed is None:
            raise TypeError(f"unexpected getVersion response body: {response.parsed!r}")
        return response.parsed

    def close(self) -> None:
        self._raw.get_httpx_client().close()

    async def aclose(self) -> None:
        await self._raw.get_async_httpx_client().aclose()

    def __enter__(self) -> ForgeDashboardClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        # httpx.BaseTransport's own __exit__ ignores exc_info and just
        # closes -- our RetryTransport doesn't override that -- so there's
        # nothing this needs from *exc_info beyond letting `with` call it.
        self.close()

    async def __aenter__(self) -> ForgeDashboardClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()
