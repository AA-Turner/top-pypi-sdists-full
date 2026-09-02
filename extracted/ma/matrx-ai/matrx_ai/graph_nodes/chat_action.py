"""``ai.chat.manual`` — compose a prompt on the fly and execute it.

This is the low-level, non-agentic entry point: caller supplies the model,
the full message list, and any tools / system instruction directly. No
agent definition is loaded; the request is treated as an ephemeral turn.

Most workflows should prefer ``ai.agent.start`` (use a saved agent) or
``ai.conversation.continue`` (continue an existing thread). Reach for
``chat.manual`` when you need full control of the config — sweeping model
comparisons, one-off prompts, or system-prompt-authored-by-upstream-node
patterns.
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
    AiMessage,
    normalize_completed_result,
)


class ChatManualInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description="Model identifier (e.g. 'claude-opus-4-7', 'gpt-5'). Resolved by matrx-ai's UnifiedAIClient.",
        json_schema_extra=field_extras(widget="model_picker"),
    )
    messages: list[AiMessage] = Field(
        default_factory=list,
        description="Full conversation to send. Use `system_instruction` for the system prompt instead of a role='system' message.",
    )
    system_instruction: str | None = Field(
        default=None,
        description="System prompt. Overrides any existing system message.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    user_input: str | None = Field(
        default=None,
        description="Convenience — if messages is empty, append a single user message with this text.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    tools: list[str] = Field(
        default_factory=list,
        description="Tool names to enable on this call (looked up in ToolRegistry).",
        json_schema_extra=field_extras(widget="tool_picker"),
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        json_schema_extra=field_extras(widget="slider"),
    )
    top_p: float | None = Field(
        default=None, ge=0.0, le=1.0, json_schema_extra=field_extras(widget="slider")
    )
    max_tokens: int | None = Field(default=None, ge=1)
    max_iterations: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Hard cap on agent-loop iterations (tool-call rounds).",
    )
    max_retries_per_iteration: int = Field(default=2, ge=0, le=10)
    variables: dict[str, JsonValue] = Field(default_factory=dict)
    conversation_id: str | None = Field(
        default=None,
        description="Optional — attach this call to an existing conversation.",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


@register_node(
    name="ai.chat.manual",
    display_name="Custom AI Call",
    description="Send your own messages and settings directly to an AI model.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ChatManualInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    icon="message-square",
    tags=("ai", "chat", "llm"),
)
async def chat_manual(
    ctx: NodeExecutionContext, inputs: ChatManualInput
) -> NodeResult[AiExecutionResult]:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_connect.context.app_context import set_app_context

    # The AppContext on the scheduler's forked step is what matrx-ai reads
    # via get_app_context(). If the caller supplied a conversation_id, push
    # it onto that context so execute_ai_request picks it up.  The scheduler
    # forks a fresh AppContext for each parallel invocation, so it is safe
    # to install a derived ctx here without bleeding into siblings.
    if inputs.conversation_id:
        ctx.app = ctx.app.with_overrides(conversation_id=inputs.conversation_id)
        set_app_context(ctx.app)

    messages: list[dict[str, Any]] = [m.model_dump(mode="json") for m in inputs.messages]
    if not messages and inputs.user_input:
        messages = [{"role": "user", "content": inputs.user_input}]

    overrides: dict[str, Any] = {}
    if inputs.temperature is not None:
        overrides["temperature"] = inputs.temperature
    if inputs.top_p is not None:
        overrides["top_p"] = inputs.top_p
    if inputs.max_tokens is not None:
        overrides["max_tokens"] = inputs.max_tokens

    config = UnifiedConfig.from_dict(
        {
            "model": inputs.model,
            "messages": messages,
            "system_instruction": inputs.system_instruction,
            "tools": inputs.tools,
            "variables": inputs.variables,
            **overrides,
        }
    )

    completed = await execute_ai_request(
        config,
        max_iterations=inputs.max_iterations,
        max_retries_per_iteration=inputs.max_retries_per_iteration,
        metadata=inputs.metadata or None,
    )
    # Node Result System: a failed turn becomes a structured Failure
    # (code='ai_turn_failed', billed usage in details) instead of a raise.
    return normalize_completed_result(completed)
