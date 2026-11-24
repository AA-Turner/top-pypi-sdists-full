"""The ONE generator of a ``tool.definition.parameters`` jsonb from a declared tool's args model.

The DB is the source of truth for a tool's contract, and the drift gate
(:mod:`matrx_ai.tools.validation.engine`) diffs it against the code model — so the row is
never a hand-typed guess. Two supported forms:

* a plain ``ToolArgs`` model -> the flat ``{name: {type, required, ...}}`` map;
* a discriminated-union ``RootModel`` dispatcher (one action or many) -> the same flat map
  (the union of every variant's fields, which is what a provider advertises) plus the
  per-action ``$variants`` contract ``canon_db_variants`` reads, each entry a JSON-Schema
  object (``type``/``properties``/``required``) carrying every default and nullable member.

Callers: ``scripts/tool_params_from_model.py`` (the CLI) and any host that writes its own
rows at boot (aidream's ``tables_*`` rows, ``aidream.tools.table_doors_tools.definition``).
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any


def _property_entry(prop: dict[str, Any], *, required: bool) -> dict[str, Any]:
    entry = {key: value for key, value in prop.items() if key != "title"}
    if required and "default" not in entry:
        entry["required"] = True
    return entry


def _inline(prop: Any, defs: dict[str, Any], _open: frozenset[str] = frozenset()) -> dict[str, Any]:
    """Inline ``$ref``s so the row stands alone (the DB carries no ``$defs``).

    A model that contains itself (a tree node, a nested filter) cannot be inlined forever: the
    second visit to a definition already being expanded closes as a bare ``{"type": "object"}``
    (the recursion point), so the output is finite and every other level is fully expanded.
    """
    if not isinstance(prop, dict):
        return {}
    ref = prop.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/$defs/"):
        name = ref.split("/")[-1]
        extra = {k: v for k, v in prop.items() if k != "$ref"}
        if name in _open:
            return {"type": "object", **{k: v for k, v in extra.items() if k == "description"}}
        merged = {**defs.get(name, {}), **extra}
        return _inline(merged, defs, _open | {name})
    out: dict[str, Any] = {}
    for key, value in prop.items():
        if isinstance(value, dict):
            out[key] = _inline(value, defs, _open)
        elif isinstance(value, list):
            out[key] = [_inline(v, defs, _open) if isinstance(v, dict) else v for v in value]
        else:
            out[key] = value
    return out


def _flat_map(model: type, *, drop: str | None = None) -> dict[str, Any]:
    schema = model.model_json_schema()
    defs = schema.get("$defs", {}) if isinstance(schema.get("$defs"), dict) else {}
    required = set(schema.get("required", []) or [])
    out: dict[str, Any] = {}
    for name, prop in (schema.get("properties") or {}).items():
        if drop is not None and name == drop:
            continue
        out[name] = _property_entry(_inline(prop, defs), required=name in required)
    return out


def build_parameters(model: type, *, action_description: str) -> dict[str, Any]:
    from matrx_ai.tools.validation.schema import discriminated_union_members

    union = discriminated_union_members(model)
    if union is None:
        return _flat_map(model)

    discriminator, members = union
    flat: dict[str, Any] = {}
    variants: dict[str, Any] = {}
    for tag, submodel in sorted(members.items()):
        schema = submodel.model_json_schema()
        defs = schema.get("$defs", {}) if isinstance(schema.get("$defs"), dict) else {}
        required = sorted(
            name
            for name in (schema.get("required", []) or [])
            if name != discriminator
        )
        properties = {
            name: _inline(prop, defs)
            for name, prop in (schema.get("properties") or {}).items()
            if name != discriminator
        }
        for name, prop in properties.items():
            properties[name] = {k: v for k, v in prop.items() if k != "title"}
        variants[tag] = {
            "type": "object",
            "required": required,
            "properties": properties,
        }
        for name, entry in _flat_map(submodel, drop=discriminator).items():
            flat.setdefault(name, {k: v for k, v in entry.items() if k != "required"})

    flat[discriminator] = {
        "enum": sorted(members),
        "type": "string",
        "required": True,
        "description": action_description,
    }
    flat["$variants"] = variants
    return flat


def _claimed_slugs(marker: Any) -> set[str]:
    """The kind names a row's ``__kind`` slot promises: a bare string, or a schema's ``const`` / ``enum``."""
    if isinstance(marker, str):
        return {marker}
    if isinstance(marker, dict):
        values = [marker.get("const"), *(marker.get("enum") or [])]
        return {v for v in values if isinstance(v, str)}
    return set()


def carry_curated_text(generated: Any, live: Any, registered_kinds: Collection[str]) -> Any:
    """``generated`` with every ``description`` the LIVE row already carries at the same place.

    The SHAPE of a row's parameters comes from code (field names, types, required, defaults, bounds); the TEXT
    a model reads may be curated on the row (a condensed description, a hint the model has none of). A host that
    writes parameters from code keeps that text: a description found at the same path in ``live`` wins; a field
    the row does not have yet takes the model's own description. Lists are walked by position only when both
    sides are the same length.

    A ``__kind`` the row declares and the model has not yet declared is carried ONLY when every kind it names is in
    ``registered_kinds`` (the kind registry the host reads): a real marker is part of the data and is never stripped
    (content-ir FEATURE.md section 4.2a), while a stale one naming no registered kind is an invented kind (rule 31)
    and the model wins. A slot the model declares itself is always the model's.
    """
    if isinstance(generated, dict):
        if not isinstance(live, dict):
            return generated
        out = {key: carry_curated_text(value, live.get(key), registered_kinds) for key, value in generated.items()}
        if isinstance(live.get("description"), str):
            out["description"] = live["description"]
        if "__kind" in live and "__kind" not in out:
            claimed = _claimed_slugs(live["__kind"])
            if claimed and claimed <= set(registered_kinds):
                out["__kind"] = live["__kind"]
        return out
    if isinstance(generated, list) and isinstance(live, list) and len(generated) == len(live):
        return [
            carry_curated_text(gen, row, registered_kinds) for gen, row in zip(generated, live, strict=True)
        ]
    return generated


__all__ = ["build_parameters", "carry_curated_text"]
