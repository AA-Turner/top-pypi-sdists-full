"""Information-extraction primitive — the non-chat sibling of UnifiedAIClient.

GLiNER2-style models are not chat models: they take ``(text, labels)`` and return
typed character-offset spans, so they don't go through UnifiedConfig/messages.
``extract_spans`` resolves an extraction model from the registry (so capabilities /
pricing / model selection are configured exactly like chat models) and dispatches
to the matching extraction provider.
"""

from __future__ import annotations

import httpx

from matrx_ai.providers.fastino import (
    ExtractedSpan,
    FastinoExtraction,
    SpanExtractionResult,
)

__all__ = ["ExtractedSpan", "SpanExtractionResult", "extract_spans"]


async def extract_spans(
    model_id_or_name: str,
    text: str,
    labels: list[str],
    *,
    threshold: float = 0.3,
    client: httpx.AsyncClient | None = None,
) -> SpanExtractionResult:
    """Resolve an extraction model from the registry and run span extraction."""
    # Lazy import — keeps this module import-safe in an unconfigured environment
    # (resolution touches the host-injected ORM at call time).
    from matrx_ai.catalog.resolve import resolve_call_profile

    profile = await resolve_call_profile(model_id_or_name)

    interaction = profile.capabilities.interaction
    if interaction != "extraction":
        raise ValueError(
            f"Model {profile.model_name!r} declares "
            f"capabilities.interaction={interaction!r}, not 'extraction'. extract_spans() is "
            "only for information-extraction models; chat models go through the UnifiedAIClient."
        )

    # Single extraction provider today (Fastino). When a second one lands, branch
    # on profile.wire_format here exactly like UnifiedAIClient.execute.
    # The hosted model id is DB data — ai.offering.provider_model_id (backfilled
    # with the full "fastino/..." ids in ai_036; the dropped model_class column
    # used to carry them).
    extractor = FastinoExtraction(client=client)
    return await extractor.extract(
        text,
        labels,
        threshold=threshold,
        model_class=profile.provider_model_id,
    )
