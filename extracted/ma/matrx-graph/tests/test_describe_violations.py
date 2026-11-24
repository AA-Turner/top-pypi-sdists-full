"""``describe_violations`` names path + keyword + expectation, never a rejected value.

Born from ``block_envelope_contract_drift`` (1,095+ rows): the system error said only
``value:validation_failed``, so nobody could tell which field of which kind failed.
"""

from __future__ import annotations

from matrx_graph.executor.schema_validation import describe_violations, validate_instance

ITEM = {
    "type": "object",
    "required": ["__kind", "id"],
    "properties": {"__kind": {"const": "ranking"}, "id": {"type": "string"}},
    "additionalProperties": False,
}
SCHEMA = {
    "type": "object",
    "required": ["__kind", "rankings", "cards"],
    "properties": {
        "__kind": {"const": "rankings_set"},
        "rankings": {"type": "array", "items": ITEM},
        "source": {"anyOf": [{"type": "object", "properties": {"origin": {"type": "string"}},
                               "additionalProperties": False}, {"type": "null"}]},
        "meta": {"type": "object", "additionalProperties": {"type": "integer"}},
        "cards": {"type": "array"},
    },
}


def test_each_violation_names_path_keyword_and_expectation_without_values() -> None:
    value = {
        "__kind": "rankings_set",
        "rankings": [{"__kind": "ranking", "id": "a"}, {"__kind": "SECRET_ID_1", "id": "b"}],
        "source": {"origin": "SECRET_ORIGIN", "SECRET_EXTRA": "SECRET_VALUE"},
        "meta": {"SECRET_KEY": "SECRET_VALUE"},
    }
    lines = describe_violations(SCHEMA, value)
    assert validate_instance(SCHEMA, value)  # same verdict as the validator
    assert "(root): required 'cards'" in lines
    assert "rankings[1].__kind: const: expected 'ranking'" in lines
    assert "meta.*: type: expected 'integer', got string" in lines
    assert any(line.startswith("source: anyOf: no branch matched; closest:") for line in lines)
    assert "SECRET" not in repr(lines)


def test_valid_value_has_no_violations() -> None:
    value = {"__kind": "rankings_set", "rankings": [], "cards": []}
    assert describe_violations(SCHEMA, value) == []
