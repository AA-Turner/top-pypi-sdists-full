"""Shared settle-time citation emission — ONE helper for every provider.

Providers that only learn their citations at stream settle (Google grounding
metadata, xAI's response-level URL list, OpenAI-compatible endpoints that
return a terminal ``citations``/``annotations`` payload) all emit the typed
``citation`` stream event the same way: one ``CitationPayload`` per normalized
citation already attached to the response's text blocks by the translator.

Anthropic and OpenAI (Responses API) additionally emit LIVE per-delta events
inside their stream loops — that path stays provider-specific; this helper is
the canonical settle-time emitter so the pattern is never re-implemented.
"""

from __future__ import annotations

import asyncio

from matrx_utils import vcprint

from matrx_ai.config import TextContent, UnifiedResponse
from matrx_ai.context.emitter_protocol import Emitter


async def emit_citations_from_response(
    response: UnifiedResponse | None,
    emitter: Emitter | None,
    provider_label: str,
) -> None:
    """Emit one typed ``citation`` event per normalized citation on the response.

    Reads ``TextContent.metadata["citations"]`` (the canonical cross-provider
    home the translators populate) and sends ``CitationPayload{block_index:
    None, citation}`` for each. Every send is individually guarded: a malformed
    citation logs red and is skipped — it must NEVER abort the answer
    (persistence already carries the citation; the live event is best-effort).
    """
    from matrx_connect.context.events import CitationPayload

    if not emitter or not response or not response.messages:
        return
    for msg in response.messages:
        for content_item in msg.content or []:
            if not isinstance(content_item, TextContent):
                continue
            for citation in content_item.metadata.get("citations") or []:
                if isinstance(citation, dict):
                    try:
                        await emitter.send_citation(
                            CitationPayload(block_index=None, citation=citation)
                        )
                    except Exception as citation_exc:
                        vcprint(
                            f"[{provider_label} CITATIONS] Failed to emit a "
                            f"settle-time citation — skipping this citation only "
                            f"(answer unaffected): {citation_exc}",
                            color="red",
                        )
                    await asyncio.sleep(0)
