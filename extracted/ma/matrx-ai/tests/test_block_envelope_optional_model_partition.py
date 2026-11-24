"""An ``Optional[Model]`` node (``anyOf: [{$ref}, {type: null}]``) is partitioned like any object.

Live class ``block_envelope_contract_drift`` (data_table, 2026-11-02): a key the
nested model does not declare stayed in the clean value and failed the WHOLE block,
while the same key one level up rides residue. The key must survive (law 3) as
residue, and the block must stamp.
"""

from __future__ import annotations

from matrx_graph.executor.schema_validation import validate_instance

from matrx_ai.processing.blocks.envelope import _partition_value

SCHEMA = {
    "type": "object",
    "required": ["__kind", "rows"],
    "properties": {
        "__kind": {"const": "data_table"},
        "rows": {"type": "array", "items": {"type": "object"}},
        "source": {"anyOf": [{"$ref": "#/$defs/TableSource"}, {"type": "null"}], "default": None},
    },
    "additionalProperties": False,
    "$defs": {
        "TableSource": {
            "type": "object",
            "properties": {"origin": {"anyOf": [{"type": "string"}, {"type": "null"}]}},
            "additionalProperties": False,
        }
    },
}


def test_undeclared_key_inside_optional_model_rides_residue() -> None:
    value = {"__kind": "data_table", "rows": [], "source": {"origin": "manual", "stray": "x"}}
    clean, _root_residue, node_index, collapses = _partition_value(value, SCHEMA)
    assert clean["source"] == {"origin": "manual"}
    assert node_index["source"]["residue"]["extra"] == {"stray": "x"}
    assert collapses == []
    assert validate_instance(SCHEMA, clean) == []


def test_null_optional_model_is_left_alone() -> None:
    value = {"__kind": "data_table", "rows": [], "source": None}
    clean, *_ = _partition_value(value, SCHEMA)
    assert clean.get("source") is None  # unset optional: absent or null, never a rejection
    assert validate_instance(SCHEMA, clean) == []
