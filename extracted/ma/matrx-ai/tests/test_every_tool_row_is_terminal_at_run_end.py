"""Every tool-call row of a run is terminal when the run ends (PB-08, defect 58).

A run that ends — completed, failed, cancelled, disconnected — must never leave a
``chat.tool_call`` row it opened at ``running``/``pending``. The periodic stale
sweep only repaints such a row minutes later; until then the transcript shows a
tool that is "still running" in a run that is over (Tidewell's ``agent`` row).

Two halves:
  * behaviour — a row opened and never settled is settled by the run-end sweep
    with an honest status and reason, queued on the run's coordinator; a row
    whose real result was queued is left alone; the sweep is loud.
  * wiring — the run's exit (``_finalize_and_persist``) runs the sweep BEFORE
    the final commit (same commit as the run's final state), and the ledger's
    close runs it as a backstop for an exit that skipped the finalize.
"""

from __future__ import annotations

import inspect

import pytest

from matrx_ai.tools import turn_ledger
from matrx_ai.tools.logger import ToolExecutionLogger


class _Coord:
    def __init__(self) -> None:
        self.ops: list[tuple[str, dict, str]] = []

    def queue(self, table, payload, *, op_type="insert", primary_key=None, depends_on=()):
        self.ops.append((table, dict(payload), op_type))
        return "op"


@pytest.fixture
def ledger():
    token = turn_ledger.start_turn_ledger()
    yield turn_ledger.get_turn_ledger()
    turn_ledger.reset_turn_ledger(token)


@pytest.mark.asyncio
async def test_an_open_row_is_settled_at_run_end_and_a_settled_one_is_not(ledger, monkeypatch):
    captured: list[dict] = []

    async def fake_capture(exc, *, kind, **fields):
        captured.append({"kind": kind, **fields})

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture
    )
    coord = _Coord()
    logger = ToolExecutionLogger()

    # Two rows opened by this run (log_started's INSERT, status 'running').
    turn_ledger.record_row_opened(row_id="tidewell-row", tool_name="agent")
    turn_ledger.record_row_opened(row_id="ares-row", tool_name="agent")
    # Ares's real result is queued: it is no longer open.
    await logger._update_row(
        "ares-row", {"status": "completed", "success": True}, coordinator=coord
    )
    coord.ops.clear()

    settled = await logger.settle_open_rows_at_run_end(
        outcome="completed", conversation_id="c1", request_id="r1", coordinator=coord
    )

    assert settled == 1
    assert [(t, p["id"], o) for t, p, o in coord.ops] == [
        ("chat.tool_call", "tidewell-row", "update")
    ], "only the never-settled row is swept, onto the run's own coordinator"
    payload = coord.ops[0][1]
    assert payload["status"] == "error" and payload["is_error"] is True
    assert payload["error_type"] == "abandoned_at_run_end"
    assert "completed" in payload["error_message"]
    assert [c["kind"] for c in captured] == ["tool_call_settled_at_run_end"]
    assert captured[0]["context"]["row_ids"] == ["tidewell-row"]
    # Idempotent: nothing is left to settle a second time.
    assert await logger.settle_open_rows_at_run_end(outcome="completed", coordinator=coord) == 0


@pytest.mark.asyncio
async def test_a_parked_row_is_not_swept(ledger):
    coord = _Coord()
    logger = ToolExecutionLogger()
    turn_ledger.record_row_opened(row_id="client-tool-row", tool_name="browser_click")
    await logger._update_row(
        "client-tool-row", {"status": "delegated", "is_client_delegated": True}, coordinator=coord
    )
    coord.ops.clear()
    assert await logger.settle_open_rows_at_run_end(outcome="completed", coordinator=coord) == 0
    assert coord.ops == []


def test_the_run_exit_sweeps_before_its_final_commit():
    from matrx_ai.orchestrator import executor

    src = inspect.getsource(executor._finalize_and_persist)
    sweep = src.find("settle_open_rows_at_run_end(")
    final = src.find('finalize(reason="request_final_commit")')
    assert sweep != -1, "_finalize_and_persist must run the run-end sweep"
    assert final != -1
    assert sweep < final, "the sweep must be queued before the run's final commit"

    run_src = inspect.getsource(executor.execute_until_complete)
    backstop = run_src.find("settle_open_rows_at_run_end(")
    close = run_src.find("reset_turn_ledger(ledger_token)")
    assert backstop != -1 and backstop < close, (
        "the ledger's close must run the sweep as a backstop before it forgets the rows"
    )
