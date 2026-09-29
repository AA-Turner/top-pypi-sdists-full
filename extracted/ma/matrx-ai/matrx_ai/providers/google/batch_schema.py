"""The Gemini BATCH endpoint's spelling of a structured-output schema.

Part of the ONE Google translator (``translator.GoogleTranslator.to_batch_request``
is the only caller). There is no second Google schema translator anywhere: until
2026-09-27 ``matrx_batch.google_batch._mirror_response_schema`` was one — it
deleted every keyword on a deny-list, so over the live schema set it dropped
``additionalProperties`` from 3,823 and ``$ref`` from 565 of 4,000 schemas and
recorded none of it (Arman, 2026-09-27: "we have translators for each schema type
and they are supposed to take in any input and make it safe for the exact api.
Fix it at the core and don't do a workaround").

WHY the batch lane needs its own spelling at all — measured, not assumed:

* The Batch API ACCEPTS ``responseJsonSchema`` and IGNORES it. 2026-08-15: 12/12
  CRM party-kind judgements came back under invented keys. Re-measured
  2026-09-27 with those same twelve stored payloads, raw field only:
  ``gemini-3.6-flash`` 0/13 and ``gemini-3.8-flash`` 0/13 conforming (invented
  keys, prose, a ``$ref`` object flattened). The live endpoint honours the same
  field; only the batch endpoint drops it.
* The Batch API enforces ``responseSchema`` — the OpenAPI ``Schema`` message —
  and that message has NO ``additionalProperties`` and no ``$ref``/``$defs``
  (``400 Unknown name "additional_properties" … response_schema: Cannot find
  field``, 2026-09-27).

So the conversion is to the ``Schema`` message, and it is done keyword by
keyword against an ALLOW-list (never a deny-list — an unknown keyword is a
question, not a deletion):

* LOSSLESS, so not recorded: ``$ref`` into ``$defs`` is INLINED (the SDK's own
  ``process_schema`` does the same); ``allOf`` is merged; ``const`` becomes a
  one-value ``enum``; ``["T", "null"]`` becomes ``nullable``;
  ``additionalProperties: false`` / ``unevaluatedProperties: false`` are dropped
  because a ``Schema`` object is CLOSED by construction (the decoder emits only
  declared properties — verified on the live batch probe); pure annotations
  (``$schema``, ``$id``, ``$comment``, ``examples``, ``x-*``, ``ui:*`` form
  hints …) carry no constraint.
* NOT expressible, so RECORDED by path and keyword through the translator's
  findings buffer (``structured_output.narrowed`` / ``.relaxed``, naming the
  agent and the schema): a recursive definition (unrolled to 4 levels with the
  shared primitive), a dynamic-key map (``additionalProperties: {schema}`` —
  the entries cannot be declared), ``oneOf`` (sent as ``anyOf``), a non-string
  ``enum``, and every other constraint keyword the ``Schema`` message lacks.

The answer is still CHECKED against the stored schema when the result lands;
nothing here changes the contract, only what the provider can enforce of it.
"""

from __future__ import annotations

import copy
from typing import Any

from matrx_ai.schema.rules import (
    flatten_allof,
    hoist_nested_defs,
    ref_cycles,
    rewrite_const_as_enum,
    unroll_recursive_refs,
)

#: Fields of Gemini's ``Schema`` message (Developer API, the one the Batch API
#: validates ``responseSchema`` against), spelled as JSON Schema spells them.
SCHEMA_MESSAGE_KEYWORDS = frozenset(
    {
        "type",
        "format",
        "title",
        "description",
        "nullable",
        "enum",
        "items",
        "minItems",
        "maxItems",
        "properties",
        "required",
        "minProperties",
        "maxProperties",
        "minLength",
        "maxLength",
        "pattern",
        "minimum",
        "maximum",
        "anyOf",
        "propertyOrdering",
        "default",
        "example",
    }
)

#: Keywords that constrain nothing (annotations / document plumbing). Dropping
#: them loses no enforcement, so they are not findings.
ANNOTATION_KEYWORDS = frozenset(
    {
        "$schema",
        "$id",
        "$anchor",
        "$comment",
        "$defs",
        "definitions",
        "examples",
        "readOnly",
        "writeOnly",
        "deprecated",
        "contentMediaType",
        "contentEncoding",
    }
)

#: The SDK's snake_case spellings of Schema fields (``types.Schema`` validates by
#: name too, so stored schemas written from it carry them). Normalised first.
_SNAKE_FIELDS = {
    "any_of": "anyOf",
    "additional_properties": "additionalProperties",
    "property_ordering": "propertyOrdering",
    "min_items": "minItems",
    "max_items": "maxItems",
    "min_length": "minLength",
    "max_length": "maxLength",
    "min_properties": "minProperties",
    "max_properties": "maxProperties",
}

_TYPES = frozenset({"string", "number", "integer", "boolean", "array", "object"})
_UNROLL_DEPTH = 4


def to_gemini_batch_schema(
    schema: dict[str, Any],
    *,
    narrowed: list[str] | None = None,
    relaxed: list[str] | None = None,
) -> dict[str, Any]:
    """Raw JSON Schema (what the live translator puts on ``response_json_schema``)
    → the ``Schema`` message the Batch API enforces on ``response_schema``.

    Never mutates ``schema``. Everything given up is appended to ``narrowed``
    (the provider now forbids something the contract allows) or ``relaxed`` (the
    provider now allows something the contract forbids), one line per path."""
    narrowed = narrowed if narrowed is not None else []
    relaxed = relaxed if relaxed is not None else []
    work = hoist_nested_defs(copy.deepcopy(schema))
    if ref_cycles(work):
        notes: list[str] = []
        work = unroll_recursive_refs(work, depth=_UNROLL_DEPTH, notes=notes)
        relaxed.extend(notes)
    work = flatten_allof(work, work)
    work = rewrite_const_as_enum(work)
    defs: dict[str, Any] = {}
    for key in ("$defs", "definitions"):
        if isinstance(work.get(key), dict):
            defs.update({f"#/{key}/{name}": body for name, body in work[key].items()})
    return _convert(work, defs, "$", narrowed, relaxed, frozenset())


def _convert(
    node: Any,
    defs: dict[str, Any],
    path: str,
    narrowed: list[str],
    relaxed: list[str],
    resolving: frozenset[str],
) -> Any:
    if not isinstance(node, dict):
        return node
    if any(key in _SNAKE_FIELDS for key in node):
        node = {_SNAKE_FIELDS.get(key, key): value for key, value in node.items()}
    ref = node.get("$ref")
    if isinstance(ref, str):
        target = defs.get(ref)
        if target is None or ref in resolving:
            relaxed.append(f"{path}: `$ref` {ref!r} does not resolve — the node is unconstrained")
            node = {k: v for k, v in node.items() if k != "$ref"}
        else:
            # Siblings beside a $ref (a description, a nullable) refine the target.
            merged = {**copy.deepcopy(target), **{k: v for k, v in node.items() if k != "$ref"}}
            return _convert(merged, defs, path, narrowed, relaxed, resolving | {ref})

    out: dict[str, Any] = {}
    nullable = False

    raw_type = node.get("type")
    if isinstance(raw_type, list):
        kinds = [t for t in raw_type if t != "null"]
        nullable = len(kinds) != len(raw_type)
        if len(kinds) > 1:
            # Several concrete types → one anyOf branch per type, sharing the rest.
            rest = {k: v for k, v in node.items() if k != "type"}
            branches = [
                _convert({**rest, "type": kind}, defs, f"{path}|{kind}", narrowed, relaxed, resolving)
                for kind in kinds
            ]
            result: dict[str, Any] = {"anyOf": branches}
            if nullable:
                result["nullable"] = True
            if isinstance(node.get("description"), str):
                result["description"] = node["description"]
            return result
        raw_type = kinds[0] if kinds else "null"
    if raw_type == "null":
        # A value that can ONLY be null (the unroll floor). The Schema message has
        # no null type; a nullable, property-less object is the closest shape and
        # the decoder writes null for it.
        return {"type": "object", "nullable": True, **(
            {"description": node["description"]} if isinstance(node.get("description"), str) else {}
        )}
    if isinstance(raw_type, str):
        if raw_type in _TYPES:
            out["type"] = raw_type
        else:
            relaxed.append(f"{path}: type {raw_type!r} has no Schema equivalent — dropped")

    for key, value in node.items():
        if key in ("type", "$ref"):
            continue
        at = f"{path}.{key}"
        if key == "properties" and isinstance(value, dict):
            out["properties"] = {
                name: _convert(sub, defs, f"{path}.properties.{name}", narrowed, relaxed, resolving)
                for name, sub in value.items()
            }
        elif key == "items":
            if isinstance(value, dict):
                out["items"] = _convert(value, defs, f"{path}.items", narrowed, relaxed, resolving)
            elif isinstance(value, list):  # draft-4 tuple form
                relaxed.append(f"{at}: tuple-form items cannot be expressed — items unconstrained")
            elif value is False:
                out["maxItems"] = 0
        elif key in ("anyOf", "oneOf") and isinstance(value, list):
            if key == "oneOf":
                relaxed.append(f"{at}: `oneOf` sent as `anyOf` — exactly-one is not enforced")
            branches = []
            for i, branch in enumerate(value):
                if isinstance(branch, dict) and branch.get("type") == "null" and len(branch) == 1:
                    nullable = True
                    continue
                branches.append(
                    _convert(branch, defs, f"{path}.{key}[{i}]", narrowed, relaxed, resolving)
                )
            if len(branches) == 1 and not out.get("properties"):
                # anyOf [T, null] → T nullable: the Schema message's own spelling.
                for bk, bv in branches[0].items():
                    out.setdefault(bk, bv)
            elif branches:
                out["anyOf"] = out.get("anyOf", []) + branches
        elif key == "additionalProperties":
            if value is False:
                continue  # a Schema object is closed by construction — lossless
            if value is True or isinstance(value, dict):
                if node.get("properties"):
                    relaxed.append(
                        f"{at}: extra keys beside the declared properties cannot be declared "
                        "— only the declared properties can be written"
                    )
                else:
                    narrowed.append(
                        f"{at}: a dynamic-key map cannot be declared in the batch Schema — "
                        "it can only be written empty"
                    )
        elif key == "unevaluatedProperties":
            if value is not False:
                relaxed.append(f"{at}: `unevaluatedProperties` cannot be expressed")
        elif key == "enum" and isinstance(value, list):
            values = [v for v in value if v is not None]
            if None in value:
                nullable = True
            if all(isinstance(v, str) for v in values):
                out["enum"] = values
                out.setdefault("type", "string")
            else:
                relaxed.append(
                    f"{at}: non-string enum {values!r} cannot be expressed — the value is "
                    "constrained by type only"
                )
        elif key == "exclusiveMinimum" and isinstance(value, (int, float)) and not isinstance(value, bool):
            out.setdefault("minimum", value)
            relaxed.append(f"{at}: exclusive bound {value} sent inclusive")
        elif key == "exclusiveMaximum" and isinstance(value, (int, float)) and not isinstance(value, bool):
            out.setdefault("maximum", value)
            relaxed.append(f"{at}: exclusive bound {value} sent inclusive")
        elif key == "examples":
            if isinstance(value, list) and value and "example" not in node:
                out["example"] = value[0]
        elif key in ANNOTATION_KEYWORDS or key.startswith(("x-", "ui:")):
            continue
        elif key in SCHEMA_MESSAGE_KEYWORDS:
            if key in ("default", "example") and _holds_null(value):
                # An annotation, not a constraint; a JSON null inside it cannot
                # survive the stored payload's null-stripping, so it is not sent.
                continue
            out[key] = copy.deepcopy(value)
        else:
            relaxed.append(f"{at}: `{key}` has no batch Schema equivalent — not enforced")

    if nullable:
        out["nullable"] = True
    if isinstance(out.get("required"), list) and isinstance(out.get("properties"), dict):
        out["required"] = [r for r in out["required"] if r in out["properties"]]
    return out


def _holds_null(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, dict):
        return any(_holds_null(v) for v in value.values())
    if isinstance(value, list):
        return any(_holds_null(v) for v in value)
    return False


__all__ = ["SCHEMA_MESSAGE_KEYWORDS", "ANNOTATION_KEYWORDS", "to_gemini_batch_schema"]
