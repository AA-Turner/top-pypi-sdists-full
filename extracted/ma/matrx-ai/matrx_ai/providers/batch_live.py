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

from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from anthropic import AsyncAnthropic
    from google import genai
    from openai import AsyncOpenAI

LIVE_ENDPOINTS: dict[str, tuple[str, ...]] = {
    "openai": ("/v1/responses", "/v1/chat/completions", "/v1/embeddings"),
    "anthropic": ("messages",),
    "gemini": ("generate_content",),
}


async def send_live(
    provider: str,
    endpoint: str,
    payload: dict[str, Any],
    *,
    client: AsyncOpenAI | AsyncAnthropic | genai.Client,
) -> Any:
    """Send one rendered batch body live and return the provider's response object.

    THE PER-CALL SPEND CAP: this lane sends straight to the vendor SDK, beside the unified client's
    dispatch seam, so it asks the cap itself. A body carries no ``UnifiedConfig`` to price, so under an
    open cap it is refused unpriced (``admit_call_spend_cap`` fails closed) — nothing is sent.
    """
    from matrx_ai.providers.guardrail_gate import admit_call_spend_cap

    admit_call_spend_cap(None, None)
    if provider == "openai":
        openai_client = cast("AsyncOpenAI", client)
        if endpoint == "/v1/responses":
            return await openai_client.responses.create(**payload)
        if endpoint == "/v1/chat/completions":
            return await openai_client.chat.completions.create(**payload)
        if endpoint == "/v1/embeddings":
            return await openai_client.embeddings.create(**payload)
    elif provider == "anthropic" and endpoint == "messages":
        return await cast("AsyncAnthropic", client).messages.create(**payload)
    elif provider == "gemini" and endpoint == "generate_content":
        return await cast("genai.Client", client).aio.models.generate_content(
            model=str(payload.get("model") or ""),
            contents=payload.get("contents"),
            config=payload.get("config"),
        )
    raise ValueError(
        f"batch live send: no {provider!r} endpoint {endpoint!r} (known: {LIVE_ENDPOINTS.get(provider, ())})"
    )
