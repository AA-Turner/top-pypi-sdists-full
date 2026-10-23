"""Anthropic wire transport used by the scoped token-broker relay.

The broker verifies scoped grants and rewrites the approved model before it
gets here.  Keeping the provider request in this package prevents service
features from creating independent Anthropic transport boundaries.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

import httpx

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
COUNT_TOKENS_URL = "https://api.anthropic.com/v1/messages/count_tokens"
#: The Admin API root — organization usage and cost REPORTS, never a model call.
#: It lives here for the same reason the two above do: a provider endpoint
#: spelled at a call site is an independent transport boundary, and the
#: mandate/provider scan has to read it as a bypass because from the outside it
#: is indistinguishable from one. Named separately so a reader can see at a
#: glance that reaching it spends nothing.
ADMIN_API_BASE_URL = "https://api.anthropic.com"
#: The Messages API version header every one of these endpoints expects.
ANTHROPIC_API_VERSION = "2023-06-01"


#: The relay names the OPERATION; the endpoint stays inside the provider layer
#: (the funnel). A caller never reads a URL constant (no-exemptions, 2026-10-22).
BrokerEndpoint = Literal["messages", "count_tokens"]
_BROKER_ENDPOINTS: dict[str, str] = {"messages": MESSAGES_URL, "count_tokens": COUNT_TOKENS_URL}


async def open_broker_stream(
    *,
    endpoint: BrokerEndpoint,
    body: dict[str, Any],
    headers: Mapping[str, str],
    request_timeout: httpx.Timeout,
) -> tuple[httpx.AsyncClient, httpx.Response]:
    """Open an unbuffered Anthropic response and return its owned client.

    The caller must close both values after it has relayed or read the body.
    On setup failure this function closes the client before propagating the
    provider transport error.
    """
    client = httpx.AsyncClient(timeout=request_timeout)
    try:
        upstream_request = client.build_request(
            "POST", _BROKER_ENDPOINTS[endpoint], json=body, headers=headers
        )
        return client, await client.send(upstream_request, stream=True)
    except httpx.HTTPError:
        await client.aclose()
        raise
