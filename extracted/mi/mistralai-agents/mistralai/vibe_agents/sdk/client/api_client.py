"""``agents.Client``: an API key and the URLs of the Agents control plane, with one connection pool
for the calls made through it, as ``mistralai.Mistral`` is for the Mistral API."""

from __future__ import annotations

import asyncio
import dataclasses
import threading
from collections.abc import AsyncIterator
from types import TracebackType
from typing import Self
from uuid import UUID

import httpx

from mistralai.vibe_agents._http import _client_headers, _mistral_api_transport
from mistralai.vibe_agents.sdk.authoring import errors as sdk_errors
from mistralai.vibe_agents.sdk.client import listing
from mistralai.vibe_agents.sdk.client.records import SessionInfo
from mistralai.vibe_agents.sdk.transport import remote as remote_transport

__all__ = ["Client"]

# The timeout of the control plane's own HTTP clients.
_TIMEOUT_SECONDS = 30.0


class Client:
    """The Agents control plane for one API key. Every call is async.

    ``api_key`` defaults to ``MISTRAL_API_KEY``; with no key from either, ``Client()`` raises
    ``SdkError``.
    ``server_url`` is the Mistral API root: ``MISTRAL_API_URL``, else ``https://api.mistral.ai``.
    ``agents_url`` is the Agents control plane: ``AGENTS_SDK_DEPLOY_CONTROL_PLANE_URL`` when
    ``server_url`` is not given, else ``server_url`` + ``/v2/agents``, so one URL is enough for
    another cloud.

    ``async_client`` is your own ``httpx.AsyncClient`` for the requests, as in ``mistralai.Mistral``;
    its timeouts and connection limits apply, and the client never closes it. Without it, the client
    opens its own connection pool at its first call, and ``await client.aclose()`` or the end of
    ``async with agents.Client() as client:`` closes it. Creating a client sends nothing and needs no
    event loop. Its own pool serves one event loop: a call from a later one (a second
    ``asyncio.run``) opens a new pool, and a call while another thread's event loop still uses it
    raises ``SdkError``. ``aclose`` closes the pool of the event loop it runs in, so call it in the
    loop that used the client last. An ``async_client`` also serves one event loop. Agents loaded
    with ``Agent.load_from(client=client)`` and their sessions send their requests through the
    client; once it is closed, they raise ``SdkError``.
    """

    __slots__ = (
        "_async_client",
        "_closed",
        "_deployment",
        "_lock",
        "_own_http",
        "_own_loop",
        "_pooled",
        "_server_url",
    )

    def __init__(
        self,
        *,
        api_key: str | None = None,
        server_url: str | None = None,
        agents_url: str | None = None,
        async_client: httpx.AsyncClient | None = None,
    ) -> None:
        if async_client is not None and not isinstance(async_client, httpx.AsyncClient):
            raise sdk_errors.SdkError(
                f"async_client must be an httpx.AsyncClient or None, got {type(async_client).__name__}"
            )
        self._server_url, control_plane_url = remote_transport._client_urls(server_url, agents_url)
        self._deployment = remote_transport.RemoteAgentDeployment(
            server_url=control_plane_url, api_key=remote_transport._client_api_key(api_key), pool=self._pool
        )
        self._async_client = async_client
        self._own_http: httpx.AsyncClient | None = None
        self._pooled = True
        # The event loop the own pool's connections belong to, once a call made in one opened it.
        self._own_loop: asyncio.AbstractEventLoop | None = None
        # Threads that call at once see the pool and its loop change together.
        self._lock = threading.Lock()
        self._closed = False

    @classmethod
    def _per_call(
        cls, *, api_key: str | None = None, server_url: str | None = None, agents_url: str | None = None
    ) -> Client:
        """A client without a shared connection pool, so it needs no close.

        The client of ``agents.list_sessions()`` and of ``Agent.load_from`` / ``Agent.load_session``
        without ``client=``. Each listing page, and each session, opens a pool of its own and closes
        it when it ends.
        """
        client = cls(api_key=api_key, server_url=server_url, agents_url=agents_url)
        client._pooled = False
        return client

    @property
    def server_url(self) -> str:
        """The Mistral API root."""
        return self._server_url

    @property
    def agents_url(self) -> str:
        """The Agents control plane URL."""
        return self._deployment.server_url

    def list_sessions(
        self,
        *,
        scope: listing.SessionScope = "roots",
        root: str | None = None,
        parent: str | None = None,
        status: listing.SessionStatus | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[SessionInfo]:
        """Iterate over the deployed sessions of this client's API key, newest first.

        The keywords are those of ``agents.list_sessions``. Pages are read through this client's
        connection pool as you iterate.
        """
        self._check_open()
        return listing._deployed_sessions(
            self._deployment, scope=scope, root=root, parent=parent, status=status, limit=limit
        )

    def _agent_deployment(
        self, *, agent_deployment_id: UUID | None = None, agent_deployment_name: str | None = None
    ) -> remote_transport.RemoteAgentDeployment:
        """The routing of an agent's handle on this client's control plane, sending through it."""
        return dataclasses.replace(
            self._deployment, agent_deployment_id=agent_deployment_id, agent_deployment_name=agent_deployment_name
        )

    def _check_open(self) -> None:
        if self._closed:
            raise sdk_errors.SdkError("This agents.Client is closed: create a new one")

    def _pool(self) -> httpx.AsyncClient | None:
        """The connection pool for a request, or ``None`` for a connection of the request's own."""
        self._check_open()
        if self._async_client is not None:
            return self._async_client
        if not self._pooled:
            return None
        loop = _running_loop()
        with self._lock:
            # Again under the lock: an aclose() in another thread may have closed the client since.
            self._check_open()
            own_loop = self._own_loop
            if self._own_http is not None and loop is not None and own_loop is not None and own_loop is not loop:
                if own_loop.is_running():
                    raise sdk_errors.SdkError(
                        "This agents.Client's connection pool serves another thread's running event loop: "
                        "create one client per event loop"
                    )
                # The pool's connections belong to a stopped event loop (an earlier asyncio.run): open a new one.
                self._own_http = None
            if self._own_http is None:
                self._own_http = httpx.AsyncClient(
                    headers=_client_headers(),
                    timeout=httpx.Timeout(_TIMEOUT_SECONDS),
                    # No cap on open connections: each session's event stream holds one while it waits, and
                    # sessions used to have a pool each. The limits go on the transport: httpx ignores the
                    # client's limits= when it is given a transport.
                    transport=_mistral_api_transport(
                        limits=httpx.Limits(max_connections=None, max_keepalive_connections=20),
                    ),
                )
            if loop is not None:
                self._own_loop = loop
            return self._own_http

    async def aclose(self) -> None:
        """Close the client's own connection pool. A given ``async_client`` stays open."""
        with self._lock:
            self._closed = True
            pool, pool_loop = self._own_http, self._own_loop
            self._own_http = None
        # A pool that another event loop uses (a stopped one, or one in another thread) cannot be closed from
        # this one.
        if pool is not None and pool_loop in (None, _running_loop()):
            await pool.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: dict[int, object]) -> Self:
        # A client is shared, not copied: a deep copy of an agent loaded with it keeps it.
        return self

    def __repr__(self) -> str:
        return f"Client(server_url={self.server_url!r}, agents_url={self.agents_url!r})"


def _running_loop() -> asyncio.AbstractEventLoop | None:
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None
