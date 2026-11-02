"""A run started with a multi-megabyte input keeps a SMALL ``metadata``, and every reader still gets the value.

2026-10-28, Smart Add offerings (runs 0f6621a7 / 27e48276): children seeded with a ~6 MB ``evidence`` input
held it twice on ``workflow.run`` — ``input`` and ``metadata._settings.input_values``. Every heartbeat, claim
stamp and status merge is a ``jsonb_set`` on ``metadata``, and Postgres rewrites the whole jsonb value each
time: ~200 ms per write on child 319da0a6 vs ~1 ms on a small row (same statement, measured live), and the
run's event writer fell 2-7 s behind (vs 0.06 s on a 65 KB sibling).

The rule now: a large ``input_values`` entry goes into the run's value store (the same rule and store as a
``node_started`` event's ``inputs``); the row keeps a reference; ``RunStore.load`` resolves it, so every
execution leg (queued worker, resume, a parked run's merge) reads exactly the value the run started with.

Red on the old engine: ``metadata`` held the whole 6 MB after ``create`` and after ``merge_metadata``.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

RUN_DEF = "7a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
ORG = "884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f"
SMALL_ROW_BYTES = 64_000


def _evidence() -> dict[str, Any]:
    pages = [{"url": f"https://example.com/p/{i}", "text": f"page {i} " + "lorem ipsum " * 400} for i in range(1200)]
    return {"__kind": "evidence_pack", "pages": pages}


class FakeRunTable:
    """``workflow.run`` for ``RunStore``: create, shallow jsonb merge on update, values()."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}

    def model(self) -> Any:
        table = self

        class _Query:
            def __init__(self, run_id: str) -> None:
                self.run_id = run_id

            def returning(self, *_cols: str) -> _Query:
                return self

            async def update(self, **values: Any) -> Any:
                row = table.rows[self.run_id]
                for key, value in values.items():
                    if type(value).__name__ == "JsonbMerge":
                        value = {**(row.get(key) or {}), **value.value}
                    row[key] = json.loads(json.dumps(value, default=str))
                return [{"id": self.run_id}]

            async def values(self, *_fields: str) -> list[dict[str, Any]]:
                row = table.rows.get(self.run_id)
                return [json.loads(json.dumps(row, default=str))] if row else []

        class _Model:
            @staticmethod
            async def create(**fields: Any) -> None:
                row = dict.fromkeys(
                    ("output", "error", "interrupt_payload", "last_checkpoint_id", "created_at", "completed_at")
                )
                row.update(json.loads(json.dumps(fields, default=str)), steps_executed=0)
                table.rows[fields["id"]] = row

            @staticmethod
            def filter(**kw: Any) -> _Query:
                return _Query(kw["id"])

        return _Model


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch) -> tuple[FakeRunTable, dict[str, Any]]:
    from matrx_graph import knobs
    from matrx_graph.checkpoint import postgres, value_store
    from matrx_graph.db import run_store as module

    table = FakeRunTable()
    model = table.model()
    monkeypatch.setattr(module, "get_model", lambda _name: model)
    monkeypatch.setattr(module, "_run_settings_provider", None)
    monkeypatch.setattr(module, "_run_origin_provider", None)
    monkeypatch.setattr(postgres, "_value_store_available", lambda: True)

    stored: dict[str, Any] = {}

    async def _store(run_id: str, values: dict[str, Any], *, organization_id: str | None = None) -> None:
        stored.update(json.loads(json.dumps(values)))

    async def _load_all(run_id: str, hashes: Any) -> dict[str, Any]:
        from matrx_graph.checkpoint.values import resolve_values

        return {h: resolve_values(stored[h], stored) for h in hashes if h in stored}

    async def _knob() -> int:
        return knobs.STARTING_EVENT_INLINE_VALUE_MAX_BYTES

    monkeypatch.setattr(value_store, "store_run_values", _store)
    monkeypatch.setattr(value_store, "_load_all", _load_all)
    monkeypatch.setattr(knobs, "event_inline_value_max_bytes", _knob)
    return table, stored


def _bytes(value: Any) -> int:
    return len(json.dumps(value, default=str))


@pytest.mark.asyncio
async def test_a_large_input_value_is_kept_off_the_run_row_and_loads_back_whole(wired: Any) -> None:
    from matrx_graph.db.run_store import RunStore

    table, stored = wired
    evidence = _evidence()
    assert _bytes(evidence) > 5_000_000
    inputs = {"evidence": evidence, "read_pages": 3}
    store = RunStore()
    run_id = await store.create(
        definition_id=RUN_DEF,
        definition_hash="h",
        inputs=inputs,
        organization_id=ORG,
        metadata={"_settings": {"input_values": dict(inputs), "test_run_id": RUN_DEF}, "_inputs": {}},
    )

    metadata = table.rows[run_id]["metadata"]
    # The row every heartbeat rewrites is small: the large value is a reference, the small ones stay inline.
    assert _bytes(metadata) < SMALL_ROW_BYTES, _bytes(metadata)
    assert metadata["_settings"]["input_values"]["read_pages"] == 3
    assert metadata["_settings"]["test_run_id"] == RUN_DEF
    assert stored, "the large value must be in the run's value store"

    # Every reader gets exactly what the run started with.
    loaded = await store.load(run_id, resolve_output=False)
    assert loaded is not None
    assert loaded["metadata"]["_settings"]["input_values"] == inputs


@pytest.mark.asyncio
async def test_a_parked_runs_merged_inputs_land_by_reference_too(wired: Any) -> None:
    from matrx_graph.db.run_store import RunStore

    table, _stored = wired
    store = RunStore()
    run_id = await store.create(definition_id=RUN_DEF, definition_hash="h", organization_id=ORG, inputs={})
    evidence = _evidence()

    await store.merge_metadata(run_id, {"_settings": {"input_values": {"evidence": evidence}}, "_inputs": {}})

    assert _bytes(table.rows[run_id]["metadata"]) < SMALL_ROW_BYTES
    loaded = await store.load(run_id, resolve_output=False)
    assert loaded is not None
    assert loaded["metadata"]["_settings"]["input_values"] == {"evidence": evidence}


@pytest.mark.asyncio
async def test_small_input_values_are_untouched(wired: Any) -> None:
    from matrx_graph.db.run_store import RunStore

    table, stored = wired
    store = RunStore()
    settings = {"input_values": {"brand_id": "fa20adeb-0000-4000-8000-000000000000"}}
    run_id = await store.create(
        definition_id=RUN_DEF, definition_hash="h", organization_id=ORG, metadata={"_settings": settings}
    )
    assert table.rows[run_id]["metadata"]["_settings"] == settings
    assert not stored


@pytest.mark.asyncio
async def test_a_run_whose_stored_input_value_is_gone_fails_naming_it_when_executed(wired: Any) -> None:
    """Red before 2026-10-28 (review of 84e644e1): the load logged and handed the run its REFERENCE MARKER as the
    input, so a run could start with ``{"__matrx_checkpoint_value__": …}`` where its evidence should be."""
    from matrx_graph.checkpoint.values import RunInputValueMissingError
    from matrx_graph.db.run_store import RunStore, execution_input_values

    _table, stored = wired
    store = RunStore()
    run_id = await store.create(
        definition_id=RUN_DEF,
        definition_hash="h",
        organization_id=ORG,
        inputs={},
        metadata={"_settings": {"input_values": {"evidence": _evidence(), "read_pages": 3}}},
    )
    loaded = await store.load(run_id, resolve_output=False)
    assert execution_input_values(loaded)["read_pages"] == 3  # whole values execute
    stored.clear()  # the value row is gone

    loaded = await store.load(run_id, resolve_output=False)
    with pytest.raises(RunInputValueMissingError) as caught:
        execution_input_values(loaded)
    assert caught.value.run_id == run_id
    assert "run_input_value_missing" in str(caught.value)


@pytest.mark.parametrize(
    "status",
    ["pending", "running", "errored", "interrupted", "paused", "awaiting_input", "cancelling", "pausing", "failed"],
)
@pytest.mark.asyncio
async def test_a_plain_row_read_never_raises_for_a_gone_input_value(wired: Any, status: str) -> None:
    """Red before this fix (2026-10-28 review): ``load(resolve_output=False)`` — the owner check behind ~33
    endpoints (view / cancel / delete) and the worker's row reads — raised ``RunInputValueMissingError`` for every
    status outside completed/failed/cancelled, so an ERRORED run whose input was gone could not even be cancelled."""
    from matrx_graph.checkpoint.values import REF_KEY
    from matrx_graph.db.run_store import RunStore

    table, stored = wired
    store = RunStore()
    run_id = await store.create(
        definition_id=RUN_DEF,
        definition_hash="h",
        organization_id=ORG,
        inputs={},
        metadata={"_settings": {"input_values": {"evidence": _evidence()}}},
    )
    stored.clear()
    table.rows[run_id]["status"] = status

    row = await store.load(run_id, resolve_output=False)
    assert row is not None and row["status"] == status
    assert REF_KEY in json.dumps(row["metadata"]["_settings"]["input_values"])  # the reference, honestly kept
    assert await store.load(run_id, resolve_output=False, missing="mark") is not None
