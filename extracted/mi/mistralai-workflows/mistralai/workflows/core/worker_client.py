from typing import Any

import httpx

from mistralai.workflows.client import _get_async_client
from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
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
    timeout: float = 60.0,
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    token_provider: TokenProvider | None = None,
) -> PrivateWorkerClient:
    resolved_base_url = (base_url or config.worker.server_url).rstrip("/")
    provider = token_provider or get_token_provider(api_key)
    async_client = _get_async_client(
        timeout=timeout, token_provider=provider, headers=headers, server_url=resolved_base_url
    )
    client = PrivateWorkerClient(
        server_url=resolved_base_url,
        client=_NoopSyncClient(),
        async_client=async_client,
        timeout_ms=int(timeout * 1000),
    )
    # The async_client was created specifically for this instance;
    # mark it as not-supplied so the SDK closes it on __aexit__.
    client.sdk_configuration.async_client_supplied = False
    return client
