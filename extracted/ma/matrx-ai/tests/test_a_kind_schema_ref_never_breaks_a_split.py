"""A kind schema that ``$ref``s a sibling kind validates; one nothing resolves never breaks a split.

2026-11-02: a saved reply quoting a ``variable_definition`` value could not be given its blocks —
the registered schema ``$ref``s ``variable_component.schema.json`` and the validator raised
``Unresolvable``, which failed the whole split (the reply saved without blocks). Two layers:
the splitter resolves a sibling kind's schema from the kind registry, and ``validate_instance``
fails open, loudly, on a ``$ref`` nothing resolves (as it already did on a malformed schema).
"""

from __future__ import annotations

from matrx_graph.executor.schema_validation import validate_instance
from matrx_graph.input_declaration import all_source_schemas

from matrx_ai.processing.blocks import blocks_v1
from matrx_ai.processing.blocks.saved_blocks import block_fields

_SCHEMAS = all_source_schemas()

_REPLY = """The shape:
```json
{
  "__kind": "variable_definition",
  "name": "target_brand",
  "label": "Brand",
  "required": true,
  "customComponent": { "__kind": "variable_component", "type": "nonsense_type" }
}
```
"""


def _registry(schemas: dict) -> blocks_v1.KindRegistryView:
    return blocks_v1.KindRegistryView(
        schema=lambda slug: schemas.get(slug),
        version=lambda slug: 1,
        known=lambda slug: slug in schemas,
        warm=lambda: True,
    )


def _kind_block(registry: blocks_v1.KindRegistryView) -> dict:
    fields = block_fields(_REPLY, validate=blocks_v1.kind_validator(registry))
    kinds = [b for b in fields["blocks"] if b["type"] == "kind"]
    assert len(kinds) == 1, fields["blocks"]
    return kinds[0]


def test_a_sibling_kind_ref_resolves_and_its_errors_are_reported() -> None:
    block = _kind_block(_registry(_SCHEMAS))
    assert block["status"] == "invalid"
    assert any("customComponent" in e for e in block["errors"]), block["errors"]


def test_a_ref_nothing_resolves_never_breaks_the_split() -> None:
    only_definition = {"variable_definition": _SCHEMAS["variable_definition"]}
    block = _kind_block(_registry(only_definition))
    assert block["kind"] == "variable_definition"


def test_validate_instance_fails_open_on_an_unresolvable_ref() -> None:
    schema = {"type": "object", "properties": {"x": {"$ref": "https://example.invalid/missing.schema.json"}}}
    assert validate_instance(schema, {"x": 1}) == []
    assert validate_instance(schema, {"x": 1}, retrieve=lambda uri: None) == []
