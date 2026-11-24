"""A kind property never lands in a key the record store reads as structure.

2026-11-17, live: ``window_cleaning_quote`` outputs were refused whole (``invalid input syntax for type uuid:
"owner@harborcoffee.example.com"`` — NOTHING STORED) because the kind's own ``to`` (an email) sat in the record's
document where the store's edge function cast ``to`` as a record id. That cast now runs only for relation records
(``custom.record_carrying_edges``, P10-CLEAN). The one key every record's document still carries as structure is
``parent_id`` (``custom.containment_parent`` casts it on every write); the live active kind ``content_plan_node``
declares a string ``parent_id``. Written there, a non-id fails the write and an id silently re-parents the record.
The class guard: such a property gets a column of its own, and its value maps back to the kind's own name.
"""

from __future__ import annotations

from matrx_graph.kind_fields import (
    STORE_STRUCTURE_KEYS,
    fields_for_kind,
    record_values_for,
    value_from_record,
)

_SCHEMA = {
    "type": "object",
    "properties": {
        "__kind": {"const": "plan_node"},
        "title": {"type": "string"},
        "parent_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "to": {"type": "string"},
    },
}


def _declarations() -> list[dict]:
    return [dict(f.declaration) for f in fields_for_kind(_SCHEMA, kind="plan_node")]


def test_no_field_of_a_kind_claims_a_store_structure_key() -> None:
    keys = {d["key"] for d in _declarations()}
    assert "parent_id" in STORE_STRUCTURE_KEYS
    assert not keys & set(STORE_STRUCTURE_KEYS), keys


def test_the_value_is_written_under_its_own_column_and_reads_back_by_its_own_name() -> None:
    declarations = _declarations()
    value = {"__kind": "plan_node", "title": "Intro", "parent_id": "node-1", "to": "owner@example.com"}
    values, children = record_values_for(value, declarations)
    assert not set(values) & set(STORE_STRUCTURE_KEYS), values
    assert "node-1" in values.values()
    # A plain property of the same name as a relation END stays its own column: only relation records cast it.
    assert values["to"] == "owner@example.com"
    assert value_from_record(values, children, declarations, kind="plan_node") == value
