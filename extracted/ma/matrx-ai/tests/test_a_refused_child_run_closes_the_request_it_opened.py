"""A child run refused before its loop closes the request row it opened (2026-11-12).

``run_agent`` ensures the child's ``chat.user_request`` early (so tool_call FKs never orphan). When the
agent then refused to run — a required input missing, raised by ``apply_variables`` before any model
call — nothing settled that row: it sat 'pending' until the lifecycle watchdog abandoned it 30 minutes
later and filed a critical ``lifecycle_watchdog_stuck_rows`` alarm (agent_call → 'DB Cartographer').

A row somebody else opened is not this run's to close, so only the one ``run_agent`` gave birth to is.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.db.conversation_gate as gate
from matrx_ai.agents.required_variables import RequiredVariablesMissing

USER_ID = "22222222-2222-4222-8222-222222222222"
REQUEST_ID = "33333333-3333-4333-8333-333333333333"


async def _run_refused_child(
    monkeypatch: pytest.MonkeyPatch, *, born: bool, cancelled: bool = False
) -> list[tuple[Any, ...]]:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    settled: list[tuple[Any, ...]] = []

    async def ensure(**_: Any) -> bool:
        return born

    async def update(request_id: str, status: str, error: str | None = None) -> None:
        settled.append((request_id, status, error))

    monkeypatch.setattr(gate, "ensure_user_request_exists", ensure)
    monkeypatch.setattr(gate, "update_user_request_status", update)

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=REQUEST_ID))

    async def refuse(*_: Any, **__: Any) -> Any:
        if cancelled:  # the parent tore the child down (a fan-out sibling failed, a deploy drain)
            raise asyncio.CancelledError()
        raise RequiredVariablesMissing(["task"], agent_name="DB Cartographer")

    agent = SimpleNamespace(
        name="DB Cartographer",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        request_metadata={},
        execute=refuse,
    )
    call = run_agent(
        agent,  # type: ignore[arg-type]
        label="cartographer",
        source_app="test",
        source_feature="agent_call",
        emit_lifecycle=False,
    )
    if cancelled:
        with pytest.raises(asyncio.CancelledError):
            await call
        return settled
    result = await call
    assert not result.success
    assert isinstance(result.exception, RequiredVariablesMissing)
    return settled


@pytest.mark.asyncio
async def test_the_request_this_run_opened_is_closed_as_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    settled = await _run_refused_child(monkeypatch, born=True)
    assert len(settled) == 1, settled
    request_id, status, error = settled[0]
    assert status == "failed"
    assert request_id  # the child's own request id, minted by the context fork
    assert "task" in (error or "")


@pytest.mark.asyncio
async def test_a_request_someone_else_opened_is_left_to_them(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _run_refused_child(monkeypatch, born=False) == []


@pytest.mark.asyncio
async def test_a_cancelled_child_closes_the_request_it_opened(monkeypatch: pytest.MonkeyPatch) -> None:
    """Feedback d7435c89 (2026-11-15): the cancel path settled the run's spine but left its request
    'pending' — the lifecycle watchdog abandoned it 30 minutes later with a critical alarm."""
    settled = await _run_refused_child(monkeypatch, born=True, cancelled=True)
    assert [status for _, status, _ in settled] == ["cancelled"], settled


@pytest.mark.asyncio
async def test_a_cancelled_child_leaves_a_request_someone_else_opened(monkeypatch: pytest.MonkeyPatch) -> None:
    assert await _run_refused_child(monkeypatch, born=False, cancelled=True) == []
