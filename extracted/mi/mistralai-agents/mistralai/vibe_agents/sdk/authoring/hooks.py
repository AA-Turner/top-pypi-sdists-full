"""Protocol-free Hook results and tool call views for authored Hooks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import JsonValue

from mistralai.vibe.harness.core import protocol
from mistralai.vibe.harness.runtime.capabilities import (
    PostToolCallHookInvocation,
    PreToolCallHookInvocation,
)

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


class PreToolCall(PreToolCallHookInvocation):
    """The tool call a ``pre_tool_call`` Hook receives."""

    @property
    def tool_name(self) -> str:
        """The authored tool's name, or the built-in's, such as ``file_system.bash``."""

        return _tool_name(self.tool_call.call)

    @property
    def tool_id(self) -> str:
        """The tool's ID: ``<namespace>.<name>``, such as ``billing.charge``, or the built-in's name."""

        return _tool_id(self.tool_call.call)

    @property
    def arguments(self) -> dict[str, JsonValue]:
        """The arguments the model produced."""

        return self.tool_call.call.arguments


class PostToolCall(PostToolCallHookInvocation):
    """The tool call and result a ``post_tool_call`` Hook receives."""

    @property
    def tool_name(self) -> str:
        """The authored tool's name, or the built-in's, such as ``file_system.bash``."""

        return _tool_name(self.tool_call.call)

    @property
    def tool_id(self) -> str:
        """The tool's ID: ``<namespace>.<name>``, such as ``billing.charge``, or the built-in's name."""

        return _tool_id(self.tool_call.call)

    @property
    def arguments(self) -> dict[str, JsonValue]:
        """The arguments the tool ran with."""

        return self.tool_call.call.arguments


__all__ = ["HookDecision", "HookDecisionKind", "PostToolCall", "PreToolCall", "reject", "retry", "skip"]
