"""Inline agent-loop actions: ``ai.agent.tool_calling`` and ``ai.agent.react``.

Two first-class agent node types for workflow authors. They differ in how
the agent reasons about tools — the choice is visible in the graph, not
hidden inside an orchestrator that "decides for you."

- **``ai.agent.tool_calling``** — autonomous loop using the provider's
  native tool-use API. The model decides when to call tools; we just
  iterate until it stops. Use this when you want the model to act, not
  to narrate. Output: standard :class:`AiExecutionResult`.

- **``ai.agent.react``** — same execution path, but the system prompt
  forces a stepwise *Thought → Action → Observation* cadence and the
  output adds a structured :class:`ReActTrace` derived from the
  conversation history. Use this when the *reasoning* is part of what
  you want to consume downstream (audit logs, transparency, debug).

These are distinct from:

- ``ai.agent.start`` — runs a *saved* agent (loaded from DB, full host
  machinery). Use that when the agent is configured in the agent admin.
- ``ai.chat.manual`` — single-call low-level chat. No agent framing.
- ``ai.llm.chat`` — single-shot, no tools, max_iterations=1.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import Failure, NodeResult, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.shared import (
    AiExecutionResult,
    AiMessage,
    normalize_completed_result,
)

# ============================================================================
# SHARED INPUT SCHEMA
# ============================================================================


class AgentLoopInput(BaseModel):
    """Common input for inline agent-loop actions."""

    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description="Model identifier. Resolved by matrx-ai's UnifiedAIClient.",
        json_schema_extra=field_extras(widget="model_picker"),
    )
    user_input: str = Field(
        min_length=1,
        description="The query or task the agent should work on.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=4),
    )
    system_instruction: str | None = Field(
        default=None,
        description=(
            "Optional system prompt. For ai.agent.react, the ReAct framing "
            "is appended automatically — your system_instruction is added "
            "as additional context, not replaced."
        ),
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    tools: list[str] = Field(
        default_factory=list,
        description="Tool names from ToolRegistry to enable for this run.",
        json_schema_extra=field_extras(widget="tool_picker"),
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        json_schema_extra=field_extras(widget="slider"),
    )
    max_tokens: int | None = Field(default=None, ge=1)
    max_iterations: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Cap on agent-loop iterations (tool-call rounds).",
    )
    max_retries_per_iteration: int = Field(default=2, ge=0, le=10)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


# ============================================================================
# ai.agent.tool_calling — native tool-use loop
# ============================================================================


@register_node(
    name="ai.agent.tool_calling",
    display_name="Agent with Tools",
    description="Run an AI agent that can use tools to get things done.",
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentLoopInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    icon="bot",
    tags=("ai", "agent", "tool_calling"),
)
async def agent_tool_calling(
    ctx: NodeExecutionContext, inputs: AgentLoopInput
) -> NodeResult[AiExecutionResult]:
    _ = ctx
    config = _build_config(inputs, system_instruction=inputs.system_instruction)
    completed = await _execute(config, inputs)
    # Node Result System: a failed turn becomes a structured Failure
    # (code='ai_turn_failed', billed usage in details) instead of a raise.
    return normalize_completed_result(completed)


# ============================================================================
# ai.agent.react — structured Thought / Action / Observation trace
# ============================================================================

REACT_SYSTEM_FRAMING = """\
You are a ReAct-style reasoning agent.

For every turn that involves a decision, follow this cadence:

  Thought: <your reasoning about what to do next, in 1-3 sentences>
  (then either call a tool, or provide your final answer)

When you call a tool, the user message that follows will contain the
observation. Reason about the observation in your next Thought before
deciding the next step.

When you have enough information to answer the user, write your final
answer as plain text WITHOUT a Thought prefix.

This structure is part of your output contract. Skipping the Thought
prefix when reasoning is the failure mode — be explicit about your
reasoning at every decision point.
"""


class ReActStep(BaseModel):
    """One step of a ReAct trace.

    Each step captures the agent's reasoning ("Thought") followed by
    either a tool invocation ("Action" + "ActionInput") or a final
    answer. Observations from tools are recorded in the *next* step.
    """

    model_config = ConfigDict(extra="forbid")

    iteration: int = Field(ge=0)
    thought: str = Field(default="")
    action: str | None = Field(
        default=None,
        description="Tool name when the agent calls a tool; None for the final answer step.",
    )
    # Model-authored tool arguments — genuinely dynamic JSON.
    action_input: dict[str, JsonValue] = Field(default_factory=dict)
    observation: str = Field(
        default="",
        description="Tool result observed after the action ran. Empty for the final-answer step.",
    )


class AgentReactResult(BaseModel):
    """Output of ``ai.agent.react`` — final answer plus structured trace.

    The trace is derived from the assistant/tool messages produced during
    the run. Downstream nodes can wire to ``react_trace`` for audit views,
    or to ``final_text`` for the answer alone.
    """

    model_config = ConfigDict(extra="forbid")

    final_text: str = ""
    react_trace: list[ReActStep] = Field(default_factory=list)
    iterations: int = 0
    tool_calls_made: int = 0
    underlying: AiExecutionResult


@register_node(
    name="ai.agent.react",
    display_name="Agent with Visible Reasoning",
    description="Run an AI agent that shows its step-by-step reasoning as it works.",
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentLoopInput,
    output_schema=AgentReactResult,
    output_kind="agent_react_result",
    icon="brain",
    tags=("ai", "agent", "react"),
)
async def agent_react(
    ctx: NodeExecutionContext, inputs: AgentLoopInput
) -> NodeResult[AgentReactResult]:
    _ = ctx
    system = REACT_SYSTEM_FRAMING
    if inputs.system_instruction:
        system = f"{system}\n\nAdditional context:\n{inputs.system_instruction}"

    config = _build_config(inputs, system_instruction=system)
    completed = await _execute(config, inputs)
    # Node Result System: a failed turn is a structured Failure carrying the
    # billed usage in details — propagate it unchanged (no trace to build).
    normalized = normalize_completed_result(completed)
    if isinstance(normalized, Failure):
        return normalized
    underlying = normalized.result
    trace = _build_react_trace(underlying.messages)

    return success(
        AgentReactResult(
            final_text=underlying.final_text,
            react_trace=trace,
            iterations=underlying.iterations,
            tool_calls_made=underlying.tool_calls_made,
            underlying=underlying,
        )
    )


# ============================================================================
# SHARED HELPERS
# ============================================================================


def _build_config(inputs: AgentLoopInput, system_instruction: str | None) -> Any:
    from matrx_ai.config import UnifiedConfig

    overrides: dict[str, Any] = {}
    if inputs.temperature is not None:
        overrides["temperature"] = inputs.temperature
    if inputs.max_tokens is not None:
        overrides["max_tokens"] = inputs.max_tokens

    return UnifiedConfig.from_dict(
        {
            "model": inputs.model,
            "messages": [{"role": "user", "content": inputs.user_input}],
            "system_instruction": system_instruction,
            "tools": inputs.tools,
            **overrides,
        }
    )


async def _execute(config: Any, inputs: AgentLoopInput) -> Any:
    from matrx_ai.orchestrator.executor import execute_ai_request

    return await execute_ai_request(
        config,
        max_iterations=inputs.max_iterations,
        max_retries_per_iteration=inputs.max_retries_per_iteration,
        metadata=inputs.metadata or None,
    )


def _build_react_trace(messages: list[AiMessage]) -> list[ReActStep]:
    """Derive a ReAct trace from the conversation history.

    Two-pass: first collect every tool result keyed by tool_call_id, then
    walk assistant messages and pair each tool_call to its observation.
    The two-pass approach is necessary because a tool message follows its
    triggering assistant message in the conversation order, so a single
    forward pass would never see the observation in time.
    """
    pending_tool_results: dict[str, str] = {}
    for msg in messages:
        if msg.role == "tool":
            tcid = msg.tool_call_id or ""
            if tcid:
                pending_tool_results[tcid] = _coerce_text(msg.content)

    trace: list[ReActStep] = []
    iteration = 0

    for msg in messages:
        if msg.role != "assistant":
            continue

        thought = _extract_thought(_coerce_text(msg.content))

        if not msg.tool_calls:
            trace.append(
                ReActStep(
                    iteration=iteration,
                    thought=thought,
                    action=None,
                    action_input={},
                    observation="",
                )
            )
            iteration += 1
            continue

        for call in msg.tool_calls:
            tool_name, tool_args, tool_call_id = _parse_tool_call(call)
            observation = pending_tool_results.get(tool_call_id, "")
            trace.append(
                ReActStep(
                    iteration=iteration,
                    thought=thought,
                    action=tool_name,
                    action_input=tool_args,
                    observation=observation,
                )
            )
            iteration += 1
            thought = ""

    return trace


def _coerce_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for p in content:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict):
                if p.get("type") in ("text", "output_text"):
                    parts.append(str(p.get("text", "")))
                elif "content" in p:
                    parts.append(str(p["content"]))
        return "".join(parts)
    return str(content)


def _extract_thought(text: str) -> str:
    """Pull the Thought prefix when present; otherwise return the raw text."""
    stripped = text.strip()
    lower = stripped.lower()
    if lower.startswith("thought:"):
        return stripped[len("thought:") :].strip()
    return stripped


def _parse_tool_call(call: Any) -> tuple[str, dict[str, JsonValue], str]:
    if isinstance(call, dict):
        name = (
            call.get("name")
            or call.get("tool_name")
            or (call.get("function") or {}).get("name")
            or ""
        )
        args = (
            call.get("input")
            or call.get("arguments")
            or (call.get("function") or {}).get("arguments")
            or {}
        )
        if isinstance(args, str):
            try:
                import json

                args = json.loads(args)
            except (TypeError, ValueError):
                args = {"raw": args}
        if not isinstance(args, dict):
            args = {"raw": args}
        call_id = call.get("id") or call.get("tool_call_id") or ""
        return str(name), args, str(call_id)

    name = getattr(call, "name", None) or getattr(call, "tool_name", None) or ""
    args = getattr(call, "input", None) or getattr(call, "arguments", {}) or {}
    if isinstance(args, str):
        try:
            import json

            args = json.loads(args)
        except (TypeError, ValueError):
            args = {"raw": args}
    if not isinstance(args, dict):
        args = {"raw": args}
    call_id = getattr(call, "id", "") or getattr(call, "tool_call_id", "")
    return str(name), args, str(call_id)
