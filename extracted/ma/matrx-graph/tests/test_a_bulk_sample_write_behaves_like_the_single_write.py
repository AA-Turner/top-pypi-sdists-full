"""A run's bulk sample write sets every slot exactly as the single write does (review 2026-11-10, finding 4).

``adopt_live_outputs`` sends one ``bulk_upsert`` for a run's samples. matrx-orm renders
``col = COALESCE(EXCLUDED.col, t.col)`` for a column not present in every row, so a step whose sample has
no output kind KEPT the stale kind already stored, where the single write cleared it to NULL. And one bad
row failed every step's sample while adoption still reported ``len(writes)``.

The guards run the REAL matrx-orm statement builder (only the database call is stubbed):
- a row with no output kind is written ``output_kind = EXCLUDED.output_kind`` (NULL), never COALESCEd;
- a failing bulk statement falls back to one write per sample, and the count is what actually landed.
"""

from __future__ import annotations

import re
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.db.node_data_slot_store import NodeDataSlotStore
from matrx_graph.db.standalone import build_standalone_models

from .test_a_large_step_result_reaches_only_when_whole import _Outcomes


def _outcome(run_id: str, node_id: str, output: Any, output_kind: str | None) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "node_id": node_id,
        "step": 0,
        "attempt": 1,
        "error": None,
        "source": "executor",
        "output": output,
        "emissions": {},
        "output_kind": output_kind,
    }


def _wire(
    monkeypatch: pytest.MonkeyPatch, outcomes: list[dict[str, Any]], *, fail_bulk: bool = False
) -> tuple[list[str], list[str]]:
    """Real slot model + real statement builder; returns (bulk SQL sent, node ids written one at a time)."""
    slot_model = build_standalone_models("slot_bulk_parity_test")["WfNodeDataSlot"]
    import matrx_graph.db._registry as registry

    monkeypatch.setattr(
        registry,
        "get_model",
        lambda key: {"WfNodeOutcome": _Outcomes(outcomes), "WfCheckpointValue": _Outcomes([])}.get(
            key, slot_model
        ),
    )

    sent: list[str] = []
    from matrx_orm.query import builder as builder_mod
    from matrx_orm.query import executor as executor_mod

    class _DB:
        async def execute_write(self, sql: str, *params: Any, **_options: Any) -> list[dict[str, Any]]:
            sent.append(sql)
            if fail_bulk:
                raise RuntimeError("one bad row")
            rows = sql.count("), (") + 1
            return [{"id": str(uuid4())} for _ in range(rows)]

    def _init(self: Any, query: dict[str, Any]) -> None:
        self.query = query
        self.model = query.get("model")
        self.db = _DB()

    async def _no_dict(self: Any, _q: dict[str, Any]) -> Any:
        return NotImplemented

    monkeypatch.setattr(executor_mod.QueryExecutor, "__init__", _init)
    monkeypatch.setattr(executor_mod.QueryExecutor, "_try_write_dict", _no_dict)
    monkeypatch.setattr(executor_mod.QueryExecutor, "_guard_writable", lambda self, _op: None)
    monkeypatch.setattr(executor_mod.QueryExecutor, "_make", lambda self, row: row)
    monkeypatch.setattr(
        builder_mod.QueryBuilder,
        "_build_query",
        lambda self: {"table": "workflow.node_data_slot", "model": self.model},
    )

    singles: list[str] = []
    import matrx_orm.operations.conflict_writes as conflict_writes

    async def _single(_model: Any, data: dict[str, Any], **_kw: Any) -> dict[str, Any]:
        singles.append(data["node_id"])
        if data["node_id"] == "bad":
            raise RuntimeError("one bad row")
        return {"id": uuid4()}

    monkeypatch.setattr(conflict_writes, "upsert_with_conflict", _single)
    return sent, singles


def _assignment(sql: str, col: str) -> str:
    match = re.search(rf"\b{col} = (COALESCE\(EXCLUDED\.{col}, [^)]*\)|EXCLUDED\.{col})", sql)
    assert match, f"{col} is not set on conflict: {sql}"
    return match.group(1)


@pytest.mark.asyncio
async def test_a_sample_with_no_output_kind_clears_the_stored_kind(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    sent, singles = _wire(
        monkeypatch,
        [_outcome(run_id, "a", {"n": 1}, "news_article"), _outcome(run_id, "b", {"n": 2}, None)],
    )
    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )
    assert adopted == 2
    assert singles == []
    assert len(sent) == 1
    for col in ("output_kind", "captured_by", "value", "emissions", "source"):
        assert _assignment(sent[0], col) == f"EXCLUDED.{col}", (
            f"{col} is COALESCEd: a sample without it keeps the stale stored value"
        )


@pytest.mark.asyncio
async def test_one_bad_row_never_costs_the_other_samples(monkeypatch: pytest.MonkeyPatch) -> None:
    run_id = str(uuid4())
    _sent, singles = _wire(
        monkeypatch,
        [
            _outcome(run_id, "a", {"n": 1}, None),
            _outcome(run_id, "bad", {"n": 2}, None),
            _outcome(run_id, "c", {"n": 3}, None),
        ],
        fail_bulk=True,
    )
    adopted = await NodeDataSlotStore().adopt_live_outputs(
        run_id=run_id, definition_id=str(uuid4()), user_id=str(uuid4())
    )
    assert sorted(singles) == ["a", "bad", "c"], "a failed bulk write falls back to one write per sample"
    assert adopted == 2, "the count is what actually landed, never len(writes)"
