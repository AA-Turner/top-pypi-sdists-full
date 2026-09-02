"""The production `ProviderTurn` — one real `UnifiedAIClient` turn → a `TurnResult`.

This is the only matrx-ai-specific mapping the conversation executor needs: build a
request from the conversation history, run it, and translate matrx-ai's
`UnifiedResponse` / `TokenUsage` into the runtime-consumer's typed `TurnResult`
(text + tool calls + a `TokenSpend` meter + a finish signal). The loop, persistence,
metering roll-ups, budget/cancel, and nesting all belong to `ConversationRunner` +
the runtime engine — this only supplies the provider turn.

Injected `client` / `cost_resolver` keep the mapping unit-testable with crafted
`UnifiedResponse` objects (no provider, no DB).
"""

from __future__ import annotations

import traceback
from collections.abc import Callable
from decimal import Decimal
from typing import Any, Protocol

from matrx_runtime import ExecutionError

from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.unified_content import TextContent
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.conversation_runtime import (
    TokenSpend,
    ToolCall,
    TurnResult,
)

CostResolver = Callable[[TokenUsage], Decimal]


class _ProviderClient(Protocol):
    async def execute(self, request: Any) -> UnifiedResponse: ...


def _default_cost(usage: TokenUsage) -> Decimal:
    try:
        return Decimal(str(usage.calculate_cost() or 0))
    except Exception:
        return Decimal("0")


class UnifiedProviderTurn:
    """A `ProviderTurn` over the real client. `sub_conversation_tools` names the
    tools whose call spawns a child conversation (the substrate then creates a
    child execution)."""

    def __init__(
        self,
        client: _ProviderClient,
        *,
        model: str,
        tools: list[Any] | None = None,
        system_instruction: Any = None,
        sub_conversation_tools: frozenset[str] = frozenset(),
        cost_resolver: CostResolver | None = None,
    ) -> None:
        self._client = client
        self._model = model
        self._tools = list(tools or [])
        self._system = system_instruction
        self._sub_tools = frozenset(sub_conversation_tools)
        self._cost = cost_resolver or _default_cost

    async def __call__(
        self, *, conversation_id: str, history: list[dict[str, Any]], iteration: int
    ) -> TurnResult:
        request = self._build_request(conversation_id, history)
        try:
            resp = await self._client.execute(request)
        except Exception as exc:  # noqa: BLE001 — provider error → a clean error turn
            return TurnResult(finish="error", error=_exec_error(exc),
                              spend=self._spend_from_exception(exc))
        return self._map(resp)

    # --- request building ----------------------------------------------------

    def _build_request(self, conversation_id: str, history: list[dict[str, Any]]) -> Any:
        from matrx_ai.config.unified_config import UnifiedConfig
        from matrx_ai.orchestrator.requests import AIMatrixRequest

        messages = MessageList([self._to_unified(m) for m in history])
        config = UnifiedConfig(
            model=self._model, messages=messages,
            tools=list(self._tools), system_instruction=self._system,
        )
        return AIMatrixRequest(conversation_id=conversation_id, config=config)

    @staticmethod
    def _to_unified(message: dict[str, Any]) -> UnifiedMessage:
        content = message.get("content")
        text = content if isinstance(content, str) else _stringify(content)
        return UnifiedMessage(role=message.get("role", "user"), content=[TextContent(text=text)])

    # --- response mapping ----------------------------------------------------

    def _map(self, resp: UnifiedResponse) -> TurnResult:
        text = self._extract_text(resp)
        tool_calls = [
            ToolCall(
                call_id=tc.id or f"call-{i}", name=tc.name, arguments=tc.arguments or {},
                spawns_conversation=tc.name in self._sub_tools,
                child_prompt=_prompt_arg(tc.arguments) if tc.name in self._sub_tools else None,
            )
            for i, tc in enumerate(self._extract_tool_calls(resp))
        ]
        spend = self._spend(resp.usage)
        if tool_calls:
            return TurnResult(text=text or None, tool_calls=tool_calls, spend=spend, finish="tools")
        finish, error = "stop", None
        if resp.finish_reason:
            try:
                if FinishReason(resp.finish_reason).is_error():
                    finish = "error"
                    error = ExecutionError(error_type="provider_finish_reason",
                                           message=resp.finish_reason)
            except ValueError:
                pass
        return TurnResult(text=text or None, spend=spend, finish=finish, error=error)

    @staticmethod
    def _extract_text(resp: UnifiedResponse) -> str:
        parts = [
            c.text
            for m in (resp.messages or []) if m.role == "assistant"
            for c in (m.content or []) if isinstance(c, TextContent)
        ]
        return "".join(parts)

    @staticmethod
    def _extract_tool_calls(resp: UnifiedResponse) -> list[ToolCallContent]:
        return [
            c for m in (resp.messages or []) for c in (m.content or [])
            if isinstance(c, ToolCallContent)
        ]

    def _spend(self, usage: TokenUsage | None) -> TokenSpend | None:
        if usage is None:
            return None
        return TokenSpend(
            usd=self._cost(usage),
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            label=usage.matrx_model_name or usage.provider_model_name or self._model,
        )

    def _spend_from_exception(self, exc: BaseException) -> TokenSpend | None:
        usage = getattr(exc, "usage", None) or getattr(exc, "token_usage", None)
        return self._spend(usage) if isinstance(usage, TokenUsage) else None


def _exec_error(exc: BaseException) -> ExecutionError:
    return ExecutionError(
        error_type=type(exc).__name__, message=str(exc),
        traceback="".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
    )


def _prompt_arg(arguments: dict[str, Any] | None) -> str | None:
    if not arguments:
        return None
    for key in ("prompt", "message", "query", "question", "input"):
        if key in arguments:
            return str(arguments[key])
    return None


def _stringify(value: Any) -> str:
    return value if isinstance(value, str) else str(value)


__all__ = ["UnifiedProviderTurn"]
