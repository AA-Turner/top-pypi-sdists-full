"""Every run ending goes through THE terminal write, which hands back only the columns the hooks read
(review 2026-11-10, findings 5 and 6).

5. ``_write_terminal`` said ``RETURNING *``: the run's whole ``input`` (~6 MB on a large start) was shipped and
   decoded inside the terminal write, the 2026-11-02 whole-row class. It now names every column but ``input``,
   and the row handed to the settle hook has no ``input`` key (so a reader can tell "not returned").
   A completion write that LANDED and then raised (a timeout reading its answer back) is never turned into a
   failed run by the fallback: the failed write is guarded against a completed row.
6. A terminal job failure ended its run with a bare ``transition()`` plus a separate announce; it now goes
   through the terminal write (sanitized error, ``completed_at``, the settle hook gets the row).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.types.primitives import RunStatus

RUN = "6f1e2d3c-4b5a-4968-8776-655443322111"

_COLUMNS = (
    "id thread_id parent_run_id definition_id definition_version_id definition_hash status input output error "
    "interrupt_payload steps_executed last_checkpoint_id created_by organization_id deleted_at project_id task_id "
    "conversation_id agent_id agent_version_id metadata created_at started_at completed_at"
).split()


class _Result:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows_affected = len(rows)
        self.updated_rows = rows


class _Runs:
    """One workflow.run row; update_where honors status filters and RETURNING like Postgres."""

    _fields = {name: None for name in _COLUMNS}

    def __init__(self, status: str) -> None:
        self.row: dict[str, Any] = {name: None for name in _COLUMNS}
        self.row.update(id=RUN, thread_id=RUN, definition_id=RUN, status=status, steps_executed=0,
                        input={"big": "x" * 1000}, metadata={})  # fmt: skip
        self.returning: list[Any] = []
        self.fail_after_landing = False

    async def update_where(self, filters: dict[str, Any], *, returning: Any = None, **values: Any) -> _Result:
        status = self.row["status"]
        if "status__in" in filters and status not in filters["status__in"]:
            return _Result([])
        if "status__not_in" in filters and status in filters["status__not_in"]:
            return _Result([])
        self.returning.append(returning)
        self.row.update({k: v for k, v in values.items() if k in self.row and not hasattr(v, "field")})
        if self.fail_after_landing:
            self.fail_after_landing = False
            raise TimeoutError("timed out reading the completed row back")
        cols = list(self.row) if returning is None else list(returning)
        return _Result([{c: self.row[c] for c in cols}])

    def filter(self, **_kw: Any) -> Any:
        row = self.row

        class _Q:
            async def values(self, *cols: str) -> list[dict[str, Any]]:
                return [{c: row.get(c) for c in cols}] if cols else [dict(row)]

        return _Q()


@pytest.fixture
def runs(monkeypatch: pytest.MonkeyPatch) -> tuple[_Runs, list[dict[str, Any]]]:
    from matrx_graph.db import run_store as module

    model = _Runs("running")
    monkeypatch.setattr(module, "get_model", lambda _name: model)
    settled: list[dict[str, Any]] = []

    async def _hook(run_id: str, status: str, cancel_reason: str | None = None, *, row: Any = None) -> None:
        settled.append({"status": status, "row": row})

    module.configure_run_settled(_hook)
    yield model, settled
    module.configure_run_settled(None)


async def test_the_terminal_write_never_hands_back_the_runs_input(runs) -> None:
    from matrx_graph.db.run_store import RunStore

    model, settled = runs
    await RunStore().mark_cancelled(RUN, steps_executed=3)
    assert model.returning and model.returning[-1] is not None, "RETURNING * decodes the whole row"
    assert "input" not in model.returning[-1]
    assert {"status", "output", "metadata", "error", "created_by"} <= set(model.returning[-1])
    assert settled and settled[-1]["row"] is not None
    assert "input" not in settled[-1]["row"], "a row without input must say so (no key), never input=None"


async def test_a_terminal_job_failure_ends_its_run_through_the_terminal_write(runs) -> None:
    from matrx_graph.workers.queue import Job
    from matrx_graph.workers.runner import settle_run_after_terminal_failure

    model, settled = runs
    job = Job(job_id="00000000-0000-0000-0000-0000000000a1", run_id=RUN, kind="start", attempt=1, claimed_by="w")
    assert await settle_run_after_terminal_failure(job, ValueError("gone"), reason="definition_missing")
    assert model.row["status"] == "failed"
    assert model.row["completed_at"] is not None, "every ending stamps when it ended"
    assert model.row["error"]["cause"] == "terminal_job_failure"
    assert settled and settled[-1]["status"] == "failed"
    assert settled[-1]["row"] is not None, "the settle hook gets the row the terminal write left"


async def test_a_completion_that_landed_then_timed_out_stays_completed(runs) -> None:
    from matrx_graph.db.run_store import RunStore

    model, _settled = runs
    model.fail_after_landing = True
    with pytest.raises(TimeoutError):
        await RunStore().apply_result(
            RUN, status=RunStatus.COMPLETED, steps_executed=5, output=None, interrupt=None, error=None,
            last_checkpoint_id=None,
        )  # fmt: skip
    assert model.row["status"] == "completed", "the fallback must never fail a run whose completion landed"
    assert (model.row["error"] or {}).get("cause") != "final_write_failed"


async def test_a_terminal_job_failure_never_overwrites_a_settled_run(runs) -> None:
    from matrx_graph.workers.queue import Job
    from matrx_graph.workers.runner import settle_run_after_terminal_failure

    model, settled = runs
    model.row["status"] = "errored"
    job = Job(job_id="00000000-0000-0000-0000-0000000000a1", run_id=RUN, kind="start", attempt=1, claimed_by="w")
    assert not await settle_run_after_terminal_failure(job, ValueError("gone"), reason="definition_missing")
    assert model.row["status"] == "errored" and settled == []
