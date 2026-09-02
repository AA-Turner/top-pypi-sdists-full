"""The conversation executor on the runtime spine — a REAL conversation flowing
through `matrx_runtime.ExecutionEngine`, with provider/cx/tool I/O faked but the
runtime engine + store REAL (in-memory). This is the cx_ request-handling
replacement proven: one conversation = one execution, token spend metered, a
sub-conversation = a child execution, budget/cancel enforced.

Runs under matrx-ai's conftest (DB stubs) so imports resolve; no real DB/provider.
"""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from matrx_runtime import (
    ExecutionEngine,
    ExecutionStatus,
    InMemoryExecutionStore,
)

from matrx_ai.orchestrator.conversation_runtime import (
    ConversationRunner,
    TokenSpend,
    ToolCall,
    ToolResult,
    TurnResult,
)


def test_token_spend_keeps_provider_charge_as_evidence_only() -> None:
    class Charge:
        authoritative_usd = 0.07

    class Usage:
        input_tokens = 100
        output_tokens = 10
        cached_input_tokens = 0
        provider_charge = Charge()
        response_id = "response-1"
        offering_id = "offering-1"

        @staticmethod
        def calculate_cost() -> float:
            return 0.08

        @staticmethod
        def calculate_catalog_cost() -> float:
            return 0.08

    spend = TokenSpend.from_usage(Usage(), label="provider_call:1")

    assert spend.usd == Decimal("0.08")
    assert spend.cost_source == "catalog_from_provider_usage"
    assert spend.provider_charge_available is True
    assert spend.provider_charge_usd == Decimal("0.07")
    assert spend.provider_catalog_variance_usd == Decimal("-0.01")


class FakeCx:
    """Stands in for cx_* persistence — records turns, replays history."""

    def __init__(self):
        self.turns = defaultdict(list)

    async def append_turn(self, *, conversation_id, execution_id, role, content):
        self.turns[conversation_id].append(
            {"role": role, "content": content, "execution_id": execution_id}
        )

    async def history(self, conversation_id):
        return [{"role": t["role"], "content": t["content"]} for t in self.turns[conversation_id]]


class FakeProvider:
    """Scripted turns keyed by conversation_id; an optional per-turn hook lets a
    test cause a side effect (e.g. request cancel)."""

    def __init__(self, scripts, *, on_turn=None):
        self._scripts = {k: list(v) for k, v in scripts.items()}
        self._on_turn = on_turn
        self.seen = []

    async def __call__(self, *, conversation_id, history, iteration):
        self.seen.append((conversation_id, iteration))
        if self._on_turn is not None:
            await self._on_turn(conversation_id, iteration)
        queue = self._scripts.get(conversation_id, [])
        return queue.pop(0) if queue else TurnResult(text="(done)", finish="stop")


async def _cheap_tool(call):
    return ToolResult(call_id=call.call_id, content="tool-ok", spend=TokenSpend(usd=Decimal("0.01")))


def _setup(scripts, *, on_turn=None, tool=_cheap_tool):
    store = InMemoryExecutionStore()
    engine = ExecutionEngine(store)
    cx = FakeCx()
    runner = ConversationRunner(
        engine, provider_turn=FakeProvider(scripts, on_turn=on_turn),
        persistence=cx, tool_dispatch=tool,
    )
    return runner, engine, store, cx


# --- a real single-turn chat ------------------------------------------------

async def test_simple_chat_creates_execution_meters_and_persists():
    runner, engine, _, cx = _setup({
        "conv-1": [TurnResult(text="hi there",
                              spend=TokenSpend(usd=Decimal("0.10"), input_tokens=20, output_tokens=5),
                              finish="stop")],
    })
    result = await runner.run(conversation_id="conv-1", user_message="hello", request_id="req-1")

    ex = result.execution
    assert ex.type == "conversation"
    assert ex.status is ExecutionStatus.COMPLETED
    assert ex.link_kind == "conversation" and ex.link_id == "conv-1"  # linked, not owned
    assert ex.request_id == "req-1"
    assert result.total_cost == Decimal("0.10")
    # token spend metered onto the execution (money → cost, tokens → meters)
    assert ex.cost == Decimal("0.10")
    assert ex.meters["input_tokens"] == Decimal("20")
    # conversation turns went to cx (the consumer's store), not runtime
    assert [t["role"] for t in cx.turns["conv-1"]] == ["user", "assistant"]


# --- multi-turn with a tool -------------------------------------------------

async def test_tool_turn_then_finish_sums_cost():
    runner, _, _, cx = _setup({
        "conv-1": [
            TurnResult(text="let me check",
                       tool_calls=[ToolCall(call_id="c1", name="search")],
                       spend=TokenSpend(usd=Decimal("0.05"), input_tokens=10), finish="tools"),
            TurnResult(text="done", spend=TokenSpend(usd=Decimal("0.03")), finish="stop"),
        ],
    })
    result = await runner.run(conversation_id="conv-1", user_message="q")
    assert result.execution.status is ExecutionStatus.COMPLETED
    assert result.total_cost == Decimal("0.09")  # 0.05 turn + 0.01 tool + 0.03 turn
    assert [t["role"] for t in cx.turns["conv-1"]] == ["user", "assistant", "tool", "assistant"]


# --- conversation → conversation (the A2A case) on the spine ----------------

async def test_sub_conversation_spawns_child_execution():
    runner, engine, _, _ = _setup({
        "conv-1": [
            TurnResult(tool_calls=[ToolCall(call_id="c1", name="ask_expert",
                                            spawns_conversation=True, child_prompt="sub q")],
                       spend=TokenSpend(usd=Decimal("0.05")), finish="tools"),
            TurnResult(text="final", spend=TokenSpend(usd=Decimal("0.02")), finish="stop"),
        ],
        "conv-1::sub::c1": [
            TurnResult(text="expert answer",
                       spend=TokenSpend(usd=Decimal("0.07"), input_tokens=15), finish="stop"),
        ],
    })
    result = await runner.run(conversation_id="conv-1", user_message="q")

    assert len(result.child_execution_ids) == 1
    child = await engine.get_execution(result.child_execution_ids[0])
    assert child.type == "conversation"                       # a conversation, not "agent"
    assert child.parent_execution_id == result.execution.id   # nested on the spine
    assert child.root_execution_id == result.execution.id
    # the WHOLE tree's cost rolls up: 0.05 + 0.02 (parent) + 0.07 (child)
    assert await engine.tree_cost(result.execution.id) == Decimal("0.14")
    assert await engine.tree_quantity(result.execution.id, "input_tokens") == Decimal("15")


# --- the envelope guarantees ------------------------------------------------

async def test_budget_halts_the_conversation():
    runner, _, _, _ = _setup({
        "conv-1": [
            TurnResult(tool_calls=[ToolCall(call_id="c1", name="search")],
                       spend=TokenSpend(usd=Decimal("0.10")), finish="tools"),  # blows 0.05 budget
        ],
    })
    result = await runner.run(conversation_id="conv-1", user_message="q", cost_budget=Decimal("0.05"))
    assert result.execution.status is ExecutionStatus.FAILED
    assert result.execution.error.error_type == "BudgetExceeded"


async def test_cancel_halts_the_conversation():
    async def cancel_on_first_turn(conversation_id, iteration):
        if iteration == 1:
            # find the conversation's execution (linked by link_id) and cancel the tree
            for ex in store._executions.values():
                if ex.link_id == conversation_id:
                    await engine.request_cancel(ex.id)

    runner, engine, store, _ = _setup(
        {"conv-1": [TurnResult(tool_calls=[ToolCall(call_id="c1", name="search")],
                               spend=TokenSpend(usd=Decimal("0.01")), finish="tools")]},
        on_turn=cancel_on_first_turn,
    )
    result = await runner.run(conversation_id="conv-1", user_message="q")
    assert result.execution.status is ExecutionStatus.CANCELLED


async def test_provider_error_fails_the_conversation():
    from matrx_runtime import ExecutionError

    runner, _, _, _ = _setup({
        "conv-1": [TurnResult(finish="error",
                              error=ExecutionError(error_type="provider_500", message="upstream"),
                              spend=TokenSpend(usd=Decimal("0.02")))],
    })
    result = await runner.run(conversation_id="conv-1", user_message="q")
    assert result.execution.status is ExecutionStatus.FAILED
    assert result.execution.error.error_type == "provider_500"
    assert result.total_cost == Decimal("0.02")  # a failed turn STILL billed
