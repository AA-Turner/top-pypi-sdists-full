import asyncio
import weakref
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any, cast

import httpx

from mistralai.workflows.client import _get_async_client
from mistralai.workflows.core.auth import RunAs, TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.worker_client.httpclient import ClientOwner, close_clients
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient


class _NoopSyncClient:
    """No-op sync HTTP client stub passed to the Speakeasy SDK constructor.

    When ``client=None``, the SDK allocates a real ``httpx.Client`` (opening a
    connection pool) even though we only call async methods.
    Passing this stub avoids that allocation entirely.
    """

    def send(self, request: httpx.Request, **kwargs: Any) -> httpx.Response:
        raise RuntimeError("Synchronous SDK methods are not supported")

    def build_request(self, method: str, url: Any, **kwargs: Any) -> httpx.Request:
        return httpx.Request(method, url)

    def close(self) -> None:
        pass


def get_worker_client(
    base_url: str | None = None,
    timeout: float | None = None,
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    token_provider: TokenProvider | None = None,
) -> PrivateWorkerClient:
    resolved_base_url = (base_url or config.worker.server_url).rstrip("/")
    resolved_timeout = timeout if timeout is not None else config.http.timeout
    provider = token_provider or get_token_provider(api_key)
    # The generated worker client is built on httpx regardless of the installed mistralai major.
    async_client = _get_async_client(
        timeout=resolved_timeout,
        token_provider=provider,
        headers=headers,
        server_url=resolved_base_url,
        run_as=RunAs.DEPLOYMENT,
        _http=httpx,
    )
    client = PrivateWorkerClient(
        server_url=resolved_base_url,
        client=_NoopSyncClient(),
        async_client=async_client,
        timeout_ms=int(resolved_timeout * 1000),
    )
    # The async_client was created specifically for this instance;
    # mark it as not-supplied so the SDK closes it on __aexit__.
    client.sdk_configuration.async_client_supplied = False
    # The SDK's own finalizer recorded the client as supplied and never closes it, so a client
    # dropped without `async with` would leave its connections open until the GC reaps the sockets.
    weakref.finalize(
        client, close_clients, cast(ClientOwner, client.sdk_configuration), None, True, async_client, False
    )
    return client


# The running worker's long-lived client, with the event loop that owns its connections.
_shared_worker_client: tuple[PrivateWorkerClient, asyncio.AbstractEventLoop] | None = None


@asynccontextmanager
async def share_worker_client(client: PrivateWorkerClient) -> AsyncIterator[None]:
    """Let internal activities reuse the worker's client while the worker runs."""
    global _shared_worker_client
    _shared_worker_client = (client, asyncio.get_running_loop())
    try:
        yield
    finally:
        _shared_worker_client = None


def _get_shared_worker_client() -> PrivateWorkerClient | None:
    if _shared_worker_client is None:
        return None
    client, loop = _shared_worker_client
    # httpx connections are bound to their event loop; a sync activity running its
    # own loop in a thread must not borrow them.
    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        return None
    return client if running_loop is loop else None


@asynccontextmanager
async def borrow_worker_client(fallback: Callable[[], PrivateWorkerClient]) -> AsyncIterator[PrivateWorkerClient]:
    """Yield the running worker's shared client, or a client from `fallback` closed on exit."""
    shared = _get_shared_worker_client()
    if shared is not None:
        yield shared
        return
    async with fallback() as client:
        yield client
