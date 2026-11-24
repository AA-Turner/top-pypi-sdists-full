"""A chain of steps saved together hashes each step's output ONCE, though it is also the next step's input.

2026-11-07 (L-SPEED round 4, research pick child): a pure-step chain lands as one save, and every
outcome row splits its large ``output`` and ``input`` into the run's value store on its own — so a
step's output was serialized and hashed as that step's output, then again as the next step's input,
and each split first serialized the whole value only to measure it. On the child's real 15.6 MB of
step outputs the chain's interning cost 822 ms CPU (laptop; ~2.75x on the server); with the outcomes
of one save sharing one ``InternMemo`` and the split sized by its own walk, 465 ms.

Red before the fix: ``save_checkpoint_chain`` prepared each outcome with no memo, so the chain hashed
every output twice.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from matrx_graph.checkpoint import postgres as pg
from matrx_graph.checkpoint import values as values_module
from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome
from matrx_graph.checkpoint.values import outcome_input_row, referenced_hashes, resolve_values

LIMIT = 32768
STEPS = 6


class _HashedBytes:
    def __init__(self) -> None:
        self.total = 0

    def sha256(self, data: bytes = b"") -> Any:
        self.total += len(data)
        return hashlib.sha256(data)


def _rows(step: int) -> list[dict[str, Any]]:
    return [{"source": f"s{step}_{i}", "body": "x" * 9000, "score": i} for i in range(120)]


def _chain() -> list[tuple[Checkpoint, list[NodeOutcome]]]:
    """Each step's output object is the next step's input — exactly as the scheduler delivers it."""
    items, previous = [], None
    for step in range(STEPS):
        output = {"rows": _rows(step)}
        outcome = NodeOutcome(
            run_id="run-1", step=step, node_id=f"n{step}", attempt=1, output=output,
            inputs={"rows": previous["rows"]} if previous else None,
        )
        items.append((Checkpoint(run_id="run-1", thread_id="t", checkpoint_id=f"cp{step}", step=step, channel_values={}), [outcome]))
        previous = output
    return items


def _json(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


async def _prepared_by_the_chain_save(monkeypatch) -> tuple[list[Any], int]:
    async def org(_run_id: str) -> str:
        return "org-1"

    async def limit() -> int:
        return LIMIT

    captured: dict[str, Any] = {}

    async def save_checkpoint(self, checkpoint, *, _outcomes=None, _earlier=()):  # noqa: ANN001
        captured["outcomes"] = [o for _cp, outs in _earlier for o in outs] + list(_outcomes or ())

    monkeypatch.setattr(pg, "_organization_for_run", org)
    monkeypatch.setattr(pg, "_available_versioned_kind_columns", lambda: ())
    monkeypatch.setattr(pg, "_available_input_envelope_columns", lambda: ("input",))
    monkeypatch.setattr(pg, "_value_store_available", lambda: True)
    monkeypatch.setattr("matrx_graph.knobs.event_inline_value_max_bytes", limit)
    monkeypatch.setattr(pg.PostgresCheckpointer, "save_checkpoint", save_checkpoint)
    hashed = _HashedBytes()
    monkeypatch.setattr(values_module, "hashlib", hashed)
    await pg.PostgresCheckpointer().save_checkpoint_chain(_chain())
    return captured["outcomes"], hashed.total


async def test_a_chain_save_hashes_each_step_output_once(monkeypatch) -> None:
    prepared, chain_bytes = await _prepared_by_the_chain_save(monkeypatch)
    one_output = len(json.dumps(_rows(0), sort_keys=True, separators=(",", ":")).encode())

    # Each of the STEPS outputs is hashed once (its rows list is one value over the limit); the
    # inputs of steps 1.. are the same objects and cost nothing more.
    assert chain_bytes < one_output * (STEPS + 1), (
        f"the chain hashed {chain_bytes:,} bytes for {STEPS} outputs of {one_output:,} — each output must be "
        "hashed once per save, not again as the next step's input"
    )
    store: dict[str, Any] = {}
    for p in prepared:
        store.update(p.fresh)
    store = _json(store)
    for p, (_cp, [outcome]) in zip(prepared, _chain(), strict=True):
        assert referenced_hashes(p.row["output"]) <= set(store)
        assert resolve_values(_json(p.row["output"]), store) == _json(outcome.output)
        if outcome.inputs is not None:
            assert resolve_values(_json(p.row["input"]), store) == _json(outcome.inputs)


def test_the_split_matches_the_one_value_at_a_time_form() -> None:
    """Sized by its own walk, the split keeps small values whole and the same references for large ones."""
    small = {"a": 1, "b": "x" * 100}
    assert outcome_input_row(small, LIMIT) == (small, {})
    big = {"rows": _rows(1), "note": "kept inline"}
    row, store = outcome_input_row(big, LIMIT)
    assert row["note"] == "kept inline" and referenced_hashes(row["rows"])
    assert resolve_values(_json(row), _json(store)) == _json(big)
    flat, flat_store = outcome_input_row(_rows(2), LIMIT)
    assert referenced_hashes(flat) and resolve_values(_json(flat), _json(flat_store)) == _json(_rows(2))
