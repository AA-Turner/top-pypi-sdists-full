"""A ``workflow.run`` UPDATE hands back only the columns its caller reads — never ``RETURNING *``.

2026-10-28, Smart Add offerings (parent 0f6621a7): each child unit is seeded with a ~6 MB
``evidence`` input, held TWICE on its run row (``input`` + ``metadata._settings.input_values``).
Every event (seq bump), checkpoint (``last_checkpoint_id``) and ``steps_executed`` write was an
``update_where`` → ``RETURNING *``, so each shipped and decoded ~12 MB it never read (measured:
~1.0 s for the whole row vs ~0.16 s for two columns). A 5 ms step cost 0.5–3 s; a 10-step unit ~30 s.

The guard reads the source of the writers that run once PER STEP or PER EVENT (the event store,
the checkpointer, ``RunStore.merge_metadata``): none says
``update_where`` (RETURNING *); they name their columns (``run_store.update_run`` or
``.returning(...)``). The host's per-checkpoint ``steps_executed`` check is a host contract
(tests/package_host_contracts/test_matrx_graph_host.py). The once-per-run status writers (``mark_*``,
``transition``) still return the row; they cost one fat read per transition, not per step.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "matrx_graph"

_WHOLE_ROW_UPDATE = re.compile(r'get_model\(\s*"WfRun"\s*\)\s*\.update_where\(|wf_run\.update_where\(')


def _offenders(text: str) -> list[int]:
    return [text.count("\n", 0, m.start()) + 1 for m in _WHOLE_ROW_UPDATE.finditer(text)]


def _per_step_sources() -> dict[str, str]:
    run_store = (ENGINE / "db" / "run_store.py").read_text(encoding="utf-8")
    out = {
        "db/event_store.py": (ENGINE / "db" / "event_store.py").read_text(encoding="utf-8"),
        "checkpoint/postgres.py": (ENGINE / "checkpoint" / "postgres.py").read_text(encoding="utf-8"),
    }
    for fn in ("merge_metadata",):
        body = run_store.split(f"async def {fn}(", 1)[1].split("\n    async def ", 1)[0]
        out[f"db/run_store.py::{fn}"] = body
    return out


def test_no_per_step_run_update_returns_the_whole_row() -> None:
    found = {where: lines for where, text in _per_step_sources().items() if (lines := _offenders(text))}
    assert not found, (
        "a per-step workflow.run UPDATE says RETURNING * (the whole, possibly multi-MB row) — "
        f"use matrx_graph.db.run_store.update_run(...) or .returning(...): {found}"
    )


def test_the_guard_can_fail() -> None:
    assert _offenders('x = await get_model("WfRun").update_where({"id": r}, steps_executed=1)') == [1]
    assert _offenders("await wf_run.update_where({'id': r}, last_checkpoint_id=c)") == [1]
    assert _offenders('await update_run({"id": r}, steps_executed=1)') == []


@pytest.mark.asyncio
async def test_update_run_names_its_returning_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_graph.db import run_store

    seen: dict[str, object] = {}

    class _Builder:
        def returning(self, *cols: str) -> _Builder:
            seen["returning"] = cols
            return self

        async def update(self, **updates: object) -> str:
            seen["updates"] = updates
            return "ok"

    class _Model:
        @staticmethod
        def filter(**filters: object) -> _Builder:
            seen["filters"] = filters
            return _Builder()

    monkeypatch.setattr(run_store, "get_model", lambda name: _Model)
    assert await run_store.update_run({"id": "r"}, steps_executed=3) == "ok"
    assert seen["returning"] == ("id",) and seen["updates"] == {"steps_executed": 3}
    await run_store.update_run({"id": "r"}, returning=("id", "event_seq"), event_seq=1)
    assert seen["returning"] == ("id", "event_seq")
