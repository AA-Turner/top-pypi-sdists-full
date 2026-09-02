"""The conversation executor — a CONSUMER of the matrx-runtime Request Management
Layer. This is the replacement for the cx_ request-handling envelope: one
conversation = one `global_execution` (opaque `type="conversation"`); a tool that
spawns a sub-conversation = a child execution; token spend = a `MeterEvent`.

The runtime engine owns the envelope (identity, nesting, status, cost/metering,
budget/cancel, context, resume); THIS owns the conversation loop (provider turn ↔
tool dispatch). All provider/persistence/tool I/O is injected, so the orchestration
is unit-testable against the real engine + an in-memory store with fakes, and the
production build wires the real `UnifiedAIClient`, cx persistence, and
`OrmExecutionStore`. The conversation MESSAGES live in `cx_*` (linked via the
execution's `link_kind`/`link_id`); runtime never sees them.

Design: docs/runtime/REQUEST_MANAGEMENT_LAYER.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Protocol

from matrx_runtime import (
    ContextMode,
    ExecutionCancelled,
    ExecutionContext,
    ExecutionEngine,
    ExecutionError,
    GlobalExecution,
    MeterEvent,
)


class TokenSpend(MeterEvent):
    """The LLM cost event — tokens are matrx-ai's concept, not runtime's. `usd` is
    the money quantity the budget enforces; tokens roll up generically too."""

    usd: Decimal = Decimal("0")
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    provider_charge_usd: Decimal | None = None
    provider_charge_available: bool = False
    catalog_cost_usd: Decimal | None = None
    provider_catalog_variance_usd: Decimal | None = None
    cost_source: str = "catalog_from_provider_usage"
    response_id: str | None = None
    offering_id: str | None = None

    @classmethod
    def from_usage(cls, usage: Any, *, label: str, **payload_extras: Any) -> TokenSpend:
        """Build a runtime meter with both canonical cost and its evidence provenance.

        `payload_extras` are additional NON-QUANTITY attribution fields
        (`ai_model_id`, `conversation_id`, `status`, durations…) — MeterEvent is
        `extra="allow"`, so they ride into `global_meter_entry.payload` via
        `model_dump` (the same keys the 0235 backfill stamped from chat.request,
        letting the spine views shed their chat.request laterals)."""
        try:
            resolved = usage.calculate_cost()
        except Exception:
            resolved = None
        try:
            catalog = usage.calculate_catalog_cost()
        except Exception:
            catalog = None
        charge = getattr(usage, "provider_charge", None)
        provider = charge.authoritative_usd if charge is not None else None
        return cls(
            label=label,
            usd=Decimal(str(round(resolved, 6))) if resolved is not None else Decimal("0"),
            input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
            cached_tokens=int(getattr(usage, "cached_input_tokens", 0) or 0),
            provider_charge_usd=(Decimal(str(provider)) if provider is not None else None),
            provider_charge_available=provider is not None,
            catalog_cost_usd=(Decimal(str(round(catalog, 6))) if catalog is not None else None),
            provider_catalog_variance_usd=(
                Decimal(str(round(provider - catalog, 6)))
                if provider is not None and catalog is not None
                else None
            ),
            # ``usd`` is always our catalog amount. Provider dollars are
            # comparison evidence and must never change runtime settlement.
            cost_source="catalog_from_provider_usage",
            response_id=getattr(usage, "response_id", None) or None,
            offering_id=getattr(usage, "offering_id", None) or None,
            **payload_extras,
        )


@dataclass
class ToolCall:
    call_id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    # When True, this call is a sub-conversation ("conversation → conversation"):
    # the runner spawns a CHILD execution and runs a nested conversation for it.
    spawns_conversation: bool = False
    child_prompt: str | None = None  # the seed message for the spawned conversation


@dataclass
class ToolResult:
    call_id: str
    content: Any
    is_error: bool = False
    spend: TokenSpend | None = None  # a tool may itself bill


@dataclass
class TurnResult:
    """What one provider turn produced (the matrx-ai adapter maps a UnifiedResponse
    to this)."""

    text: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    spend: TokenSpend | None = None
    finish: str = "stop"  # "stop" | "tools" | "error"
    error: ExecutionError | None = None


class ProviderTurn(Protocol):
    """Run ONE provider turn over the conversation history (oldest→newest list of
    ``{"role","content"}``). Production: wrap UnifiedAIClient. Tests: scripted."""

    async def __call__(
        self, *, conversation_id: str, history: list[dict[str, Any]], iteration: int
    ) -> TurnResult: ...


class ConversationPersistence(Protocol):
    """Persist conversation turns to the consumer's own store (cx_*). The runner
    never assumes a schema — it just appends typed turns and reads history back."""

    async def append_turn(
        self,
        *,
        conversation_id: str,
        execution_id: str,
        role: str,
        content: Any,
    ) -> None: ...

    async def history(self, conversation_id: str) -> list[dict[str, Any]]: ...


class ToolDispatch(Protocol):
    async def __call__(self, call: ToolCall) -> ToolResult: ...


@dataclass
class ConversationResult:
    execution: GlobalExecution
    conversation_id: str
    iterations: int
    total_cost: Decimal
    child_execution_ids: list[str] = field(default_factory=list)


class ConversationRunner:
    """Drives one conversation on the runtime spine."""

    def __init__(
        self,
        engine: ExecutionEngine,
        *,
        provider_turn: ProviderTurn,
        persistence: ConversationPersistence,
        tool_dispatch: ToolDispatch | None = None,
        max_iterations: int = 50,
    ) -> None:
        self._engine = engine
        self._turn = provider_turn
        self._cx = persistence
        self._dispatch = tool_dispatch
        self._max = max_iterations

    async def run(
        self,
        *,
        conversation_id: str,
        user_message: str,
        request_id: str | None = None,
        context: ExecutionContext | dict | None = None,
        cost_budget: Decimal | None = None,
        execution_id: str | None = None,
        parent_execution_id: str | None = None,
        context_mode: ContextMode = ContextMode.INHERIT,
    ) -> ConversationResult:
        # one conversation = one execution, linked to the cx conversation record
        if parent_execution_id is not None:
            execution = await self._engine.spawn_child(
                parent_execution_id, type="conversation", context_mode=context_mode,
                link_kind="conversation", link_id=conversation_id, execution_id=execution_id,
            )
        else:
            execution = await self._engine.create_root(
                type="conversation", request_id=request_id, context=context,
                cost_budget=cost_budget, link_kind="conversation", link_id=conversation_id,
                execution_id=execution_id,
            )
        await self._engine.start(execution.id)
        await self._cx.append_turn(
            conversation_id=conversation_id, execution_id=execution.id,
            role="user", content=user_message,
        )

        run_cost = Decimal("0")
        child_ids: list[str] = []
        iterations = 0
        for iteration in range(1, self._max + 1):
            iterations = iteration

            # budget / per-quantity limit / cancel / deadline — checked every turn
            try:
                await self._engine.ensure_can_proceed(execution.id)
            except ExecutionCancelled:
                settled = await self._engine.cancel(execution.id, cost=run_cost)
                return self._result(settled, conversation_id, iterations, run_cost, child_ids)
            except Exception as exc:  # budget/limit/deadline — settle FAILED, loud
                settled = await self._engine.fail(
                    execution.id,
                    error=ExecutionError(error_type=type(exc).__name__, message=str(exc)),
                    cost=run_cost,
                )
                return self._result(settled, conversation_id, iterations, run_cost, child_ids)

            history = await self._cx.history(conversation_id)
            turn = await self._turn(
                conversation_id=conversation_id, history=history, iteration=iteration
            )
            run_cost += await self._meter(execution.id, turn.spend)

            if turn.text:
                await self._cx.append_turn(
                    conversation_id=conversation_id, execution_id=execution.id,
                    role="assistant", content=turn.text,
                )

            if turn.finish == "error":
                settled = await self._engine.fail(
                    execution.id,
                    error=turn.error or ExecutionError(
                        error_type="provider_error", message="conversation turn failed"
                    ),
                    cost=run_cost,
                )
                return self._result(settled, conversation_id, iterations, run_cost, child_ids)

            if turn.finish != "tools" or not turn.tool_calls:
                settled = await self._engine.complete(execution.id, cost=run_cost)
                return self._result(settled, conversation_id, iterations, run_cost, child_ids)

            # dispatch tools — a sub-conversation tool spawns + runs a child execution
            for call in turn.tool_calls:
                if call.spawns_conversation:
                    child = await self.run(
                        conversation_id=f"{conversation_id}::sub::{call.call_id}",
                        user_message=call.child_prompt or "",
                        parent_execution_id=execution.id,
                    )
                    child_ids.append(child.execution.id)
                    run_cost_child = child.total_cost  # already on the child execution; tree rollup sums it
                    await self._cx.append_turn(
                        conversation_id=conversation_id, execution_id=execution.id,
                        role="tool", content={"call_id": call.call_id,
                                              "child_execution_id": child.execution.id,
                                              "cost": str(run_cost_child)},
                    )
                    continue

                result = await self._run_tool(call)
                run_cost += await self._meter(execution.id, result.spend)
                await self._cx.append_turn(
                    conversation_id=conversation_id, execution_id=execution.id,
                    role="tool", content={"call_id": call.call_id, "result": result.content,
                                          "is_error": result.is_error},
                )

            await self._engine.save_checkpoint(execution.id, {"iteration": iteration})

        # ran out of iterations
        settled = await self._engine.fail(
            execution.id,
            error=ExecutionError(error_type="matrx_max_iterations",
                                 message=f"conversation hit the {self._max}-turn ceiling"),
            cost=run_cost,
        )
        return self._result(settled, conversation_id, iterations, run_cost, child_ids)

    # --- internals -----------------------------------------------------------

    async def _meter(self, execution_id: str, spend: TokenSpend | None) -> Decimal:
        if spend is None:
            return Decimal("0")
        return await self._engine.record(execution_id, spend)

    async def _run_tool(self, call: ToolCall) -> ToolResult:
        if self._dispatch is None:
            return ToolResult(call_id=call.call_id, content=None,
                              is_error=True)
        return await self._dispatch(call)

    def _result(self, execution, conversation_id, iterations, run_cost, child_ids):
        return ConversationResult(
            execution=execution, conversation_id=conversation_id, iterations=iterations,
            total_cost=run_cost, child_execution_ids=child_ids,
        )


__all__ = [
    "ConversationRunner",
    "ConversationResult",
    "ConversationPersistence",
    "ProviderTurn",
    "ToolDispatch",
    "TurnResult",
    "ToolCall",
    "ToolResult",
    "TokenSpend",
]
