"""A save of several outcomes lands exactly as the same outcomes saved one at a time (review 6h, I3).

The real-Postgres proof is ``tests/package_host_contracts/test_a_bulk_outcome_rewrite_clears_like_the_single_one.py``
(skipped without the local database). This file pins the two rules in the suite: every nullable column with no
default that a row supplies as None is cleared (``clear_when_empty``) — what the single upsert's ``EXCLUDED`` gives —
and a key repeated within one save lands outcome by outcome, in order. Red before: no ``clear_when_empty`` was
passed, and a repeated key was collapsed into one statement in shape order.
"""

from __future__ import annotations

import datetime
from typing import Any

from matrx_graph.checkpoint import postgres as P

UPDATE = ["output", "channel_writes", "sends", "emissions", "duration_ms", "error", "source", "completed_at",
          "output_kind", "output_kind_ok", "output_kind_errors"]


class _Field:
    def __init__(self, nullable: bool, default: Any = None) -> None:
        self.nullable, self.default = nullable, default


class _Model:
    _fields = {
        "output": _Field(False, {}), "channel_writes": _Field(False, []), "sends": _Field(False, []),
        "emissions": _Field(False, {}), "duration_ms": _Field(False, 0), "error": _Field(True),
        "source": _Field(False, "executor"), "completed_at": _Field(False), "output_kind": _Field(True),
        "output_kind_ok": _Field(True), "output_kind_errors": _Field(True),
    }
    calls: list[dict[str, Any]] = []

    @classmethod
    async def bulk_upsert(cls, rows: list[dict[str, Any]], **kw: Any) -> list[Any]:
        cls.calls.append({"rows": rows, **kw})
        return []


def _prepared(node: str, written: list[str], attempt: int = 1) -> P._PreparedOutcome:
    row = {"run_id": "r", "step": 1, "node_id": node, "attempt": attempt, "dispatch_id": "", "item_index": 0,
           "output": {"x": 1}, "channel_writes": [], "sends": [], "emissions": {}, "duration_ms": 1, "error": None,
           "source": "executor", "completed_at": datetime.datetime.now(datetime.UTC), "output_kind": None,
           "output_kind_ok": None, "output_kind_errors": None}
    prepared = P._PreparedOutcome(run_id="r", organization_id="o", row=row, update_fields=list(UPDATE), fresh={},
                                  inline_payload={})

    async def write(values: dict[str, Any]) -> None:
        written.append(values["node_id"] + ":" + str(values["output"]))

    object.__setattr__(prepared, "write", write)
    return prepared


async def test_a_batch_clears_every_nullable_column_a_row_leaves_empty(monkeypatch) -> None:
    _Model.calls = []
    monkeypatch.setattr(P, "get_model", lambda name: _Model)
    await P._write_outcomes_together([_prepared("a", []), _prepared("b", [])])
    assert len(_Model.calls) == 1
    assert set(_Model.calls[0]["clear_when_empty"]) == {"error", "output_kind", "output_kind_ok", "output_kind_errors"}


async def test_a_repeated_key_lands_one_outcome_at_a_time_in_order(monkeypatch) -> None:
    _Model.calls = []
    monkeypatch.setattr(P, "get_model", lambda name: _Model)
    written: list[str] = []
    first, second = _prepared("a", written), _prepared("a", written)
    second.row["output"] = {"x": 2}
    await P._write_outcomes_together([first, _prepared("b", written), second])
    assert _Model.calls == [] and written == ["a:{'x': 1}", "b:{'x': 1}", "a:{'x': 2}"]
