"""Anthropic's structured-output engine compiles a NARROW JSON-Schema subset, and
the shapes Pydantic emits routinely fall outside it. Every refusal asserted here
was measured live against ``claude-opus-5-5`` on 2026-09-27 — one probe request
per keyword combination, the provider's verbatim message quoted beside each case.

WHY IT MATTERS. The agent-generation agent — the trained builder that creates
every platform agent — is pinned to an Anthropic model and its wire contract is
``CreateAgentDefinitionEnvelope``. Every ``build_from_spec`` died with
"meta-agent execution failed" before a token was spent. The first fix stripped
the ONE keyword in the first 400 (``discriminator``) and the provider then
refused the very same contract for ``allOf``'s siblings, with a message that
still said ``anyOf``. So these tests cover the CLASS: no combinator may reach
Anthropic carrying a sibling its decoder will not compile, whatever produced it.

Each case fails on the pre-fix translator (prove it with
``git show <sha>:packages/matrx-ai/matrx_ai/schema/rules.py > …``) and passes
after.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.schema.rules import (
    COMBINATOR_SAFE_SIBLINGS,
    concretize_empty_schemas,
    flatten_allof,
    normalize_array_items,
    normalize_combinator_siblings,
    prune_unreachable_defs,
    structured_output_schema_violations,
    take_normalization_notes,
)


def wire(schema: dict[str, Any]) -> dict[str, Any]:
    """The schema exactly as the Anthropic send boundary would transmit it."""
    fmt = AnthropicTranslator._build_anthropic_output_format(
        {"type": "json_schema", "json_schema": {"schema": schema}}
    )
    assert fmt is not None
    return fmt["schema"]


def walk(node: Any, path: str = "$"):
    """Every (path, node) pair in a schema, descending name maps correctly."""
    if isinstance(node, list):
        for index, item in enumerate(node):
            yield from walk(item, f"{path}[{index}]")
        return
    if not isinstance(node, dict):
        return
    yield path, node
    for key, value in node.items():
        if key in ("properties", "$defs", "definitions") and isinstance(value, dict):
            for name, sub in value.items():
                yield from walk(sub, f"{path}.{key}.{name}")
        elif key not in ("required", "enum", "const"):
            yield from walk(value, f"{path}.{key}")


def obj(**properties: Any) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
    }


# --------------------------------------------------------------------------
# The measured refusals, one case each.
# --------------------------------------------------------------------------

#: name -> (schema, the provider's verbatim 400 message for it)
REJECTED_SHAPES: dict[str, tuple[dict[str, Any], str]] = {
    # "output_config.format.schema: For 'anyOf', 'discriminator' is not supported"
    "discriminator_beside_anyof": (
        obj(
            u={
                "anyOf": [{"$ref": "#/$defs/A"}, {"$ref": "#/$defs/B"}],
                "discriminator": {"propertyName": "kind", "mapping": {"a": "#/$defs/A"}},
            }
        )
        | {"$defs": {"A": obj(kind={"type": "string"}), "B": obj(kind={"type": "string"})}},
        "For 'anyOf', 'discriminator' is not supported",
    ),
    # "output_config.format.schema: For 'anyOf', 'additionalProperties, properties,
    #  required, type' is not supported"  <- the shape that killed the factory,
    #  emitted by Pydantic for a model whose json_schema_extra adds a constraint.
    "allof_beside_object_structure": (
        obj(kind={"type": "string"}, url={"type": "string"})
        | {
            "additionalProperties": False,
            "allOf": [
                {
                    "anyOf": [
                        {"properties": {"url": {"type": "string"}}, "required": ["url"]},
                        {"properties": {"file_id": {"type": "string"}}, "required": ["file_id"]},
                    ]
                }
            ],
        },
        "For 'anyOf', 'additionalProperties, properties, required, type' is not supported",
    ),
    # A mergeable allOf: Anthropic documents allOf-with-$ref as unsupported and
    # 400s on the siblings, so it must be merged into the parent, not passed on.
    "allof_ref_branch_is_merged": (
        {
            "type": "object",
            "properties": {"a": {"type": "string"}},
            "required": ["a"],
            "allOf": [{"$ref": "#/$defs/Extra"}],
            "$defs": {"Extra": obj(b={"type": "string"})},
        },
        "For 'anyOf', 'properties, required, type' is not supported",
    ),
    # "output_config.format.schema: For 'anyOf', 'type' is not supported"
    "type_beside_anyof": (
        obj(u={"type": "string", "anyOf": [{"type": "string"}, {"type": "number"}]}),
        "For 'anyOf', 'type' is not supported",
    ),
    # "output_config.format.schema: For 'anyOf', 'additionalProperties' is not supported"
    "additionalproperties_beside_anyof": (
        obj(u={"anyOf": [{"type": "string"}, {"type": "number"}], "additionalProperties": False}),
        "For 'anyOf', 'additionalProperties' is not supported",
    ),
    # "output_config.format.schema: Schema type 'oneOf' is not supported"
    "oneof": (
        obj(u={"oneOf": [{"type": "string"}, {"type": "number"}]}),
        "Schema type 'oneOf' is not supported",
    ),
    # "output_config.format.schema: Schema keyword 'not' is not supported"
    "not_keyword": (
        obj(u={"type": "string", "not": {"type": "number"}}),
        "Schema keyword 'not' is not supported",
    ),
    # "Invalid schema: Array types must be specified with a single object schema for 'items'."
    "tuple_items": (
        obj(a={"type": "array", "items": [{"type": "string"}, {"type": "number"}]}),
        "Array types must be specified with a single object schema for 'items'",
    ),
    # "Empty schema ({}) that accepts any JSON value is not supported."
    "empty_schema_from_bare_any": (
        obj(anything={}),
        "Empty schema ({}) that accepts any JSON value is not supported",
    ),
    "annotation_only_schema": (
        obj(anything={"title": "Anything"}),
        "Empty schema ({}) that accepts any JSON value is not supported",
    ),
    # "For 'array' type, property 'prefixItems' is not supported"
    "prefix_items": (
        obj(a={"type": "array", "prefixItems": [{"type": "string"}]}),
        "For 'array' type, property 'prefixItems' is not supported",
    ),
    # "For 'array' type, property 'contains' is not supported"
    "contains": (
        obj(a={"type": "array", "items": {"type": "string"}, "contains": {"type": "string"}}),
        "For 'array' type, property 'contains' is not supported",
    ),
    # "For 'object' type, property 'if' is not supported"
    "if_then_else": (
        obj(a={"type": "string"})
        | {"if": {"properties": {"a": {"const": "x"}}}, "then": {"type": "object"}},
        "For 'object' type, property 'if' is not supported",
    ),
    # "For 'object' type, property 'dependentRequired' is not supported"
    "dependent_required": (
        obj(a={"type": "string"}, b={"type": "string"}) | {"dependentRequired": {"a": ["b"]}},
        "For 'object' type, property 'dependentRequired' is not supported",
    ),
    # "For 'object' type, property 'unevaluatedProperties' is not supported"
    "unevaluated_properties": (
        obj(a={"type": "string"}) | {"unevaluatedProperties": False},
        "For 'object' type, property 'unevaluatedProperties' is not supported",
    ),
    # "For 'object' type, 'additionalProperties' must be explicitly set to false"
    "additional_properties_true": (
        obj(o={"type": "object", "additionalProperties": True, "properties": {}, "required": []}),
        "'additionalProperties' must be explicitly set to false",
    ),
    # "For 'integer' type, property 'minimum' is not supported"
    "numeric_bounds": (
        obj(n={"type": "integer", "minimum": 0, "maximum": 9, "multipleOf": 2}),
        "For 'integer' type, property 'minimum' is not supported",
    ),
    # "For 'array' type, property 'maxItems' is not supported"
    "array_bounds": (
        obj(a={"type": "array", "items": {"type": "string"}, "maxItems": 3, "uniqueItems": True}),
        "For 'array' type, property 'maxItems' is not supported",
    ),
}


@pytest.mark.parametrize("case", sorted(REJECTED_SHAPES))
def test_the_send_boundary_emits_nothing_anthropic_rejects(case: str) -> None:
    """THE CLASS TEST. For every shape the live API refused, the wire schema the
    boundary produces carries no remaining violation — asserted by the same
    subset checker the translator screams through, so a NEW Pydantic shape that
    nobody normalised shows up here instead of as a 400 in production."""
    schema, provider_message = REJECTED_SHAPES[case]
    violations = structured_output_schema_violations(wire(schema))
    assert violations == [], (
        f"{case}: the boundary still emits a shape Anthropic refuses with "
        f"{provider_message!r} -> {violations}"
    )


@pytest.mark.parametrize("case", sorted(REJECTED_SHAPES))
def test_no_combinator_reaches_anthropic_with_a_forbidden_sibling(case: str) -> None:
    """Stated as the invariant rather than through the checker, so the two halves
    cannot drift: on the wire, a union node carries ONLY the keys measured as
    accepted, and no ``allOf`` survives at all."""
    schema, _ = REJECTED_SHAPES[case]
    for path, node in walk(wire(schema)):
        assert "allOf" not in node, f"{case}: allOf survived at {path}"
        if isinstance(node.get("anyOf"), list) or isinstance(node.get("oneOf"), list):
            offending = sorted(set(node) - COMBINATOR_SAFE_SIBLINGS)
            assert not offending, f"{case}: {offending} sit beside a union at {path}"


def test_an_allof_intersection_is_merged_not_discarded() -> None:
    """Merging is what makes the fix lossless where it can be: the branch's
    ``properties`` and ``required`` land on the parent."""
    merged, notes = take_normalization_notes(
        flatten_allof(
            {
                "type": "object",
                "properties": {"a": {"type": "string"}},
                "required": ["a"],
                "allOf": [{"type": "object", "properties": {"b": {"type": "string"}}, "required": ["b"]}],
            }
        )
    )
    assert "allOf" not in merged
    assert set(merged["properties"]) == {"a", "b"}
    assert merged["required"] == ["a", "b"]
    assert notes == []


def test_an_unmergeable_allof_branch_announces_itself() -> None:
    """A branch carrying its own union cannot merge into a parent that already
    has structure — dropping it silently would be a schema that quietly enforces
    less than the caller asked for, so the boundary reports it."""
    _, notes = take_normalization_notes(
        flatten_allof(
            {
                "type": "object",
                "properties": {"a": {"type": "string"}},
                "required": ["a"],
                "allOf": [{"anyOf": [{"required": ["a"]}, {"required": ["b"]}]}],
            }
        )
    )
    assert any("allOf branch dropped" in note for note in notes), notes


def test_a_narrowing_is_never_silent() -> None:
    """Every lossy rewrite reports what it gave up."""
    _, notes = take_normalization_notes(
        concretize_empty_schemas(normalize_array_items(obj(anything={}, a={"type": "array", "items": [{"type": "string"}]})))
    )
    assert any("empty schema" in note for note in notes), notes
    assert any("tuple `items`" in note for note in notes), notes


def test_a_property_named_like_a_keyword_is_never_touched() -> None:
    """Only schema KEYWORDS are normalised. A contract with properties named
    ``discriminator``, ``allOf`` and ``not`` keeps every one of them."""
    schema = obj(
        discriminator={"type": "string"},
        allOf={"type": "string"},
        **{"not": {"type": "string"}},
    )
    out = wire(schema)
    assert set(out["properties"]) == {"discriminator", "allOf", "not"}
    assert out["properties"]["discriminator"] == {"type": "string"}


def test_an_unreferenced_definition_is_pruned() -> None:
    """Lossless, and not cosmetic: the engine compiles the whole document, so a
    definition nothing points at spends compiled-grammar capacity."""
    pruned = prune_unreachable_defs(
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {"a": {"$ref": "#/$defs/Used"}},
            "required": ["a"],
            "$defs": {"Used": obj(k={"type": "string"}), "Orphan": obj(k={"type": "string"})},
        }
    )
    assert set(pruned["$defs"]) == {"Used"}


def test_a_recursive_contract_is_named_not_silently_shipped() -> None:
    """``Circular reference detected in schema definitions: N -> N`` is a hard
    400 no boundary rewrite can remove, so the checker reports it by name rather
    than letting the request fail at the provider with no local trace."""
    violations = structured_output_schema_violations(
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["n"],
            "properties": {"n": {"$ref": "#/$defs/N"}},
            "$defs": {
                "N": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["child"],
                    "properties": {"child": {"anyOf": [{"$ref": "#/$defs/N"}, {"type": "null"}]}},
                }
            },
        }
    )
    assert any("circular reference" in v for v in violations), violations


def test_the_normalization_never_mutates_the_callers_schema() -> None:
    """The stored schema keeps the full contract — only the provider's copy is
    reduced. A mutation here would corrupt a persisted agent config."""
    schema, _ = REJECTED_SHAPES["allof_beside_object_structure"]
    import copy

    before = copy.deepcopy(schema)
    wire(schema)
    assert schema == before


def test_the_agent_factory_wire_contract_clears_the_anthropic_subset() -> None:
    """The real contract that was failing: the agent-generation agent's own
    envelope. It must carry no keyword violation on the wire.

    (It is still refused by Anthropic's compiled-grammar CAPACITY ceiling, which
    is a different failure with a different message and no schema rewrite can
    clear it — see the task report. This test guards the half that is ours.)"""
    try:
        from aidream.services.agent_factory.agent_builder_agent import (
            CreateAgentDefinitionEnvelope,
        )
    except Exception:  # pragma: no cover - package-only test run
        pytest.skip("aidream is not importable from this test run")

    schema = CreateAgentDefinitionEnvelope.model_json_schema()
    assert "propertyName" in str(schema) and '"allOf"' in str(schema).replace("'", '"'), (
        "this test is only meaningful while the builder's contract still carries a "
        "discriminated union and an allOf refinement; if that changed, retarget it"
    )
    violations = structured_output_schema_violations(wire(schema))
    assert violations == [], violations


def test_no_optional_property_reaches_anthropic() -> None:
    """Anthropic caps a request at 24 OPTIONAL parameters and then refuses the
    compiled grammar with a message that names no keyword — "The compiled grammar
    is too large". Measured live on 2026-09-27: the agent factory's contract with
    its 106 optional properties is refused on ``claude-opus-5-5`` and the byte-for-
    byte same schema with every property required is accepted. So the boundary
    leaves none, whatever the producer did."""
    from matrx_ai.schema.rules import count_optional_properties

    schema = {
        "type": "object",
        "properties": {
            "a": {"type": "string"},
            "b": {"anyOf": [{"type": "string"}, {"type": "null"}]},
            "c": {"type": "object", "properties": {"d": {"type": "string"}}},
        },
        "required": ["a"],
    }
    assert count_optional_properties(schema) == 3
    out = wire(schema)
    assert count_optional_properties(out) == 0
    # A Pydantic optional stays answerable as null — required forbids nothing.
    assert {"type": "null"} in out["properties"]["b"]["anyOf"]


def test_making_properties_required_announces_itself() -> None:
    from matrx_ai.schema.rules import take_normalization_notes

    fmt = AnthropicTranslator._build_anthropic_output_format(
        {
            "type": "json_schema",
            "json_schema": {
                "schema": {"type": "object", "properties": {"a": {"type": "string"}}, "required": []}
            },
        }
    )
    assert fmt is not None
    # The note is stripped before the send, so assert on the normalizer directly.
    _, notes = take_normalization_notes(
        {"x-matrx-normalization-notes": ["1 optional property made required: ..."]}
    )
    assert notes
    assert fmt["schema"]["required"] == ["a"]
