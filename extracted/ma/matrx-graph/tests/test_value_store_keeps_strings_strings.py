"""A string stored in the run's value store reads back as that string (2026-10-27, run 63940e91).

The ORM's jsonb field parses any ``str`` that is valid JSON — on assignment and again on bind — so a
long agent ``final_text`` holding a JSON answer was stored as a JSON OBJECT. Run once per key then
found the saved result no longer fit ``final_text: str`` and re-ran (and paid for) that item on every
rerun. These tests drive the REAL matrx-orm row preparation (``_prep_rows`` on the standalone
``WfCheckpointValue`` model) and decode the bound text the way Postgres does, so they fail on the old
write path and pass only when what goes in is what comes out. Reads go through the REAL
``QueryExecutor._decode_row_dict`` (what ``.values()`` runs on every row after the driver's jsonb
codec decoded it), which used to re-parse a decoded string — so the read side is pinned too.
"""

from __future__ import annotations

import importlib.util
import json
import uuid
from typing import Any

import pytest

pytestmark = pytest.mark.skipif(importlib.util.find_spec("matrx_orm") is None, reason="needs matrx-orm")

# A JSON answer, a plain sentence, JSON scalars, and an empty string — each must survive as a str.
STRINGS = [
    json.dumps({"room": "self_description", "claims": [{"id": "c1", "claim": "Says it is family run"}]}),
    # A long agent answer that is JSON text (the run-once-per-key case): far past any inline limit.
    json.dumps({"room": "self_description", "claims": [{"id": f"c{i}", "claim": "y" * 300} for i in range(60)]}),
    "Plain words, not JSON at all.",
    "123",
    "true",
    "null",
    "",
]


class _PostgresLikeValueTable:
    """Stands in for workflow.checkpoint_value: rows go through matrx-orm's real per-field prep, and
    the bound jsonb text is decoded exactly as Postgres would (json.loads); reads hand the decoded
    value back the way the driver's jsonb codec does."""

    def __init__(self) -> None:
        from matrx_graph.db.standalone import build_standalone_models

        self.model = build_standalone_models("value_store_strings_test")["WfCheckpointValue"]
        self.rows: dict[tuple[str, str], Any] = {}

    async def bulk_insert_ignore(self, rows: list[dict[str, Any]], on_conflict: list[str]) -> int:
        from matrx_orm.operations.conflict_writes import _prep_rows

        for prepared in _prep_rows(self.model, rows):
            # value is NOT NULL: a bind of None (a blank string turned NULL) must fail here as it does live.
            assert prepared.get("value") is not None, "workflow.checkpoint_value.value is NOT NULL"
            self.rows.setdefault((str(prepared["run_id"]), prepared["value_hash"]), json.loads(prepared["value"]))
        return len(rows)

    def filter(self, run_id: str, value_hash__in: list[str]) -> Any:
        from matrx_orm.query.executor import QueryExecutor

        # The row as the driver's jsonb codec hands it over, then matrx-orm's own `.values()` decode.
        decode = QueryExecutor(self.model.filter(run_id=run_id)._build_query())._decode_row_dict
        found = [
            decode({"value_hash": h, "value": self.rows[(run_id, h)]})
            for h in value_hash__in
            if (run_id, h) in self.rows
        ]

        class _Q:
            async def values(self, *_: str) -> list[dict[str, Any]]:
                return found

        return _Q()


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> _PostgresLikeValueTable:
    from matrx_graph.checkpoint import value_store

    fake = _PostgresLikeValueTable()
    monkeypatch.setattr(value_store, "get_model", lambda name: fake)
    return fake


@pytest.mark.parametrize("text", STRINGS)
async def test_a_stored_string_reads_back_as_the_same_string(table: _PostgresLikeValueTable, text: str) -> None:
    from matrx_graph.checkpoint.value_store import load_run_values, store_run_values

    run_id = str(uuid.uuid4())
    await store_run_values(run_id, {"h1": text}, organization_id=str(uuid.uuid4()))
    back = await load_run_values(run_id, ["h1"])
    assert back == {"h1": text}
    assert isinstance(back["h1"], str)


async def test_objects_and_lists_are_unchanged(table: _PostgresLikeValueTable) -> None:
    from matrx_graph.checkpoint.value_store import load_run_values, store_run_values

    run_id = str(uuid.uuid4())
    values = {"o": {"a": 1, "b": ["x", "y"]}, "l": [1, "two", {"three": 3}]}
    await store_run_values(run_id, values, organization_id=str(uuid.uuid4()))
    assert await load_run_values(run_id, ["o", "l"]) == values


async def test_an_interned_json_answer_resolves_back_into_a_string_field(table: _PostgresLikeValueTable) -> None:
    """The run-once-per-key path end to end: a long ``final_text`` is interned out of the saved
    output and resolved back in; the saved result must still validate as the step's output."""
    from pydantic import BaseModel

    from matrx_graph.checkpoint.value_store import load_run_values, store_run_values
    from matrx_graph.checkpoint.values import outcome_input_row, referenced_hashes, resolve_values

    class AgentResultLike(BaseModel):
        final_text: str = ""
        content: list[Any] = []

    answer = json.dumps({"room": "self_description", "claims": [{"id": f"c{i}", "claim": "x" * 200} for i in range(80)]})
    output = {"final_text": answer, "content": [{"__kind": "brand_claim_set", "claims": []}]}
    interned, values = outcome_input_row(output, 1024)
    assert values, "the long final_text must be interned for this test to mean anything"
    run_id = str(uuid.uuid4())
    await store_run_values(run_id, values, organization_id=str(uuid.uuid4()))
    store = await load_run_values(run_id, referenced_hashes(interned))
    resolved = resolve_values(interned, store)
    assert resolved["final_text"] == answer
    AgentResultLike.model_validate(resolved)


def test_the_value_field_declares_its_strings_are_values() -> None:
    """A JSON-looking answer stored here is a string ON PURPOSE: matrx-orm's once-per-field warning stays quiet."""
    from matrx_graph.db._registry import configure_db, reset_for_tests
    from matrx_graph.db.standalone import build_standalone_models

    model = build_standalone_models("value_store_strings_flag")["WfCheckpointValue"]
    assert model._fields["value"].strings_are_values is True
    model._fields["value"].strings_are_values = False  # a host-generated model starts without the flag
    try:
        configure_db(models={"WfCheckpointValue": model})
        assert model._fields["value"].strings_are_values is True
    finally:
        reset_for_tests()
