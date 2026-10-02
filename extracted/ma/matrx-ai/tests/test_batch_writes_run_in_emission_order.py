"""Writes to one tool in one batch run in the order the model emitted them.

Walk 24 (2026-10-01): the interviewer emitted `rulebook` update_meta (create
the sections) then `rulebook` add_rules (file rules under them) in one
response. `execute_batch` ran both at once; add_rules started 2.5 ms after
update_meta, read the Rulebook before the sections existed, and was refused —
and the model's retry narration leaked to the Expert's screen.

The fake `execute` below reproduces the real shape: a writer that commits
after an await, and a second writer that reads the record first.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult
from matrx_ai.tools.registry import ToolRegistry


def _executor() -> ToolExecutor:
    registry = ToolRegistry()
    registry.register(ToolDefinition(name="rulebook", side_effect_class="db_write"))
    registry.register(ToolDefinition(name="web_search", side_effect_class="read_only"))
    return ToolExecutor(registry=registry, lifecycle=object())  # type: ignore[arg-type]


def _ctx() -> ToolContext:
    return ToolContext(call_id="", tool_name="", user_id="u", request_id="r")


def _calls(*specs: tuple[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"name": n, "arguments": a, "call_id": f"c{i}"} for i, (n, a) in enumerate(specs)]


@pytest.mark.asyncio
async def test_section_creation_lands_before_rules_filed_under_it(monkeypatch):
    executor = _executor()
    record = {"sections": ["G"]}

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        if arguments["action"] == "update_meta":
            await asyncio.sleep(0.01)  # the write commits after a round trip
            record["sections"].append("verdict")
            return {"ok": True}, ToolResult(success=True, output={"ok": True})
        await asyncio.sleep(0)
        ok = "verdict" in record["sections"]
        return {"ok": ok}, ToolResult(success=ok, output={"ok": ok})

    monkeypatch.setattr(executor, "execute", fake_execute)
    _, results = await executor.execute_batch(
        _calls(("rulebook", {"action": "update_meta"}), ("rulebook", {"action": "add_rules"})),
        _ctx(),
    )
    assert [r.success for r in results] == [True, True]


@pytest.mark.asyncio
async def test_reads_still_run_concurrently(monkeypatch):
    executor = _executor()
    live = {"now": 0, "peak": 0}

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        live["now"] += 1
        live["peak"] = max(live["peak"], live["now"])
        await asyncio.sleep(0.01)
        live["now"] -= 1
        return {}, ToolResult(success=True, output={"q": arguments["q"]})

    monkeypatch.setattr(executor, "execute", fake_execute)
    _, results = await executor.execute_batch(
        _calls(("web_search", {"q": 1}), ("web_search", {"q": 2}), ("web_search", {"q": 3})),
        _ctx(),
    )
    assert live["peak"] == 3
    assert [r.output["q"] for r in results] == [1, 2, 3]


@pytest.mark.asyncio
async def test_unclassified_tool_is_chained_and_results_keep_their_slots(monkeypatch):
    executor = _executor()
    order: list[str] = []

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        await asyncio.sleep(arguments["delay"])
        order.append(ctx.call_id)
        if arguments.get("boom"):
            raise RuntimeError("boom")
        return {"id": ctx.call_id}, ToolResult(success=True, output={"id": ctx.call_id})

    monkeypatch.setattr(executor, "execute", fake_execute)
    content, results = await executor.execute_batch(
        _calls(
            ("mystery", {"delay": 0.02}),
            ("web_search", {"delay": 0.0}),
            ("mystery", {"delay": 0.0, "boom": True}),
            ("mystery", {"delay": 0.0}),
        ),
        _ctx(),
    )
    # The unclassified tool's calls ran first-to-last despite their delays;
    # the read ran beside them.
    assert [c for c in order if c != "c1"] == ["c0", "c2", "c3"]
    assert [r.success for r in results] == [True, True, False, True]
    assert len(content) == 4


@pytest.mark.asyncio
async def test_sub_agent_fan_out_stays_parallel(monkeypatch):
    from matrx_ai.tools.models import ToolType

    executor = _executor()
    executor.registry.register(ToolDefinition(name="researcher", tool_type=ToolType.AGENT))
    live = {"now": 0, "peak": 0}

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        live["now"] += 1
        live["peak"] = max(live["peak"], live["now"])
        await asyncio.sleep(0.01)
        live["now"] -= 1
        return {}, ToolResult(success=True, output={})

    monkeypatch.setattr(executor, "execute", fake_execute)
    await executor.execute_batch(
        _calls(("researcher", {"q": 1}), ("researcher", {"q": 2})), _ctx()
    )
    assert live["peak"] == 2


@pytest.mark.asyncio
async def test_a_call_cancelled_on_its_own_is_its_result_never_its_siblings_loss(monkeypatch):
    executor = _executor()

    async def fake_execute(name, arguments, ctx, client_tools=None, allowed_tools=None):
        await asyncio.sleep(0.01)
        if arguments.get("cancel"):
            raise asyncio.CancelledError()
        return {"id": ctx.call_id}, ToolResult(success=True, output={"id": ctx.call_id})

    monkeypatch.setattr(executor, "execute", fake_execute)
    _, results = await executor.execute_batch(
        _calls(
            ("rulebook", {"action": "update_meta", "cancel": True}),
            ("rulebook", {"action": "add_rules"}),
            ("web_search", {"q": 1}),
        ),
        _ctx(),
    )
    assert [r.success for r in results] == [False, True, True]
