"""A run whose final write fails ends FAILED, never "running" forever.

2026-10-05: run 70601b15 finished all 19 steps; its 11 MB completion write timed out; every caller of
``RunStore.apply_result`` only logged the error, so the run read "running" with no end. The terminal
write now falls back to a small FAILED write naming what failed, then re-raises for the caller.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.types.primitives import RunStatus

RUN = "6f1e2d3c-4b5a-4968-8776-655443322111"


async def test_a_timed_out_completion_write_ends_the_run_failed(monkeypatch) -> None:
    from matrx_graph.db import run_store as module
    from matrx_graph.db.run_store import RunStore

    writes: list[dict[str, Any]] = []

    class _Result:
        rows_affected = 1
        updated_rows: list = []

    class _Model:
        @staticmethod
        async def update_where(filters, **values):
            if values.get("status") == "completed":
                raise TimeoutError("statement timeout writing an 11 MB output")
            writes.append(values)
            return _Result()

    monkeypatch.setattr(module, "get_model", lambda _name: _Model)
    with pytest.raises(TimeoutError):
        await RunStore().apply_result(
            RUN, status=RunStatus.COMPLETED, steps_executed=19, output={"deliver": {"x": 1}},
            interrupt=None, error=None, last_checkpoint_id=None,
        )
    assert writes and writes[-1]["status"] == "failed", writes
    error = writes[-1]["error"]
    assert error.get("cause") == "final_write_failed", error
    assert "output" not in writes[-1], "the fallback must not carry the payload that failed"


async def test_a_failing_runs_failed_final_write_still_ends_the_row_failed(monkeypatch) -> None:
    """A run that ends FAILED and whose own failure write raises must not stay "running" either
    (2026-10-27 review: the FAILED path re-raised before the fallback, so a failing child whose write
    timed out read "running" forever). The fallback keeps the cause the run meant to end with."""
    from matrx_graph.db import run_store as module
    from matrx_graph.db.run_store import RunStore
    from matrx_graph.failure import RunFailure

    writes: list[dict[str, Any]] = []
    calls = {"n": 0}

    class _Result:
        rows_affected = 1
        updated_rows: list = []

    class _Model:
        @staticmethod
        async def update_where(filters, **values):
            calls["n"] += 1
            if calls["n"] == 1:
                raise TimeoutError("statement timeout writing the failed run's row")
            writes.append(values)
            return _Result()

    monkeypatch.setattr(module, "get_model", lambda _name: _Model)
    with pytest.raises(TimeoutError):
        await RunStore().apply_result(
            RUN, status=RunStatus.FAILED, steps_executed=4, output={"deliver": {"x": 1}},
            interrupt=None, error="usage limit", last_checkpoint_id=None,
            failure=RunFailure(cause="usage_limit_reached", message="usage limit reached"),
        )
    assert writes and writes[-1]["status"] == "failed", writes
    error = writes[-1]["error"]
    assert error.get("cause") == "final_write_failed", error
    assert error.get("intended_cause") == "usage_limit_reached", error
    assert "output" not in writes[-1], "the fallback must not carry the payload that failed"


async def test_the_fallback_never_overwrites_a_row_that_already_says_why_it_failed(monkeypatch) -> None:
    from matrx_graph.db import run_store as module
    from matrx_graph.db.run_store import RunStore
    from matrx_graph.failure import RunFailure

    writes: list[dict[str, Any]] = []

    class _Query:
        async def values(self, *_fields):
            return [{"status": "failed", "error": {"cause": "usage_limit_reached"}}]

    class _Model:
        @staticmethod
        async def update_where(filters, **values):
            if not writes and values.get("status") == "failed" and "intended_cause" not in (values.get("error") or {}):
                writes.append({"first": True})
                raise TimeoutError("the discard of queued jobs timed out after the row landed")
            writes.append(values)

        @staticmethod
        def filter(**_kw):
            return _Query()

    monkeypatch.setattr(module, "get_model", lambda _name: _Model)
    with pytest.raises(TimeoutError):
        await RunStore().apply_result(
            RUN, status=RunStatus.FAILED, steps_executed=4, output=None, interrupt=None,
            error="usage limit", last_checkpoint_id=None,
            failure=RunFailure(cause="usage_limit_reached", message="usage limit reached"),
        )
    assert not [w for w in writes if (w.get("error") or {}).get("cause") == "final_write_failed"], writes
