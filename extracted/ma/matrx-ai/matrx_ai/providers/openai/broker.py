"""OpenAI wire transport used by the scoped token-broker relay.

Same reason the Anthropic sibling exists: a provider endpoint spelled at a
service call site is an independent transport boundary, and the
mandate/provider scan cannot tell one from a bypass. The broker verifies the
scoped grant and rewrites the approved model before anything gets here.

``RESPONSES_URL`` is the endpoint the Codex CLI speaks when it is pointed at a
custom ``model_providers.<id>`` with ``wire_api = "responses"`` — it POSTs
``{base_url}/responses`` with ``accept: text/event-stream``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

RESPONSES_URL = "https://api.openai.com/v1/responses"


async def open_broker_stream(
    *,
    upstream_url: str,
    body: dict[str, Any],
    headers: Mapping[str, str],
    request_timeout: httpx.Timeout,
) -> tuple[httpx.AsyncClient, httpx.Response]:
    """Open an unbuffered OpenAI response and return its owned client.

    The caller must close both values after it has relayed or read the body.
    On setup failure this function closes the client before propagating the
    provider transport error.
    """
    client = httpx.AsyncClient(timeout=request_timeout)
    try:
        upstream_request = client.build_request("POST", upstream_url, json=body, headers=headers)
        return client, await client.send(upstream_request, stream=True)
    except httpx.HTTPError:
        await client.aclose()
        raise
