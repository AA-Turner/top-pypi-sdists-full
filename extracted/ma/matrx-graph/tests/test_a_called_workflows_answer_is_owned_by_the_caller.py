"""A called workflow's answer is COPIED into its caller's value store at the hand-off — inside the database.

2026-10-28, Smart Add offerings: when a child returned, the caller re-interned the answer into its OWN value
store from Python — ~15.7 MB / ~500 values per hand-off, ~28 s. 84e644e1 skipped those writes and made every
read of the caller fall back to the stores of the runs it called (6 levels deep). Review: the caller then
silently depended on child rows that cascade-delete with the child run or its definition (lost values), a
7th-level value was skipped and never found, and every read paid extra queries.

The rule now: the hand-off copies the child's values into the caller's store with ONE ``INSERT … SELECT``
(no value crosses Python), marks those hashes stored for the caller, and every run reads ONLY its own store.

Red on 84e644e1: after the child is deleted the caller's read lost the value; 8-deep nesting lost the deepest.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

RUNS = [f"{i:08d}-0000-4000-8000-000000000000" for i in range(10)]
PARENT, CHILD, OTHER = RUNS[0], RUNS[1], RUNS[9]
ORG = "884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f"


class FakeStore:
    """``workflow.checkpoint_value`` keyed (run_id, value_hash), plus ``workflow.run`` parentage."""

    def __init__(self) -> None:
        self.values: dict[tuple[str, str], Any] = {}
        self.inserted: list[tuple[str, str]] = []
        self.copies: list[tuple[str, str]] = []

    def delete_run(self, run_id: str) -> None:
        """What a child run's (or its definition's) deletion does to its value rows: they cascade away."""
        for key in [k for k in self.values if k[0] == run_id]:
            del self.values[key]

    def models(self) -> dict[str, Any]:
        store = self

        class _ValueQuery:
            def __init__(self, kw: dict[str, Any]) -> None:
                self.kw = kw

            async def values(self, *fields: str) -> list[dict[str, Any]]:
                # A run reads ONE store: anything but run_id=<one run> is a cross-run read.
                assert set(self.kw) <= {"run_id", "value_hash__in"}, self.kw
                hashes = self.kw.get("value_hash__in")
                return [
                    {"value_hash": h, "value": v}
                    for (r, h), v in store.values.items()
                    if r == self.kw["run_id"] and (hashes is None or h in hashes)
                ]

        class _Value:
            @staticmethod
            def filter(**kw: Any) -> _ValueQuery:
                return _ValueQuery(kw)

            @staticmethod
            async def bulk_insert_ignore(rows: list[dict[str, Any]], **_kw: Any) -> None:
                for row in rows:
                    key = (row["run_id"], row["value_hash"])
                    store.inserted.append(key)
                    store.values.setdefault(key, json.loads(json.dumps(row["value"])))

            @staticmethod
            async def copy_rows_ignore(
                *, where: dict[str, Any], overrides: dict[str, Any], columns: list[str], casts: dict[str, str],
                on_conflict: list[str], returning: str | None = None,
            ) -> list[str]:
                assert set(where) == {"run_id"} and set(overrides) == {"run_id", "organization_id"}
                assert casts == {"run_id": "uuid", "organization_id": "uuid"}
                assert on_conflict == ["run_id", "value_hash"] and returning == "value_hash"
                landed: list[str] = []
                for (r, h), v in list(store.values.items()):
                    if r == where["run_id"] and (overrides["run_id"], h) not in store.values:
                        store.values[(overrides["run_id"], h)] = v
                        store.copies.append((overrides["run_id"], h))
                        landed.append(h)
                return landed

        class _Run:
            @staticmethod
            def filter(**kw: Any) -> Any:
                raise AssertionError(f"a value read must never look up other runs: {kw}")

        return {"WfCheckpointValue": _Value, "WfRun": _Run}


@pytest.fixture
def fake(monkeypatch: pytest.MonkeyPatch) -> FakeStore:
    from matrx_graph.checkpoint import postgres, value_store

    store = FakeStore()
    models = store.models()
    monkeypatch.setattr(value_store, "get_model", lambda name: models[name])
    monkeypatch.setattr(postgres, "_stored_value_hashes", {})

    async def _org(_run_id: str) -> str:
        return ORG

    monkeypatch.setattr(postgres, "_organization_for_run", _org)
    return store


def _big_output(tag: str = "") -> dict[str, Any]:
    return {"__kind": "offering_rows", "rows": [{"name": f"item {tag}{i}", "notes": "x" * 400} for i in range(400)]}


async def _child_ran(run_id: str, output: Any) -> dict[str, Any]:
    """The child's own event / checkpoint interning stored ``output`` in the CHILD's store; returns its ref."""
    from matrx_graph.checkpoint import value_store
    from matrx_graph.checkpoint.values import REF_KEY, intern_values

    child_store: dict[str, Any] = {}
    ref = intern_values(output, child_store, 32_768)
    assert REF_KEY in json.dumps(ref)
    await value_store.store_run_values(run_id, child_store)
    return ref


@pytest.mark.asyncio
async def test_the_caller_owns_the_answer_after_its_child_is_deleted(fake: FakeStore) -> None:
    from matrx_graph.checkpoint import value_store
    from matrx_graph.checkpoint.values import intern_values, referenced_hashes, resolve_values

    output = _big_output()
    ref = await _child_ran(CHILD, output)
    fake.inserted.clear()

    answer = await value_store.carry_run_values(CHILD, PARENT, {"last_outputs": {"rows": ref}})
    assert answer == {"last_outputs": {"rows": output}}
    child_hashes = {h for (r, h) in fake.values if r == CHILD}
    assert {h for (r, h) in fake.copies if r == PARENT} == child_hashes  # copied in the database

    # The caller's own write of the answer (its node_completed event / checkpoint) interns the same subtrees:
    # nothing is re-sent from Python.
    caller_store: dict[str, Any] = {}
    caller_ref = intern_values(answer, caller_store, 32_768)
    await value_store.store_run_values(PARENT, caller_store)
    assert [key for key in fake.inserted if key[1] in child_hashes] == []

    # The child run (or its definition) is deleted: its value rows cascade away. The caller still reads all.
    fake.delete_run(CHILD)
    loaded = await value_store.load_run_values(PARENT, referenced_hashes(caller_ref))
    assert resolve_values(caller_ref, loaded) == answer


@pytest.mark.asyncio
async def test_eight_levels_of_called_workflows_each_owns_its_answer(fake: FakeStore) -> None:
    from matrx_graph.checkpoint import value_store
    from matrx_graph.checkpoint.values import intern_values, referenced_hashes, resolve_values

    chain = RUNS[:9]  # chain[0] calls chain[1] … calls chain[8]: eight hand-offs
    output = _big_output("deep ")
    ref = await _child_ran(chain[-1], output)
    answer: Any = {"last_outputs": {"rows": ref}}
    for depth in range(len(chain) - 1, 0, -1):
        child, caller = chain[depth], chain[depth - 1]
        answer = await value_store.carry_run_values(child, caller, answer)
        # The caller's checkpoint interns the answer and hands its reference upward.
        caller_store: dict[str, Any] = {}
        answer = intern_values(answer, caller_store, 32_768)
        await value_store.store_run_values(caller, caller_store)
    top_ref = answer
    for run_id in chain[1:]:
        fake.delete_run(run_id)
    loaded = await value_store.load_run_values(chain[0], referenced_hashes(top_ref))
    assert resolve_values(top_ref, loaded) == {"last_outputs": {"rows": output}}


@pytest.mark.asyncio
async def test_a_run_reads_only_its_own_store(fake: FakeStore) -> None:
    from matrx_graph.checkpoint import value_store
    from matrx_graph.checkpoint.values import intern_values

    # A value only a run's CHILD stored (no hand-off happened) and one an unrelated run stored: neither is read.
    child_store: dict[str, Any] = {}
    intern_values(_big_output("child "), child_store, 32_768)
    await value_store.store_run_values(CHILD, child_store)
    other_store: dict[str, Any] = {}
    intern_values(_big_output("other "), other_store, 32_768)
    await value_store.store_run_values(OTHER, other_store)

    assert await value_store.load_run_values(PARENT, set(child_store) | set(other_store)) == {}


@pytest.mark.asyncio
async def test_a_failed_copy_costs_only_speed(fake: FakeStore, monkeypatch: pytest.MonkeyPatch) -> None:
    """The copy fails → nothing is marked stored, so the caller's own write keeps every value (slower, never lost)."""
    from matrx_graph.checkpoint import value_store
    from matrx_graph.checkpoint.values import intern_values, referenced_hashes, resolve_values

    output = _big_output()
    ref = await _child_ran(CHILD, output)

    async def _boom(**_kw: Any) -> Any:
        raise RuntimeError("statement timeout")

    models = fake.models()
    models["WfCheckpointValue"].copy_rows_ignore = staticmethod(_boom)
    monkeypatch.setattr(value_store, "get_model", lambda name: models[name])

    answer = await value_store.carry_run_values(CHILD, PARENT, {"last_outputs": {"rows": ref}})
    caller_store: dict[str, Any] = {}
    caller_ref = intern_values(answer, caller_store, 32_768)
    await value_store.store_run_values(PARENT, caller_store)
    fake.delete_run(CHILD)
    loaded = await value_store.load_run_values(PARENT, referenced_hashes(caller_ref))
    assert resolve_values(caller_ref, loaded) == answer
