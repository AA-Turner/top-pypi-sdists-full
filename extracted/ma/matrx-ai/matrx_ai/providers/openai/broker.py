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
from typing import Any, Literal

import httpx

RESPONSES_URL = "https://api.openai.com/v1/responses"
#: The OpenAI organization API root -- admin usage and COST REPORTS
#: (``/v1/organization/costs``), never a model call. Same reason as the Anthropic
#: sibling (``ADMIN_API_BASE_URL``): the host is spelled once, here, in the sanctioned
#: provider layer, and a bare origin spends nothing.
ADMIN_API_BASE_URL = "https://api.openai.com"


#: The relay names the OPERATION; the endpoint stays inside the provider layer
#: (the funnel). A caller never reads a URL constant (no-exemptions, 2026-10-22).
BrokerEndpoint = Literal["responses"]
_BROKER_ENDPOINTS: dict[str, str] = {"responses": RESPONSES_URL}


async def open_broker_stream(
    *,
    endpoint: BrokerEndpoint,
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
        upstream_request = client.build_request("POST", _BROKER_ENDPOINTS[endpoint], json=body, headers=headers)
        return client, await client.send(upstream_request, stream=True)
    except httpx.HTTPError:
        await client.aclose()
        raise
