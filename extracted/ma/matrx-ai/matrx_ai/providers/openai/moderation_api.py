"""OpenAI Moderation: a safety verdict for text — flagged, and every category with its score.

The api row ``openai_moderation`` (migration 1615) routes here. The endpoint is free and returns no usage, so the
adapter records a zero-token usage on the zero-priced, token-billed offering (an honest $0, never an unknown cost).

The verdict rides the assistant message twice: as ``metadata["moderation"]`` (the typed shape a workflow step reads)
and as JSON text (what any chat-shaped reader sees).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.config import TextContent, TokenUsage, UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import FinishReason

from .client import get_openai_client

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile


def moderation_input_text(config: UnifiedConfig) -> str:
    """Every text part of the last user message, joined: the content to check."""
    for msg in reversed(getattr(config, "messages", None) or []):
        if str(getattr(msg, "role", "")).lower() != "user":
            continue
        parts = [getattr(c, "text", None) for c in (getattr(msg, "content", None) or [])]
        text = "\n".join(p for p in parts if isinstance(p, str) and p.strip()).strip()
        if text:
            return text
    raise ValueError("[OpenAI Moderation] the request has no text to check; put it in the user message.")


def _as_dict(obj: Any) -> dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return dict(obj)
    dump = getattr(obj, "model_dump", None)
    return dict(dump(by_alias=True)) if callable(dump) else dict(vars(obj))


def verdict_from_result(result: Any, *, model: str) -> dict[str, Any]:
    """One moderation result as ``{flagged, flagged_categories, categories: [{name, flagged, score}], model}``.

    Categories keep the provider's own names (``harassment/threatening``, ``self-harm/intent``, …), sorted by
    score, highest first."""
    flags = _as_dict(getattr(result, "categories", None) if not isinstance(result, dict) else result.get("categories"))
    scores = _as_dict(
        getattr(result, "category_scores", None) if not isinstance(result, dict) else result.get("category_scores")
    )
    names = [n for n in dict.fromkeys([*scores, *flags]) if flags.get(n) is not None or scores.get(n) is not None]
    categories = sorted(
        ({"name": n, "flagged": bool(flags.get(n)), "score": float(scores.get(n) or 0.0)} for n in names),
        key=lambda c: c["score"],
        reverse=True,
    )
    flagged = bool(getattr(result, "flagged", None) if not isinstance(result, dict) else result.get("flagged"))
    return {
        "flagged": flagged,
        "flagged_categories": [c["name"] for c in categories if c["flagged"]],
        "categories": categories,
        "model": model,
    }


class OpenAIModeration:
    endpoint_name: str = "[OPENAI MODERATION]"

    def __init__(self) -> None:
        self.client = get_openai_client()

    async def execute(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile, debug: bool = False) -> UnifiedResponse:
        try:
            return await self._execute_moderation(unified_config, profile)
        except Exception as e:
            if getattr(e, "error_info", None) is not None:
                raise
            from matrx_ai.providers.errors import classify_openai_error

            e.error_info = classify_openai_error(e)
            raise

    async def _execute_moderation(self, unified_config: UnifiedConfig, profile: ResolvedCallProfile) -> UnifiedResponse:
        text = moderation_input_text(unified_config)
        model_id = profile.provider_model_id
        vcprint(f"[OpenAI Moderation] {model_id} {len(text)} chars", color="blue")
        response = await self.client.moderations.create(model=model_id, input=text)
        results = list(getattr(response, "results", None) or [])
        if not results:
            raise ValueError("OpenAI moderation returned no result.")
        verdict = verdict_from_result(results[0], model=str(getattr(response, "model", "") or model_id))
        usage = TokenUsage(
            input_tokens=0,
            output_tokens=0,
            matrx_model_name=unified_config.model,
            provider_model_name=model_id,
            api="openai",
            response_id=str(getattr(response, "id", "") or ""),
            metadata={"billing_kind": "free:moderation", "characters_checked": len(text)},
        )
        return UnifiedResponse(
            messages=[
                UnifiedMessage(
                    role="assistant",
                    content=[TextContent(text=json.dumps(verdict))],
                    metadata={"finish_reason": "stop", "moderation": verdict},
                )
            ],
            usage=usage,
            finish_reason=FinishReason.STOP,
        )
