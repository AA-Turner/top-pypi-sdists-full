"""``ai.moderate`` — check text for harmful content; a typed verdict a branch can route on.

The thin node over OpenAI Moderation (api ``openai_moderation``, free). The verdict is the
provider's own: ``flagged``, the categories it flagged, and every category with its score
(highest first). A Branch step routes on ``result.flagged`` or ``result.flagged_categories``.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.class_pin import model_class_extras, offering_id_field
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.graph_nodes.shared import AiUsage, _extract_usage, failed_turn_failure


class ModerateInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str = Field(
        min_length=1,
        description="The text to check.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    model: str = Field(
        default="omni-moderation-latest",
        min_length=1,
        description="Moderation model id, e.g. 'omni-moderation-latest'.",
        json_schema_extra=field_extras(widget="model_picker", **model_class_extras()),
    )
    offering_id: str | None = offering_id_field()
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ModerationCategory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="The provider's category name, e.g. 'harassment' or 'self-harm/intent'.")
    flagged: bool
    score: float = Field(description="How strongly the text fits the category, 0 to 1.")


class ModerateOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    flagged: bool = Field(description="True when the text breaks any category.")
    flagged_categories: list[str] = Field(default_factory=list, description="The categories it breaks.")
    categories: list[ModerationCategory] = Field(default_factory=list, description="Every category, highest score first.")
    top_category: str | None = Field(default=None, description="The highest-scoring category.")
    top_score: float = 0.0
    model: str
    usage: AiUsage = Field(default_factory=AiUsage)


def verdict_from_response(response: Any) -> dict[str, Any] | None:
    """The verdict the moderation client put on the assistant message (metadata first, else its JSON text)."""
    for msg in reversed(getattr(response, "messages", None) or []):
        meta = getattr(msg, "metadata", None) or {}
        if isinstance(meta, dict) and isinstance(meta.get("moderation"), dict):
            return meta["moderation"]
        for part in getattr(msg, "content", None) or []:
            text = getattr(part, "text", None)
            if isinstance(text, str) and text.strip().startswith("{"):
                try:
                    data = json.loads(text)
                except ValueError:
                    continue
                if isinstance(data, dict) and "flagged" in data:
                    return data
    return None


@register_node(
    name="ai.moderate",
    display_name="Check Content Safety",
    description="Check text for harmful content and say which kinds, with a score for each.",
    category=NodeCategory.LLM,
    determinism=ActionTier.IDEMPOTENT,
    input_schema=ModerateInput,
    output_schema=ModerateOutput,
    icon="shield-check",
    tags=("ai", "moderation", "safety", "classification"),
)
async def ai_moderate(ctx: NodeExecutionContext, inputs: ModerateInput) -> NodeResult[ModerateOutput]:
    _ = ctx
    try:
        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        held = await hold_step(
            {
                "model": inputs.model,
                "offering_id": inputs.offering_id,
                "messages": [{"role": "user", "content": inputs.text}],
            },
            spec_type="ai.moderation",
            consumer="ai.moderate",
            metadata=inputs.metadata,
        )
        completed = await execute_ai_request(
            UnifiedConfig.from_dict(held.config),
            max_iterations=1,
            max_retries_per_iteration=2,
            metadata=held.metadata,
            mandate_key=WORKFLOW_STEP_INTELLIGENCE_MANDATE,
        )
        turn_failed = failed_turn_failure(completed, code="moderation_failed", model=inputs.model)
        if turn_failed is not None:
            return turn_failed
        verdict = verdict_from_response(getattr(completed, "final_response", None))
        usage = _extract_usage(getattr(completed, "total_usage", None))
        if verdict is None:
            return failure(
                "moderation_failed",
                f"ai.moderate: model '{inputs.model}' returned no verdict.",
                details={"model": inputs.model, "usage": usage.model_dump(mode="json")},
            )
        categories = [ModerationCategory.model_validate(c) for c in verdict.get("categories") or []]
        categories.sort(key=lambda c: c.score, reverse=True)
        return success(
            ModerateOutput(
                flagged=bool(verdict.get("flagged")),
                flagged_categories=[c.name for c in categories if c.flagged],
                categories=categories,
                top_category=categories[0].name if categories else None,
                top_score=categories[0].score if categories else 0.0,
                model=str(verdict.get("model") or inputs.model),
                usage=usage,
            )
        )
    except Exception as e:
        return failure("moderation_failed", f"{type(e).__name__}: {e}", details={"model": inputs.model})
