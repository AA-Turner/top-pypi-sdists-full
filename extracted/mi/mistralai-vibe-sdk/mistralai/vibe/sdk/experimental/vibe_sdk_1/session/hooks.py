"""Ergonomic session hook bindings."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal

from pydantic import JsonValue

from .events import (
    ClientHookCallback,
    PostAgentTurnInput,
    PostLLMCallInput,
    PostToolCallInput,
    PreAgentTurnInput,
    PreLLMCallInput,
    PreToolCallInput,
)
from .models import HookDefinition, HookType

type HookOutput = JsonValue
type HookHandler = Callable[[JsonValue], HookOutput | Awaitable[HookOutput]]
type PreAgentTurnHook = Callable[[PreAgentTurnInput], HookOutput | Awaitable[HookOutput]]
type PostAgentTurnHook = Callable[[PostAgentTurnInput], HookOutput | Awaitable[HookOutput]]
type PreLLMCallHook = Callable[[PreLLMCallInput], HookOutput | Awaitable[HookOutput]]
type PostLLMCallHook = Callable[[PostLLMCallInput], HookOutput | Awaitable[HookOutput]]
type PreToolCallHook = Callable[[PreToolCallInput], HookOutput | Awaitable[HookOutput]]
type PostToolCallHook = Callable[[PostToolCallInput], HookOutput | Awaitable[HookOutput]]

_HOOK_FIELDS: dict[HookType, str] = {
    "pre_agent_turn": "pre_agent_turn",
    "post_agent_turn": "post_agent_turn",
    "pre_llm_call": "pre_llm_call",
    "post_llm_call": "post_llm_call",
    "pre_mcp_tool_call": "pre_mcp_tool_call",
    "post_mcp_tool_call": "post_mcp_tool_call",
    "pre_client_tool_call": "pre_client_tool_call",
    "post_client_tool_call": "post_client_tool_call",
    "pre_tool_call": "pre_tool_call",
    "post_tool_call": "post_tool_call",
}


@dataclass(frozen=True, slots=True)
class SessionHooks:
    """Live hook callables supplied to the ergonomic Agent."""

    pre_agent_turn: PreAgentTurnHook | HookHandler | None = None
    post_agent_turn: PostAgentTurnHook | HookHandler | None = None
    pre_llm_call: PreLLMCallHook | HookHandler | None = None
    post_llm_call: PostLLMCallHook | HookHandler | None = None
    pre_mcp_tool_call: PreToolCallHook | HookHandler | None = None
    post_mcp_tool_call: PostToolCallHook | HookHandler | None = None
    pre_client_tool_call: PreToolCallHook | HookHandler | None = None
    post_client_tool_call: PostToolCallHook | HookHandler | None = None
    pre_tool_call: PreToolCallHook | HookHandler | None = None
    post_tool_call: PostToolCallHook | HookHandler | None = None

    def definitions(self) -> tuple[HookDefinition, ...]:
        definitions: list[HookDefinition] = []
        for hook_type, field_name in _HOOK_FIELDS.items():
            if getattr(self, field_name) is not None:
                definitions.append(HookDefinition(type=hook_type, name=field_name))
        return tuple(definitions)

    def handler_for(self, callback: ClientHookCallback) -> HookHandler | None:
        if callback.name not in _HOOK_FIELDS.values():
            return None
        return getattr(self, callback.name)


type HookLifecycle = Literal[
    "pre_agent_turn",
    "post_agent_turn",
    "pre_llm_call",
    "post_llm_call",
    "pre_mcp_tool_call",
    "post_mcp_tool_call",
    "pre_client_tool_call",
    "post_client_tool_call",
    "pre_tool_call",
    "post_tool_call",
]
