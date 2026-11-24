"""A run whose per-run budget has room for only ONE more call spends it on its wrap-up: tools off, the model writes
what is built, what is left and offers to continue (P8-RUNS 2026-11-15: a Company Setup run stopped at 43,930 of
40,000 points with no word from the model). Red on old code: delete the ``budget_wrap_up_notice`` block in
``execute_until_complete`` and the run keeps calling tools until the hard stop."""

from __future__ import annotations

import pytest

from test_the_iteration_ceiling_ends_with_an_answer import (  # noqa: E402
    TOOL,
    WRAP_UP_TEXT,
    _config,
    _configure,
    _set_context,
    _text_of,
    _tool_calls_in,
    _tool_hungry_model,
    probe_tool,  # noqa: F401 — the fixture
)

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

NOTICE = "SYSTEM NOTICE: only this reply fits the run's budget. Tools are off. Say what is built and what is left."


@pytest.mark.asyncio
async def test_the_last_call_that_fits_the_budget_is_the_wrap_up(probe_tool, monkeypatch):  # noqa: F811
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers import guardrail_gate

    offered = _tool_hungry_model(monkeypatch, ignores_empty_tool_list=False)
    _configure()
    _set_context(sub_agent=False)
    asks: list[int] = []

    def _wrap_up(_ctx):
        asks.append(1)
        return NOTICE if len(probe_tool) >= 2 else None

    guardrail_gate.set_guardrail_host(guarded=lambda _c: True, resolver=lambda _c, _p: None, accrue=None,
                                      budget_wrap_up=_wrap_up)
    try:
        completed = await execute_ai_request(_config(), max_iterations=20)
    finally:
        guardrail_gate.set_guardrail_host(guarded=None, resolver=None, accrue=None)

    assert len(probe_tool) == 2, f"{len(probe_tool)} tool rounds ran; the budget allowed 2"
    assert offered[-1] == [], f"the wrap-up turn was offered tools: {offered[-1]}"
    last = list(completed.request.config.messages)[-1]
    assert last.role == "assistant" and _tool_calls_in(last) == 0 and _text_of(last) == WRAP_UP_TEXT
    meta = completed.metadata or {}
    assert meta.get("budget_wrap_up") is True
    assert meta.get("status") != "max_iterations_exceeded", "a budget wrap-up was recorded as the step ceiling"
    host = [m for m in completed.request.config.messages if (m.metadata or {}).get("authored_reason") == "budget_wrap_up"]
    assert len(host) == 1 and NOTICE in _text_of(host[0])
    assert TOOL
