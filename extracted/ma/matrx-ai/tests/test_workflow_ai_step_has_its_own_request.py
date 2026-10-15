"""Every AI step of a workflow run is its OWN ``chat.user_request`` (AI-WATCH.md, 2026-10-14).

THE DEFECT THIS GUARDS: ``fork_for_workflow_step`` copies the workflow root's
``request_id`` into every step context, and the request row is created idempotently
under that id — so a Smart Add round's seven AI calls (facts, we_think, classify,
entity_kind, ...) all wrote into ONE row. Watch AI listed one entry and the live lanes
all bound to the same server run.

SUT: the real ``run_step_agent``; only the host's agent runner is replaced, to record
the context each step runs under. Reverting the per-step id makes both steps report
the root's id and this fails.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

from matrx_connect.context.app_context import AppContext, get_app_context

from matrx_ai.graph_nodes import agent_action

ROOT_REQUEST = "7c1f0e2a-5d3b-4e8f-9a61-2b4c6d8e0f13"


class _Emitter:
    def __init__(self) -> None:
        self.reserved: list[Any] = []

    async def send_record_reserved(self, payload: Any) -> None:
        self.reserved.append(payload)


def test_each_ai_step_runs_under_its_own_request_id(monkeypatch: Any) -> None:
    seen: list[tuple[str | None, str | None]] = []
    emitter = _Emitter()

    async def fake_runner(agent_id: str, request: Any, ctx: AppContext) -> str:
        assert ctx is get_app_context()
        seen.append((ctx.request_id, ctx.metadata.get("mandate_key")))
        return "ok"

    monkeypatch.setattr(agent_action, "get_ext", lambda name: fake_runner)
    monkeypatch.setattr(agent_action, "has_ext", lambda name: False)

    root = AppContext(emitter=emitter, user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0", request_id=ROOT_REQUEST)

    async def run_two() -> None:
        for node_id, key in (("facts", "brand_intake.early_facts"), ("we_think", "brand_intake.we_think")):
            step = SimpleNamespace(app=root.fork_for_workflow_step(f"conv-{node_id}"), node_id=node_id)
            await agent_action.run_step_agent(step, "agent", object(), mandate_key=key)  # type: ignore[arg-type]

    asyncio.run(run_two())

    ids = [rid for rid, _ in seen]
    assert len(seen) == 2
    assert ROOT_REQUEST not in ids, "a step must never run under the workflow root's request id"
    assert ids[0] != ids[1], "two AI steps must be two requests"
    assert [k for _, k in seen] == ["brand_intake.early_facts", "brand_intake.we_think"]
    # Each step names its run on the live wire before the call, so the run page binds its lane.
    assert [(p.table, p.record_id) for p in emitter.reserved] == [("user_request", rid) for rid in ids]
