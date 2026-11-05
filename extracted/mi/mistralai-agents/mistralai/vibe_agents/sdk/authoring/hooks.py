"""Protocol-free Hook results and tool call views for authored Hooks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, JsonValue

from mistralai.vibe.harness.app_server.session import ContentBlock
from mistralai.vibe.harness.core import protocol
from mistralai.vibe.harness.runtime.capabilities import (
    PostAgentTurnHookInvocation,
    PostLlmCallHookInvocation,
    PostToolCallHookInvocation,
    PreAgentTurnHookInvocation,
    PreLlmCallHookInvocation,
    PreToolCallHookInvocation,
)
from mistralai.vibe.harness.runtime.content import to_core_content, to_session_content, tool_returned_error
from mistralai.vibe_agents.sdk.authoring.tool_result import ToolResult
from mistralai.vibe_agents.sdk.transport.results import ToolCall

type HookDecisionKind = Literal["skip", "retry", "reject"]


@dataclass(frozen=True, slots=True)
class HookDecision:
    """A Hook's decision, turned into the result of the point that returns it.

    Build it with ``agents.skip``, ``agents.retry`` or ``agents.reject``.
    """

    kind: HookDecisionKind
    message: str


def skip(reason: str) -> HookDecision:
    """Stop the turn, model call or tool call.

    From ``pre_tool_call``, ``reason`` is what the model sees in place of the tool
    result. From ``pre_agent_turn`` or ``pre_llm_call``, the turn ends with
    ``stop_reason="skipped"`` and ``reason`` as its text.
    """

    return HookDecision("skip", reason)


def retry(feedback: str) -> HookDecision:
    """Discard the model's response and call the model again with ``feedback``."""

    return HookDecision("retry", feedback)


def reject(reason: str) -> HookDecision:
    """Reject the model's response and end the turn with ``reason``."""

    return HookDecision("reject", reason)


def _tool_name(call: protocol.ExternalToolCall) -> str:
    return call.tool_name if call.type == "provided" else call.name


def _tool_id(call: protocol.ExternalToolCall) -> str:
    # The ID approvals name the tool by: `<namespace>.<name>` for an authored tool, the
    # built-in's own name otherwise.
    return f"{call.group_name}.{call.tool_name}" if call.type == "provided" else call.name


class _HookView(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    turn_id: str
    """The Turn's ID."""


class PreAgentTurn(_HookView):
    """The Turn a ``pre_agent_turn`` Hook receives."""

    user_content: list[ContentBlock]
    """The user's content for the Turn. Blocks handed back unchanged reach the model as they came."""


class PreLlmCall(_HookView):
    """The model call a ``pre_llm_call`` Hook receives."""


type FinishReason = Literal["stop", "tool_call", "length", "content_filter", "other"]


class _ModelReply(_HookView):
    content: list[ContentBlock]
    """The reply's content blocks, in order, without its reasoning and tool calls."""
    text: str
    """The reply's text blocks joined, ``""`` when it has none."""
    tool_calls: tuple[ToolCall, ...]
    """The tool calls the reply makes. ``name`` is the name the model called, such as ``get_weather``."""
    reasoning: str
    """The reply's reasoning text joined, ``""`` when it has none."""
    finish_reason: FinishReason
    """Why the model stopped."""
    usage: protocol.TokenUsage | None  # public as agents.TokenUsage
    """The tokens the model call used, when the provider reports them."""


class PostLlmCall(_ModelReply):
    """The model reply a ``post_llm_call`` Hook receives."""


class PostAgentTurn(_ModelReply):
    """The final answer of the Turn a ``post_agent_turn`` Hook receives."""


class PreToolCall(_HookView):
    """The tool call a ``pre_tool_call`` Hook receives."""

    tool_name: str
    """The authored tool's name, or the built-in's, such as ``file_system.bash``."""
    tool_id: str
    """The tool's ID: ``<namespace>.<name>``, such as ``billing.charge``, or the built-in's name."""
    tool_call_id: str
    """The call's ID, as ``ToolCallEntry.tool_call_id`` and ``ToolCallbackContext.tool_call_id`` give it."""
    arguments: dict[str, JsonValue]
    """The arguments the model produced."""


class PostToolCall(PreToolCall):
    """The tool call and result a ``post_tool_call`` Hook receives."""

    arguments: dict[str, JsonValue]
    """The arguments the tool ran with, after any ``pre_tool_call`` Hook changed them."""
    tool_result: ToolResult
    """The call's result. Return it, or a copy, in ``hook.PostToolCallHookContinue``: blocks handed
    back unchanged reach the model as they came, and a failed call kept ``is_error=True`` keeps its
    error."""


class PostToolCallHookContinue(BaseModel):
    """Continue with ``tool_result`` as the result the model gets."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["post_tool_call_continue"] = "post_tool_call_continue"
    tool_result: ToolResult


def pre_agent_turn_view(invocation: PreAgentTurnHookInvocation) -> PreAgentTurn:
    return PreAgentTurn.model_construct(
        turn_id=invocation.turn_id, user_content=to_session_content(invocation.user_content, keep_origin=True)
    )


def pre_llm_call_view(invocation: PreLlmCallHookInvocation) -> PreLlmCall:
    return PreLlmCall.model_construct(turn_id=invocation.turn_id)


def model_reply_view[ReplyT: _ModelReply](
    view: type[ReplyT], invocation: PostLlmCallHookInvocation | PostAgentTurnHookInvocation
) -> ReplyT:
    candidate = invocation.candidate
    blocks: list[protocol.ContentBlock] = []
    tool_calls: list[ToolCall] = []
    reasoning: list[str] = []
    for part in candidate.message.content:
        match part:
            case protocol.ReasoningPart():
                reasoning.extend(item.text for item in part.content if isinstance(item, protocol.ReasoningTextContent))
            case protocol.ModelToolCallPart():
                arguments = part.arguments
                value = arguments.value if isinstance(arguments, protocol.JsonToolArguments) else arguments.raw
                tool_calls.append(ToolCall(name=part.name, arguments=value))
            case _:
                blocks.append(part)
    content = to_session_content(blocks, keep_origin=True)
    # mypy's Pydantic plugin types ``model_construct`` on the base class, not on ``view``.
    return cast(
        ReplyT,
        view.model_construct(
            turn_id=invocation.turn_id,
            content=content,
            text="".join(block.text for block in blocks if isinstance(block, protocol.TextContentBlock)),
            tool_calls=tuple(tool_calls),
            reasoning="".join(reasoning),
            finish_reason=candidate.finish_reason,
            usage=candidate.usage,
        ),
    )


def _tool_call_fields(tool_call: protocol.HookToolCall) -> dict[str, Any]:
    return {
        "tool_name": _tool_name(tool_call.call),
        "tool_id": _tool_id(tool_call.call),
        "tool_call_id": tool_call.call_id,
        "arguments": tool_call.call.arguments,
    }


def pre_tool_call_view(invocation: PreToolCallHookInvocation) -> PreToolCall:
    return PreToolCall.model_construct(turn_id=invocation.turn_id, **_tool_call_fields(invocation.tool_call))


def _tool_result_view(result: protocol.ToolResult) -> ToolResult:
    fields: dict[str, Any] = {
        "content": to_session_content(result.content, keep_origin=True),
        "is_error": result.type == "failure",
        "meta": dict(result.meta or {}),
    }
    if "structured_content" in result.model_fields_set:
        fields["structured_content"] = result.structured_content
    # Constructed, not validated: a tool's result may hold blocks a hook could not build, such as audio.
    return ToolResult.model_construct(_fields_set=set(fields), **fields)


def post_tool_call_view(invocation: PostToolCallHookInvocation) -> PostToolCall:
    return PostToolCall.model_construct(
        turn_id=invocation.turn_id,
        tool_result=_tool_result_view(invocation.tool_result),
        **_tool_call_fields(invocation.tool_call),
    )


def to_core_tool_result(result: ToolResult, original: protocol.ToolResult) -> protocol.ToolResult:
    """The Runtime tool result for the ``result`` a ``post_tool_call`` Hook returned for ``original``."""

    # Compared with a fresh view, not with the one the Hook got: the Hook may have edited that
    # one's blocks in place.
    fresh = _tool_result_view(original)
    if result.model_dump() == fresh.model_dump() and ("structured_content" in result.model_fields_set) == (
        "structured_content" in fresh.model_fields_set
    ):
        return original
    content = to_core_content(result.content)
    fields: dict[str, object] = {"content": content, "_meta": result.meta or None}
    if "structured_content" in result.model_fields_set:
        fields["structured_content"] = result.structured_content
    if not result.is_error:
        return protocol.ToolSuccessResult.model_validate(fields)
    if not isinstance(original, protocol.ToolFailureResult):
        return protocol.ToolFailureResult.model_validate({**fields, "error": tool_returned_error(content)})
    # A failed call kept failed keeps its whole error, so the model reads the same error.
    return protocol.ToolFailureResult.model_validate({**fields, "error": original.error})


__all__ = [
    "FinishReason",
    "HookDecision",
    "HookDecisionKind",
    "PostAgentTurn",
    "PostLlmCall",
    "PostToolCall",
    "PostToolCallHookContinue",
    "PreAgentTurn",
    "PreLlmCall",
    "PreToolCall",
    "reject",
    "retry",
    "skip",
]
