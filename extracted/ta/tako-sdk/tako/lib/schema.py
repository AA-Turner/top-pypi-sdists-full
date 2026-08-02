"""``derive_response_schema`` — turn a caller ``output_schema`` into the schema
its ``structured_output`` actually validates against.

Per the Retrieval Agent contract (S1 §4.2): ``structured_output`` validates against
the caller's schema with **every dataset-slot node replaced by ``TakoDataset | null``**
(identity transform when there are no slots). A slot node is any object marked
``"x-tako-dataset": true``; it is nullable by construction (§12 — a declared-unfilled
slot returns ``null``, which the ``| null`` admits even when the slot is ``required``).

Usage::

    import jsonschema
    from tako.lib import derive_response_schema

    run = client.agent.retrieval.run(RetrievalAgentRunRequest(query="...", output_schema=my_schema))
    jsonschema.validate(run.result.structured_output, derive_response_schema(my_schema))

``TakoDataset`` (and its sub-schemas) is sourced from the generated model, so the
derived schema is self-contained.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Mapping, cast

from tako.models.tako_dataset import TakoDataset

_MARKER = "x-tako-dataset"
_TAKO_DATASET_DEF = "TakoDataset"

# A slot node becomes ``TakoDataset | null`` via a $ref into the derived $defs.
_SLOT_SUBSCHEMA: dict[str, Any] = {
    "anyOf": [{"$ref": f"#/$defs/{_TAKO_DATASET_DEF}"}, {"type": "null"}]
}

# JSON Schema keywords whose values hold nested schemas we must walk.
# Covers draft-07 through 2020-12. `dependentSchemas` (2020-12) and `dependencies`
# (draft-07) are {propName: schema} maps; draft-07's property-list form ({prop:
# [names]}) is a list value and passes through _replace untouched.
_MAP_OF_SCHEMAS = (
    "properties", "$defs", "definitions", "patternProperties", "dependentSchemas", "dependencies",
)
_LIST_OF_SCHEMAS = ("anyOf", "allOf", "oneOf", "prefixItems")
_SINGLE_SCHEMA = (
    "additionalProperties", "if", "then", "else", "not",
    "contains", "propertyNames", "unevaluatedProperties", "unevaluatedItems",
)


def _tako_dataset_defs() -> dict[str, Any]:
    """The ``TakoDataset`` object schema plus its transitive sub-schemas, keyed for ``$defs``."""
    schema = TakoDataset.model_json_schema()
    subdefs = schema.pop("$defs", {})
    return {_TAKO_DATASET_DEF: schema, **subdefs}


def _replace(node: Any, found: List[bool]) -> Any:
    """Recursively rebuild ``node``, replacing slot nodes; ``found[0]`` records a hit.

    Non-dict nodes (booleans, leaf values) pass through unchanged. Recursion only
    descends the JSON Schema keywords that hold nested schemas, so non-schema
    values (``enum`` members, ``default`` objects) are never mangled.
    """
    if not isinstance(node, dict):
        return node
    result: Dict[str, Any] = cast(Dict[str, Any], node)
    if result.get(_MARKER) is True:
        found[0] = True
        return copy.deepcopy(_SLOT_SUBSCHEMA)
    for key, val in list(result.items()):
        if key in _MAP_OF_SCHEMAS and isinstance(val, dict):
            sub = cast(Dict[str, Any], val)
            result[key] = {k: _replace(v, found) for k, v in sub.items()}
        elif key in _LIST_OF_SCHEMAS and isinstance(val, list):
            result[key] = [_replace(item, found) for item in cast(List[Any], val)]
        elif key in _SINGLE_SCHEMA and isinstance(val, dict):
            result[key] = _replace(val, found)
        elif key == "items":
            # ``items`` is a schema (object validation) or a list (tuple validation)
            if isinstance(val, list):
                result[key] = [_replace(item, found) for item in cast(List[Any], val)]
            elif isinstance(val, dict):
                result[key] = _replace(val, found)
    return result


def derive_response_schema(schema: Mapping[str, Any]) -> dict[str, Any]:
    """Return the response-validating schema for a caller ``output_schema``.

    Replaces every ``"x-tako-dataset": true`` node with ``TakoDataset | null`` and,
    if any slot was present, hoists the ``TakoDataset`` component (and its
    sub-schemas) into the result's ``$defs``. A markerless schema is returned
    verbatim (a deep copy — the input is never mutated).
    """
    if not isinstance(schema, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]  # defensive: callers may pass "auto"
        raise TypeError(
            f"output_schema must be a JSON Schema object (dict), got {type(schema).__name__}. "
            'The "auto" mode is reserved and not shipped.'
        )
    found: List[bool] = [False]
    result: Dict[str, Any] = _replace(copy.deepcopy(dict(schema)), found)
    if found[0]:
        tako_defs = _tako_dataset_defs()
        existing: Dict[str, Any] = result.get("$defs", {})
        clashes = [name for name, node in tako_defs.items() if name in existing and existing[name] != node]
        if clashes:
            raise ValueError(
                f"output_schema $defs collide with Tako-reserved names {clashes}; "
                "rename these definitions in your schema."
            )
        defs: Dict[str, Any] = result.setdefault("$defs", {})
        defs.update(tako_defs)  # slot refs (#/$defs/TakoDataset) resolve here
    return result
