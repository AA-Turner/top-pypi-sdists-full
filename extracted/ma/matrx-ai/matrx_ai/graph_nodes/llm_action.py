"""``ai.llm.chat`` — single-shot LLM call, no agent loop.

Convenience wrapper over ``execute_ai_request`` for the most common case:
one prompt, one response, no tools. The output still comes through
``AiExecutionResult`` so downstream nodes have a stable shape, but this
action caps iterations at 1 and omits tools by default.

Use this for node config like "summarize this text", "extract a headline",
"classify sentiment". For anything that might need tool calls or a full
agent persona, reach for ``ai.agent.start``.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.shared import (
    AiExecutionResult,
    normalize_completed_result,
)


def _build_response_format(output_schema: dict[str, JsonValue]) -> dict[str, Any]:
    """Turn an author-supplied JSON Schema into a strict json_schema
    response_format (F09), reusing matrx-ai's portability gate + wire model —
    never re-deriving the translation ai.extract / the kind binder already own.

    An empty ``{}`` schema means "any object" and cannot be made strict; a
    schema the gate can't make provider-portable is unenforceable. Both FAIL
    the node loudly: a response_format that silently degrades to prose is worse
    than no binding (mirrors ``response_format_for_kind``'s posture).
    """
    from matrx_graph.errors import ExecutionError

    from matrx_ai.config.response_format import OutputSchemaEnvelope, ResponseFormatJsonSchema
    from matrx_ai.schema.lint import lint_output_schema

    if not output_schema:
        raise ExecutionError(
            "ai.llm.chat: output_schema is empty ({}). A strict response_format "
            "needs a concrete object schema (properties/type). Remove output_schema "
            "for free-text output, or provide a real JSON Schema."
        )

    report = lint_output_schema(output_schema)
    schema = report.portable_schema
    if schema is None and report.ok:
        schema = output_schema
    if schema is None:
        errors = "; ".join(f"{f.provider} {f.path}: {f.message}" for f in report.errors)
        raise ExecutionError(
            "ai.llm.chat: output_schema cannot be made provider-portable, so it "
            f"cannot be enforced as a strict response_format. Fix the schema. {errors}"
        )

    return ResponseFormatJsonSchema(
        type="json_schema",
        json_schema=OutputSchemaEnvelope.model_validate(
            {"name": "llm_chat_output", "schema": schema, "strict": True}
        ),
    ).model_dump(mode="json", by_alias=True, exclude_none=True)


class LlmChatInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description="Model identifier. Resolved by matrx-ai's UnifiedAIClient.",
        json_schema_extra=field_extras(widget="model_picker"),
    )
    prompt: str = Field(
        min_length=1,
        description="The user prompt. Sent as a single user message.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=5),
    )
    system_instruction: str | None = Field(
        default=None,
        description="Optional system prompt.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    temperature: float | None = Field(
        default=None, ge=0.0, le=2.0, json_schema_extra=field_extras(widget="slider")
    )
    max_tokens: int | None = Field(default=None, ge=1)
    # Author-supplied JSON Schema — arbitrary JSON by definition.
    output_schema: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Optional JSON Schema. When set, the model is forced to return "
            "strict JSON matching it via the provider's native structured-output "
            "path (F09) — the same mechanism ai.extract uses. Leave null for free "
            "text. The schema is run through matrx-ai's provider-portability gate; "
            "an unenforceable schema fails the node loudly (a silent degrade to "
            "prose is worse than no binding)."
        ),
        json_schema_extra=field_extras(widget="code"),
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


@register_node(
    name="ai.llm.chat",
    display_name="Ask AI",
    description="Send a prompt to an AI model and get a text reply.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=LlmChatInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    icon="sparkles",
    tags=("ai", "llm"),
)
async def llm_chat(
    ctx: NodeExecutionContext, inputs: LlmChatInput
) -> NodeResult[AiExecutionResult]:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.orchestrator.executor import execute_ai_request

    overrides: dict[str, Any] = {}
    if inputs.temperature is not None:
        overrides["temperature"] = inputs.temperature
    if inputs.max_tokens is not None:
        overrides["max_tokens"] = inputs.max_tokens

    if inputs.output_schema is not None:
        overrides["response_format"] = _build_response_format(inputs.output_schema)

    config = UnifiedConfig.from_dict(
        {
            "model": inputs.model,
            "messages": [{"role": "user", "content": inputs.prompt}],
            "system_instruction": inputs.system_instruction,
            **overrides,
        }
    )

    _ = ctx  # scheduler has already set AppContext on the ContextVar
    completed = await execute_ai_request(
        config,
        max_iterations=1,
        max_retries_per_iteration=2,
        metadata=inputs.metadata or None,
    )
    # Node Result System: a failed turn becomes a structured Failure
    # (code='ai_turn_failed', billed usage in details) instead of a raise.
    return normalize_completed_result(completed)
