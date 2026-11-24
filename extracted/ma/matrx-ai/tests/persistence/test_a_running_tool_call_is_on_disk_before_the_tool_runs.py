"""A ``chat.tool_call`` row is ON DISK, ``status='running'``, before its tool runs.

The data-loss class (2026-11-03): ``log_started`` only QUEUED the row's INSERT
on the request Coordinator, which commits at the iteration's flush — after the
tool (and every parallel sibling) finishes. A server death mid-tool (deploy,
OOM, ECS task replaced) therefore lost every row of the in-flight calls: the
reloaded conversation showed no trace that the tool ever ran, and nothing was
left 'running' for the watchdog or crash recovery to settle.

The rule: ``log_started`` commits what the Coordinator holds and waits for it
to land (``Coordinator.commit_queued_now``) before returning, so the row exists
the instant the tool starts. The completion is then an ordinary UPDATE of that
row on the next Session — exactly ONE insert ever reaches the database, keyed
on the row id we minted (never the provider ``call_id``, which is not globally
unique).

Gut check: delete the ``_write_ahead`` call in ``log_started`` and
``test_the_row_is_running_on_disk_while_the_tool_runs`` fails — the fake
database is empty while the tool is "running".
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

import matrx_ai.persistence.coordinator as coord_mod
from matrx_ai.persistence.coordinator import Coordinator
from matrx_ai.tools import logger as logger_mod
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "tool_call"
    db_schema = "chat"


class _ToolCallModel:
    _meta = _Meta()

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


@contextlib.asynccontextmanager
async def _fake_transaction(*args: Any, **kwargs: Any):
    yield


@pytest.fixture
def db(monkeypatch: pytest.MonkeyPatch):
    """A fake database: every executed op, in order, plus the resulting rows."""
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    monkeypatch.setattr(coord_mod, "get_model", lambda table: _ToolCallModel)
    coord_mod._inflight_commits = 0
    state: dict[str, Any] = {"rows": {}, "ops": []}

    async def execute_tiers(tiers):
        written = 0
        for tier in tiers:
            for op in tier:
                state["ops"].append((op.op_type, str(op.pk_value)))
                row = state["rows"].setdefault(str(op.pk_value), {})
                row.update(dict(op.payload))
                written += 1
        return written

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", execute_tiers)
    yield state
    coord_mod._inflight_commits = 0


@pytest.fixture
def request_scope(monkeypatch: pytest.MonkeyPatch):
    conversation_id = str(uuid4())
    request_id = str(uuid4())
    user_id = str(uuid4())
    coord = Coordinator(request_id=request_id, conversation_id=conversation_id)

    async def _no_parents(**_kwargs: Any) -> None:
        return None

    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _no_parents)
    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(
        logger_mod,
        "_queue_tool_call_create",
        lambda **data: coord.queue("chat.tool_call", data, op_type="insert"),
    )
    monkeypatch.setattr(logger_mod, "_cx_tool_call_supports_as_called", lambda: False)
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, _uid: data)
    monkeypatch.setattr(logger_mod, "try_get_tracker", lambda: None)
    monkeypatch.setattr(ToolExecutionLogger, "_stamp_run_link", classmethod(lambda cls, data: None))

    app_ctx = SimpleNamespace(
        user_id=user_id,
        conversation_id=conversation_id,
        request_id=request_id,
        store=True,
        metadata={},
        emitter=None,
    )
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: app_ctx)
    monkeypatch.setattr("matrx_ai.context.app_context.get_app_context", lambda: app_ctx)
    return SimpleNamespace(coord=coord, ctx=app_ctx)


def _tool_ctx(scope: SimpleNamespace, call_id: str) -> ToolContext:
    return ToolContext(
        call_id=call_id,
        tool_name="slow_tool",
        conversation_id=scope.ctx.conversation_id,
        request_id=scope.ctx.request_id,
        user_id=scope.ctx.user_id,
    )


_TOOL = ToolDefinition(
    name="slow_tool",
    description="test",
    parameters={"type": "object", "properties": {}},
    tool_type=ToolType.LOCAL,
)


@pytest.mark.asyncio
async def test_the_row_is_running_on_disk_while_the_tool_runs(db, request_scope) -> None:
    row_id = await ToolExecutionLogger().log_started(
        _tool_ctx(request_scope, "toolu_same_provider_id"), _TOOL, {"q": "x"}
    )
    assert row_id

    # ---- the tool is running NOW; the server dies here (no turn commit, no flush) ----
    assert row_id in db["rows"], (
        "the chat.tool_call row was only queued in memory while its tool ran — "
        "a crash now loses every trace of the call"
    )
    assert db["rows"][row_id]["status"] == "running"
    assert db["rows"][row_id]["success"] is False


@pytest.mark.asyncio
async def test_the_completion_updates_the_same_row_and_never_inserts_twice(
    db, request_scope
) -> None:
    logger = ToolExecutionLogger()
    # Two calls in one conversation sharing a provider call_id (it is NOT globally
    # unique): each is its own row, keyed on the id WE minted.
    first = await logger.log_started(_tool_ctx(request_scope, "call_dup"), _TOOL, {})
    second = await logger.log_started(_tool_ctx(request_scope, "call_dup"), _TOOL, {})
    assert first and second and first != second

    result = ToolResult(success=True, output="done", tool_name="slow_tool", call_id="call_dup")
    await logger.log_completed(first, result, [], coordinator=request_scope.coord)
    await request_scope.coord.finalize(reason="request_final_commit")

    inserts = [pk for op, pk in db["ops"] if op == "insert"]
    assert sorted(inserts) == sorted([first, second]), f"exactly one INSERT per row: {db['ops']!r}"
    assert ("update", first) in db["ops"]
    assert db["rows"][first]["status"] == "completed"
    assert db["rows"][second]["status"] == "running"


@pytest.mark.asyncio
async def test_a_write_ahead_that_does_not_land_is_reported_never_swallowed(
    db, request_scope, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: list[str] = []

    async def _capture(exc: BaseException, operation: str, **payload: Any) -> None:
        captured.append(operation)

    async def _not_durable(**_kwargs: Any) -> bool:
        return False

    monkeypatch.setattr(logger_mod, "_capture_tool_ledger_failure", _capture)
    monkeypatch.setattr(Coordinator, "commit_queued_now", lambda self, **kw: _not_durable(**kw))

    row_id = await ToolExecutionLogger().log_started(
        _tool_ctx(request_scope, "call_x"), _TOOL, {}
    )
    # The tool still runs (its row stays queued and the next barrier accounts for
    # it), but the miss is a filed failure, not a silent one.
    assert row_id
    assert captured == ["insert_started_write_ahead_not_durable"]
