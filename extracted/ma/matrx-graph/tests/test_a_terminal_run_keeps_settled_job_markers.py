"""A run reaching a terminal state must not rewrite a job that already settled.

THE USE CASE: a workflow parks (its start job succeeded when it parked), a later wake job finishes it, and the run
completes. ``discard_for_run`` then sweeps the run's unclaimed rows: the parked start job must still read
"succeeded", never "dead letter", while a row that never ran is marked dead letter as before.

THE DOUBLE: the ``WfJob`` table as in-memory rows with the ORM's ``filter().values()`` / ``update_where`` shape.
``discard_for_run`` itself is real.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_graph.workers import queue


class _Table:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows

    def filter(self, **f):  # noqa: ANN003
        hits = [r for r in self.rows if r["run_id"] == f["run_id"] and r["claimed_at"] is None]

        class _Q:
            async def values(_self, *cols):  # noqa: ANN001, N805
                return [{c: r[c] for c in cols} for r in hits]

        return _Q()

    async def update_where(self, filters: dict, **updates):  # noqa: ANN003
        n = 0
        for r in self.rows:
            hit = r["id"] in filters["id__in"] if "id__in" in filters else r["run_id"] == filters["run_id"]
            if hit and r["claimed_at"] is None:
                r.update(updates)
                n += 1
        return SimpleNamespace(rows_affected=n)


@pytest.mark.asyncio
async def test_a_succeeded_job_keeps_its_marker_and_an_unrun_job_is_dead_lettered(monkeypatch):
    run = str(uuid4())
    succeeded = {"id": str(uuid4()), "run_id": run, "claimed_at": None,
                 "last_error": {"queue_state": "succeeded", "type": "terminal_success"}}
    never_ran = {"id": str(uuid4()), "run_id": run, "claimed_at": None, "last_error": None}
    other = {"id": str(uuid4()), "run_id": str(uuid4()), "claimed_at": None, "last_error": None}
    table = _Table([succeeded, never_ran, other])
    monkeypatch.setattr("matrx_graph.db._registry.get_model", lambda name: table)

    assert await queue.discard_for_run(run) == 1
    assert succeeded["last_error"] == {"queue_state": "succeeded", "type": "terminal_success"}
    assert never_ran["last_error"]["queue_state"] == "dead_letter"
    assert other["last_error"] is None
