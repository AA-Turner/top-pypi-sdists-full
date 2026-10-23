"""The Batch lane's LIVE send: one rendered body, sent now on the endpoint its batch line would use.

matrx-batch submits bodies RENDERED UPSTREAM from a resolved Holder (``mandates.batch_lane`` /
``render_agent_provider_request``); it chooses no model and no prompt. When a job routes live (urgency, or a
supervisor escalation) the same body is sent at once. The generative call itself is made HERE, in the provider
layer (the funnel), never inside matrx-batch: the host injects :func:`send_live` as matrx-batch's
``live_sender`` (``aidream/package_integration._configure_matrx_batch``), and matrx-batch hands it the client
it was configured with.

``endpoint`` names the provider operation: ``/v1/responses``, ``/v1/chat/completions`` and ``/v1/embeddings``
(OpenAI), ``messages`` (Anthropic), ``generate_content`` (Gemini). An unknown pair is refused in words.
"""

from __future__ import annotations

from typing import Any

LIVE_ENDPOINTS: dict[str, tuple[str, ...]] = {
    "openai": ("/v1/responses", "/v1/chat/completions", "/v1/embeddings"),
    "anthropic": ("messages",),
    "gemini": ("generate_content",),
}


async def send_live(provider: str, endpoint: str, payload: dict[str, Any], *, client: Any) -> Any:
    """Send one rendered batch body live and return the provider's response object."""
    if provider == "openai":
        if endpoint == "/v1/responses":
            return await client.responses.create(**payload)
        if endpoint == "/v1/chat/completions":
            return await client.chat.completions.create(**payload)
        if endpoint == "/v1/embeddings":
            return await client.embeddings.create(**payload)
    elif provider == "anthropic" and endpoint == "messages":
        return await client.messages.create(**payload)
    elif provider == "gemini" and endpoint == "generate_content":
        return await client.aio.models.generate_content(
            model=str(payload.get("model") or ""),
            contents=payload.get("contents"),
            config=payload.get("config"),
        )
    raise ValueError(
        f"batch live send: no {provider!r} endpoint {endpoint!r} (known: {LIVE_ENDPOINTS.get(provider, ())})"
    )
