"""A step's input record (node_started ``inputs``, the outcome's ``input``) names the DELIVERED objects.

2026-11-09 (L-SPEED round 4, Brand pick): the record was the inputs model's fresh dump, a stranger to the
run's interned-value cache, so a 597-source list read by nine steps was walked and hashed nine more times
(about two thirds of the run's interning CPU in a local profile). An argument that came through unchanged is
now the delivered object itself (the upstream step's settled output), so its interning is a cache hit.

Red before: ``_parse_step_inputs`` returned the dump, and interning the record hashed the whole list again.
"""

from __future__ import annotations

import hashlib
from typing import Any

from pydantic import BaseModel

from matrx_graph.checkpoint import values as values_module
from matrx_graph.checkpoint.values import InternMemo, clear_interned_cache, outcome_input_row
from matrx_graph.executor.scheduler import _parse_step_inputs

LIMIT = 32768


class _In(BaseModel):
    rows: list[dict[str, Any]] = []
    count: float = 0.0


def _rows() -> list[dict[str, Any]]:
    return [{"source": f"s{i}", "body": "x" * 2000, "score": i} for i in range(60)]


def test_an_unchanged_argument_is_the_delivered_object() -> None:
    delivered = {"rows": _rows(), "count": 3}
    _model, error, record = _parse_step_inputs(_In, dict(delivered), "ctx", delivered)
    assert error is None
    assert record["rows"] is delivered["rows"]
    # A scalar keeps the model's own form (int → float here).
    assert record["count"] == 3.0 and isinstance(record["count"], float)


def test_a_changed_argument_keeps_the_models_copy() -> None:
    _model, _error, record = _parse_step_inputs(_In, {"rows": [{"a": 1}]}, "ctx", {"rows": [{"a": 2}]})
    assert record["rows"] == [{"a": 1}]


def test_the_record_of_a_delivered_output_hashes_nothing_new(monkeypatch) -> None:
    monkeypatch.setattr(values_module, "VERIFY_INTERNED_VALUES", False)
    clear_interned_cache()
    output = {"rows": _rows()}
    _row, stored = outcome_input_row(output, LIMIT, InternMemo(frozenset()))  # the upstream step's output
    committed = set(stored)
    hashed = {"n": 0}

    class _Counting:
        def sha256(self, data: bytes = b"") -> Any:
            hashed["n"] += len(data)
            return hashlib.sha256(data)

    monkeypatch.setattr(values_module, "hashlib", _Counting())
    # The scheduler hands the model a rebuilt copy (``_gate_step_inputs``); the record must still be the original.
    copy = {"rows": [dict(r) for r in output["rows"]]}
    _model, _error, record = _parse_step_inputs(_In, copy, "ctx", {"rows": output["rows"]})
    outcome_input_row(record, LIMIT, InternMemo(committed))
    assert hashed["n"] == 0, f"the step's input record hashed {hashed['n']:,} bytes of a value already stored"
