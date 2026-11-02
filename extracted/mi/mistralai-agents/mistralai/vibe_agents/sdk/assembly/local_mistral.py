"""Build the Mistral client a process-local Session uses with the caller's own API key."""

import os
from dataclasses import dataclass

from mistralai.client import Mistral
from mistralai.client import httpclient as mistral_httpclient
from mistralai.client.httpclient import AsyncHttpClient
from mistralai.vibe_agents.sdk.app.config import mistral_api_url


@dataclass(frozen=True, slots=True)
class LocalMistralClient:
    """A Mistral client, the HTTP client its owner must close, and the key both authenticate with."""

    client: Mistral
    http: AsyncHttpClient
    api_key: str


def local_mistral_client(feature: str) -> LocalMistralClient:
    """Build a client for ``feature`` from the local process credentials.

    Supplying the HTTP client keeps Mistral's weakref.finalize from closing it a second time at
    garbage-collection time, which warns when no event loop is left to run that close.
    follow_redirects matches the client Mistral builds when none is supplied. The client comes from
    the HTTP library the SDK itself imports (httpx for mistralai 2.x, httpx2 for 3.x), so the SDK's
    error handling and retries recognise its exceptions.
    """

    api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRAL_CLIENT_API_KEY")
    if not api_key:
        raise ValueError(f"{feature} require MISTRAL_API_KEY or MISTRAL_CLIENT_API_KEY")
    http = mistral_httpclient.httpx.AsyncClient(follow_redirects=True)
    return LocalMistralClient(
        client=Mistral(api_key=api_key, server_url=mistral_api_url(), async_client=http),
        http=http,
        api_key=api_key,
    )


__all__ = ["LocalMistralClient", "local_mistral_client"]
