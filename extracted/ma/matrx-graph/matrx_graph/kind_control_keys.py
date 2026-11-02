"""The four control keys an agent may put beside a kind's values — ONE definition.

``_replaces``, ``_new``, ``_record_id``, ``_records`` are how a model says "this answer replaces
that output", "this is something new", "change this record" and "here are several records".
They are not part of any kind: no registry row is ever edited to carry them (manager ruling
2026-10-02). They are added at READ time, where a schema is used, by this one function:

* **stored** mode — the schema the stream detector and the envelope validate against; never
  sent to a provider. All four keys are declared optional properties, so the envelope's
  ``_partition`` keeps them in the value instead of moving them to residue, and the kind's
  root ``required`` Fields are lifted when the value is a patch (``_record_id``) or a batch
  (``_records``): a patch carries only changed values, a reference none, a batch its values
  inside the items. The lift is ONE branch APPENDED to ``allOf`` — an existing ``allOf`` (a
  table's type-dependent ``if/then`` branches, a registry kind's own) is never replaced.
* **authored** mode — what the model is shown (response formats). ``_replaces`` and ``_new``
  always; ``_record_id`` only with ``allow_edit``; ``_records`` only with ``many``, and then the
  root IS the batch: ``{__kind, _records: [<record without __kind>], _replaces, _new}``. Every
  signal is declared OPTIONAL: the provider translators widen optional properties to
  required-and-nullable for strict providers and prune a null back to absence — but only within
  a budget: on Anthropic the two extra root keys forced themselves (or real Fields) non-null on
  5 of 24 live record kinds (2026-10-02). So authored mode reaches a model ONLY through
  ``response_format_for_kind(..., control_keys=True)``, a chain-aware run. ``_records`` is the
  batch's content and is required.

Applied only to ``record`` kinds and table kinds (``applies_to``). The TypeScript twin is
``withControlKeys`` in ``@ai-matrx/content-ir``; both produce the same JSON for the same input
(guard W2-G7, ``tests/fixtures/kind_control_keys_golden.json``).

Design: common-docs ``projects/data-doctrine-adoption/v6/KINDS-GLUE-WAVE2-DESIGN.md`` §1.4.
"""

from __future__ import annotations

import copy
from typing import Any, Literal

__all__ = [
    "CONTROL_KEYS",
    "RECORD_DISPOSITION",
    "applies_to",
    "CONTROL_KEY_FIELDS",
    "strip_control_keys",
    "with_control_key_fields",
    "with_control_keys",
]

#: The four keys, in the order they are declared.
CONTROL_KEYS: tuple[str, ...] = ("_replaces", "_new", "_record_id", "_records")

#: The one disposition whose kinds take the control keys (table kinds are always ``record``).
RECORD_DISPOSITION = "record"

_KIND_KEY = "__kind"

# Root keywords that describe the DOCUMENT, not the record object: they stay at the root when a
# batch moves the record into ``_records.items`` (a ``$ref`` resolves against the root).
_DOCUMENT_KEYS = ("$schema", "$id", "$defs", "definitions", "title", "description")


def applies_to(disposition: str | None) -> bool:
    """Whether a kind with this disposition takes the control keys."""
    return disposition == RECORD_DISPOSITION


def _is_object_schema(schema: Any) -> bool:
    return (
        isinstance(schema, dict)
        and schema.get("type") == "object"
        and isinstance(schema.get("properties"), dict)
    )


def _record_object(schema: dict[str, Any]) -> dict[str, Any]:
    """The kind's record object without ``__kind`` — what one item of ``_records`` is."""
    item = {k: copy.deepcopy(v) for k, v in schema.items() if k not in _DOCUMENT_KEYS}
    props = {k: v for k, v in item.get("properties", {}).items() if k != _KIND_KEY and k not in CONTROL_KEYS}
    item["properties"] = props
    required = [k for k in item.get("required") or [] if k != _KIND_KEY and k not in CONTROL_KEYS]
    if required:
        item["required"] = required
    else:
        item.pop("required", None)
    return item


def _stored(schema: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(schema)
    item = _record_object(schema)
    props = out["properties"]
    props["_replaces"] = {"type": ["string", "null"], "format": "uuid"}
    props["_new"] = {"type": ["boolean", "null"]}
    props["_record_id"] = {"type": ["string", "null"], "format": "uuid"}
    props["_records"] = {"type": ["array", "null"], "items": item}

    root_required = [k for k in out.get("required") or [] if k not in CONTROL_KEYS]
    lifted = [k for k in root_required if k != _KIND_KEY]
    if lifted:
        # A patch or a batch carries no root Fields: the root's required Fields hold only when
        # the value is neither. `null` means absent, so only a real id / a real list lifts.
        kept = [k for k in root_required if k == _KIND_KEY]
        if kept:
            out["required"] = kept
        else:
            out.pop("required", None)
        branch = {
            "if": {
                "anyOf": [
                    {"required": ["_record_id"], "properties": {"_record_id": {"type": "string"}}},
                    {"required": ["_records"], "properties": {"_records": {"type": "array"}}},
                ]
            },
            "else": {"required": lifted},
        }
        all_of = out.get("allOf")
        out["allOf"] = [*all_of, branch] if isinstance(all_of, list) else [branch]
    return out


def _authored(schema: dict[str, Any], *, many: bool, allow_edit: bool) -> dict[str, Any]:
    # OPTIONAL, never "required and nullable": every provider translator widens an optional
    # property to required-and-nullable on the wire and prunes a null answer back to absence
    # (``matrx_ai.schema.lint``, SCHEMA-TRANSLATION §13: "never store the widened copy"). So a
    # strict provider still sees every key, and an answer that uses no signal carries none —
    # every downstream check against the registered schema stays exactly as it was.
    signals: dict[str, Any] = {
        "_replaces": {"type": "string", "format": "uuid"},
        "_new": {"type": "boolean"},
    }
    if allow_edit:
        signals["_record_id"] = {"type": "string", "format": "uuid"}

    if not many:
        out = copy.deepcopy(schema)
        out["properties"].update(signals)
        required = [k for k in out.get("required") or [] if k not in CONTROL_KEYS]
        if required or "required" in out:
            out["required"] = required
        return out

    # The batch root: the record's Fields move INTO the items; nothing is left beside them.
    out = {k: copy.deepcopy(v) for k, v in schema.items() if k in _DOCUMENT_KEYS}
    out["type"] = "object"
    kind_prop = schema["properties"].get(_KIND_KEY)
    properties: dict[str, Any] = {}
    if kind_prop is not None:
        properties[_KIND_KEY] = copy.deepcopy(kind_prop)
    properties["_records"] = {"type": "array", "items": _record_object(schema)}
    properties.update(signals)
    out["properties"] = properties
    out["required"] = [k for k in (_KIND_KEY, "_records") if k in properties]
    out["additionalProperties"] = False
    return out


def with_control_keys(
    schema: dict[str, Any],
    *,
    mode: Literal["stored", "authored"],
    many: bool = False,
    allow_edit: bool = False,
) -> dict[str, Any]:
    """Return a copy of ``schema`` that carries the control keys for ``mode``.

    ``many`` and ``allow_edit`` shape authored mode only; stored mode always declares all four.
    A schema that is not an object with ``properties`` (a root-form kind, the "any value" ``{}``)
    is returned unchanged — there is no record object to put a key beside.
    """
    if mode not in ("stored", "authored"):
        raise ValueError(f"with_control_keys: mode must be 'stored' or 'authored', got {mode!r}")
    if not _is_object_schema(schema):
        return schema
    if mode == "stored":
        return _stored(schema)
    return _authored(schema, many=many, allow_edit=allow_edit)


def strip_control_keys(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split a value into (values without the control keys, the control keys present)."""
    signals = {k: value[k] for k in CONTROL_KEYS if k in value}
    clean = {k: v for k, v in value.items() if k not in CONTROL_KEYS}
    return clean, signals


#: The render fields the control keys add to a content-ir ``KindSchema`` (as JSON) — all optional
#: and nullable, never stricter than the store. Twin of ``CONTROL_KEY_FIELDS`` in
#: ``@ai-matrx/content-ir``; a batch's items are read as opaque JSON (the store checks each).
CONTROL_KEY_FIELDS: dict[str, dict[str, Any]] = {
    "_replaces": {"type": "string", "nullable": True},
    "_new": {"type": "boolean", "nullable": True},
    "_record_id": {"type": "string", "nullable": True},
    "_records": {"type": "json[]", "nullable": True},
}


def with_control_key_fields(kind_schema: dict[str, Any]) -> dict[str, Any]:
    """``kind_schema`` (a ``KindSchema`` as JSON) with the four keys as optional render fields.

    Twin of ``withControlKeyFields``. A root-form kind is returned unchanged; a key the kind
    itself declares is left as declared.
    """
    if kind_schema.get("root"):
        return kind_schema
    fields = dict(kind_schema.get("fields") or {})
    for key in CONTROL_KEYS:
        if key not in fields:
            fields[key] = dict(CONTROL_KEY_FIELDS[key])
    return {**kind_schema, "fields": fields}
