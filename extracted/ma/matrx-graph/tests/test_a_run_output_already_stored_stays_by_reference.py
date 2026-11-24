"""A run output whose large steps the run's checkpoints ALREADY stored is written by reference, never inline.

L-SPEED round 6l, live 2026-11-10: PBW keyword_synthesis run 89948813 wrote a 9.8 MB ``workflow.run.output``
(its ``done`` gather 17 MB inline) though the knob is 1 MB. ``run_output_row`` turns a step the run already
committed (the process intern cache) into its reference with no walk, so the plan named no NEW value to store, and
``output_by_reference`` read "nothing to store" as "nothing over the limit" and handed back the original output.
That one row cost ~1.4 s to write and ~0.5 s per read of it (the settle hook's, ``finalize.reload``).
Red without the change: the terminal write carries the whole ~20 MB output (the fake table times it out)."""

from __future__ import annotations

import json


from matrx_graph.checkpoint import postgres, value_store, values
from matrx_graph.types.primitives import RunStatus

from .test_a_large_run_result_is_kept_by_reference import RUN, _big_output, wired  # noqa: F401 — the fixture


async def test_a_step_the_run_already_stored_is_written_by_reference(wired, monkeypatch) -> None:  # noqa: F811
    from matrx_graph import knobs
    from matrx_graph.db.run_store import RunStore

    table, stored = wired
    output = _big_output()
    limit, piece = 1_048_576, await knobs.interning_grain()
    values.clear_interned_cache()
    # What the run's checkpoints did: interned the same live values (the process cache) and committed them.
    _row, earlier, _sizes = value_store._run_output_plan(output, limit, piece, frozenset())
    assert earlier, "the big step was interned"
    stored.update(json.loads(json.dumps(earlier)))
    monkeypatch.setitem(postgres._stored_value_hashes, RUN, frozenset(earlier))

    applied = await RunStore().apply_result(
        RUN, status=RunStatus.COMPLETED, steps_executed=59, output=output,
        interrupt=None, error=None, last_checkpoint_id=None,
    )  # fmt: skip

    assert applied is True and table.rows[RUN]["status"] == "completed", table.rows[RUN].get("error")
    assert max(table.output_writes) <= limit, table.output_writes
    loaded = await RunStore().load(RUN)
    assert loaded is not None and loaded["output"] == output, "the row still reads back whole"
