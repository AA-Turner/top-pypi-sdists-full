"""A machine child of a delegated member turn is minted by ONE rule, never by its caller.

Live 2026-11-15 (failure register entry 19): every mandate side-quest started from a delegated
SMS / voice turn (the thread summary, the long-answer notice) crashed with
``ValueError: system_run marks unattended machine work ...``. ``run_agent(system_run=True)``
overrides the forked child with ``system_run=True`` and ``DelegatedMemberAppContext`` refused it
at construction, so two callers were patched one by one to step out of the turn first.

The rule now lives in matrx-connect (``DelegatedMemberAppContext``): the TURN is never
machine work; a machine CHILD of the turn is, and stays the same delegated member under its own
request. This file runs every package-level machine-child entry point from a delegated turn:

* ``run_agent(system_run=True)`` — every mandate run, judge, strict-JSON funnel call;
* ``run_agent(system_run=True, stream_system_run=True)``;
* the held code call (``mandates._send_call``: labelers, cleaners, the memory observer), which
  turns the AMBIENT turn into machine work with ``with_overrides(system_run=True)``.

The census at the bottom fails when a new direct ``with_overrides(... system_run=True ...)`` site
appears in the package without being added here.
"""

from __future__ import annotations

import asyncio
import contextvars
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

ORG_ID = "11111111-1111-4111-8111-111111111111"
USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"


async def _member(user_id: str, organization_id: str) -> str:
    return organization_id


def _delegated_turn():
    from matrx_connect.context import delegated_member_context

    return delegated_member_context(
        USER_ID,
        ORG_ID,
        reason="answering an inbound text to the Personal Staff number",
        channel="sms",
        prove_membership=_member,
        prover_id="test.membership",
        conversation_id="33333333-3333-4333-8333-333333333333",
    )


async def _in_empty_context(coro_fn):
    loop = asyncio.get_running_loop()
    return await loop.create_task(coro_fn(), context=contextvars.Context())


def _capturing_agent(seen: dict[str, Any]) -> Any:
    async def _execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        from matrx_connect.context.app_context import get_app_context

        seen["ctx"] = get_app_context()
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={},
        )

    return SimpleNamespace(
        name="sms-thread-summary",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        request_metadata={},
        execute=_execute,
    )


def _assert_machine_child_of(turn: Any, child: Any) -> None:
    from matrx_connect.context import DelegatedMemberAppContext

    assert child.system_run is True, "the side-quest is machine work"
    assert isinstance(child, DelegatedMemberAppContext), "it stays the same delegated member"
    assert child.organization_admission == "verified"
    assert (child.user_id, child.organization_id) == (turn.user_id, turn.organization_id)
    assert child.request_id != turn.request_id, "its own request, never the turn's"
    assert child.parent_request_id == turn.request_id, "parented under the turn"
    assert child.conversation_id != turn.conversation_id, "never written into the person's chat"


@pytest.fixture(autouse=True)
def _no_database(monkeypatch):
    import matrx_ai.db.conversation_gate as gate

    async def _present(*_a: Any, **_k: Any) -> bool:
        return False

    monkeypatch.setattr(gate, "ensure_user_request_exists", _present)


@pytest.mark.asyncio
@pytest.mark.parametrize("stream_system_run", [False, True])
async def test_run_agent_system_run_from_a_delegated_turn(stream_system_run: bool) -> None:
    from matrx_ai.agents.executor import run_agent

    async def work() -> None:
        async with _delegated_turn() as turn:
            seen: dict[str, Any] = {}
            result = await run_agent(
                _capturing_agent(seen),  # type: ignore[arg-type]
                label="mandate:communications.sms_thread_summary",
                source_app="test",
                source_feature="mandate:communications.sms_thread_summary",
                emit_lifecycle=False,
                system_run=True,
                stream_system_run=stream_system_run,
            )
            assert result.success, result.error
            _assert_machine_child_of(turn, seen["ctx"])

    await _in_empty_context(work)


@pytest.mark.asyncio
async def test_a_held_code_call_from_a_delegated_turn(monkeypatch) -> None:
    import matrx_ai.graph_nodes.shared as shared
    import matrx_ai.mandates as mandates
    import matrx_ai.orchestrator.executor as orchestrator_executor

    seen: dict[str, Any] = {}

    async def _execute_ai_request(*_a: Any, **_k: Any) -> Any:
        from matrx_connect.context.app_context import get_app_context

        seen["ctx"] = get_app_context()
        return SimpleNamespace()

    monkeypatch.setattr(orchestrator_executor, "execute_ai_request", _execute_ai_request)
    monkeypatch.setattr(mandates, "held_request_config", lambda *_a, **_k: None)
    monkeypatch.setattr(shared, "normalize_completed", lambda _c: SimpleNamespace(final_text="ok"))

    finished: list[str] = []

    async def _finish(text: str, **_k: Any) -> None:
        finished.append(text)

    held = SimpleNamespace(mandate_key="memory.observer", metadata={}, finish=_finish)

    async def work() -> None:
        async with _delegated_turn() as turn:
            await mandates._send_call(held)  # type: ignore[arg-type]
            _assert_machine_child_of(turn, seen["ctx"])

    await _in_empty_context(work)
    assert finished == ["ok"]


def test_every_direct_system_run_transition_in_the_package_is_covered_here() -> None:
    """A new ``with_overrides(... system_run=True ...)`` site is a new machine-child entry
    point: add a delegated-turn case above for it, then add it to ``COVERED``."""
    covered = {"mandates.py"}
    root = Path(__file__).resolve().parents[1] / "matrx_ai"
    pattern = re.compile(r"with_overrides\((?:[^()]|\([^()]*\))*?system_run\s*=\s*True", re.S)
    found = {
        path.name
        for path in root.rglob("*.py")
        if "tests" not in path.parts and pattern.search(path.read_text(encoding="utf-8"))
    }
    assert found == covered, f"uncovered machine-child entry points: {sorted(found - covered)}"
