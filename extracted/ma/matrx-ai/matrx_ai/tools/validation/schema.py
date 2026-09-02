"""Canonicalisation of tool argument schemas.

Two sides need to be compared for argument drift:

* **Code** — a Pydantic ``ToolArgs`` subclass, whose ``model_json_schema()`` is
  standard JSON Schema.
* **Database** — ``tool_def.parameters``, which in production appears in *two*
  different shapes (itself a form of drift this system surfaces):

    1. *Flat* (the dominant matrx custom shape)::

           {"command": {"type": "string", "required": true, "description": "..."},
            "timeout_seconds": {"type": "integer", "default": 30}}

    2. *Standard JSON Schema*::

           {"type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]}

Both sides are reduced to ``dict[str, CanonParam]`` so the engine can diff them
field-by-field without caring which representation it started from.

Multi-action *dispatcher* tools (one DB row + an ``action``/``command`` discriminator)
carry a richer, per-action contract on both sides — a code-side discriminated
``RootModel`` union and a DB-side ``$variants`` map. See the "Per-action contracts"
section at the bottom of this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, get_args

from pydantic import BaseModel, RootModel

# Sentinel distinct from ``None`` (a legitimate default value).
_MISSING = object()

# JSON-Schema / matrx type names normalised to a single vocabulary.
_TYPE_ALIASES = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
}


@dataclass(frozen=True)
class CanonParam:
    name: str
    type: str
    required: bool
    has_default: bool
    default: Any
    description: str | None
    # The allowed-value set when the field is an enum (code ``Literal[...]`` /
    # ``Enum`` or DB ``enum``), else ``None`` (unconstrained). Compared as a set,
    # so member order never matters and a one-sided enum (constrained on one side,
    # open on the other) is itself drift.
    enum: frozenset[str] | None = None

    @property
    def optional(self) -> bool:
        # A param is optional if it isn't required or carries a default.
        # Pydantic cannot represent "optional with no default", so we compare on
        # this derived flag rather than raw (required, has_default) to avoid
        # flagging that representational gap as drift.
        return (not self.required) or self.has_default

    def identity(self) -> tuple[str, str, bool]:
        """Drift identity: name + type + optionality (description excluded)."""
        return (self.name, self.type, self.optional)

    def default_key(self) -> Any:
        return _hashable(self.default) if self.has_default else _MISSING


def _hashable(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple(sorted((k, _hashable(v)) for k, v in value.items()))
    if isinstance(value, list):
        return tuple(_hashable(v) for v in value)
    return value


def _norm_type(raw: Any) -> str:
    if raw is None:
        return "any"
    if isinstance(raw, list):
        # JSON-Schema union as a type array, e.g. ["string", "null"].
        non_null = [t for t in raw if t != "null"]
        raw = non_null[0] if non_null else "any"
    if not isinstance(raw, str):
        return "any"
    return _TYPE_ALIASES.get(raw, raw)


def _type_from_property(prop: dict[str, Any]) -> str:
    """Extract a single type name from a JSON-Schema property node."""
    if "type" in prop:
        return _norm_type(prop["type"])
    # Optionals/unions: pydantic emits anyOf: [{type: X}, {type: null}].
    for key in ("anyOf", "oneOf"):
        if key in prop and isinstance(prop[key], list):
            for member in prop[key]:
                if not isinstance(member, dict):
                    continue
                if member.get("type") not in (None, "null"):
                    return _norm_type(member.get("type"))
                # An optional MODEL arrives as {"$ref": …} (or an inlined
                # {"properties": …}) with no "type" key. Reading that as "any"
                # let a typeless DB property pass the gate — which is how
                # credential_login shipped a `submit` the provider advertised
                # as untyped and agents sent as a JSON string (2026-08-21).
                if "$ref" in member or "properties" in member:
                    return "object"
    if "$ref" in prop or "allOf" in prop:
        return "object"
    if "enum" in prop and isinstance(prop["enum"], list) and prop["enum"]:
        return _norm_type(type(prop["enum"][0]).__name__)
    return "any"


def _resolve_ref(ref: Any, defs: dict[str, Any] | None) -> dict[str, Any] | None:
    """Resolve a ``#/$defs/Name`` JSON-Schema ``$ref`` against the schema's
    ``$defs`` block (where Pydantic emits ``Enum`` subclasses)."""
    if not (isinstance(ref, str) and ref.startswith("#/$defs/") and defs):
        return None
    target = defs.get(ref[len("#/$defs/"):])
    return target if isinstance(target, dict) else None


def _enum_from_property(prop: dict[str, Any], defs: dict[str, Any] | None = None) -> frozenset[str] | None:
    """Extract the allowed-value set from a JSON-Schema / flat property node.

    Handles the inline ``enum`` list (multi-member ``Literal[...]`` and the DB's
    flat shape), Pydantic's ``const`` (single-member ``Literal``), ``anyOf``/
    ``oneOf`` unions (optional enums — ``Literal | None``), and ``$ref`` into
    ``$defs`` (``Enum`` subclasses). Returns ``None`` when the field is not an
    enum. Members are stringified so an ``IntEnum`` and a string enum compare on
    value text, matching how the DB stores them.
    """
    enum = prop.get("enum")
    if isinstance(enum, list) and enum:
        return frozenset(str(v) for v in enum)
    if "const" in prop:
        return frozenset({str(prop["const"])})
    for key in ("anyOf", "oneOf"):
        members = prop.get(key)
        if isinstance(members, list):
            collected: set[str] = set()
            for m in members:
                if isinstance(m, dict):
                    sub = _enum_from_property(m, defs)
                    if sub:
                        collected |= sub
            if collected:
                return frozenset(collected)
    target = _resolve_ref(prop.get("$ref"), defs)
    if target is not None:
        return _enum_from_property(target, defs)
    return None


def _is_json_schema_object(params: dict[str, Any]) -> bool:
    return (
        params.get("type") == "object"
        and isinstance(params.get("properties"), dict)
    )


def canon_db_params(params: Any) -> dict[str, CanonParam]:
    """Canonicalise a ``tool_def.parameters`` value (either supported shape)."""
    if not isinstance(params, dict) or not params:
        return {}

    if _is_json_schema_object(params):
        return _canon_json_schema(params)

    # Flat custom shape: {name: {type, required, default, description}}.
    out: dict[str, CanonParam] = {}
    for name, spec in params.items():
        # Reserved meta keys (e.g. "$variants" — the per-action contract) are not
        # parameters; the dispatcher path reads them separately.
        if name.startswith("$"):
            continue
        if not isinstance(spec, dict):
            out[name] = CanonParam(name, "any", False, False, None, None)
            continue
        has_default = "default" in spec
        out[name] = CanonParam(
            name=name,
            type=_type_from_property(spec),
            required=bool(spec.get("required", False)) and not has_default,
            has_default=has_default,
            default=spec.get("default", _MISSING) if has_default else _MISSING,
            description=spec.get("description"),
            enum=_enum_from_property(spec),
        )
    return out


def _canon_json_schema(
    schema: dict[str, Any], defs: dict[str, Any] | None = None
) -> dict[str, CanonParam]:
    props = schema.get("properties", {})
    if defs is None:
        defs = schema.get("$defs") if isinstance(schema.get("$defs"), dict) else {}
    required_list = schema.get("required", []) or []
    required = set(required_list) if isinstance(required_list, list) else set()
    out: dict[str, CanonParam] = {}
    for name, prop in props.items():
        if not isinstance(prop, dict):
            prop = {}
        has_default = "default" in prop
        out[name] = CanonParam(
            name=name,
            type=_type_from_property(prop),
            required=name in required and not has_default,
            has_default=has_default,
            default=prop.get("default", _MISSING) if has_default else _MISSING,
            description=prop.get("description"),
            enum=_enum_from_property(prop, defs),
        )
    return out


def canon_model_params(model: type[BaseModel]) -> dict[str, CanonParam]:
    """Canonicalise a Pydantic args model via its JSON Schema."""
    schema = model.model_json_schema()
    # Pydantic always emits an object schema with properties at the top level.
    if not _is_json_schema_object(schema):
        # A model with no fields still has type=object but maybe no properties.
        schema = {"type": "object", "properties": schema.get("properties", {}),
                  "required": schema.get("required", []), "$defs": schema.get("$defs", {})}
    return _canon_json_schema(schema)


# ── Per-action (dispatcher) contracts ───────────────────────────────────────
#
# Multi-action tools (``web``, ``sql``, ``memory`` … — one DB row, an ``action``/
# ``command`` discriminator) cannot be honestly checked field-by-field against a
# single flat parameter map: the real contract is per-action ("queries is
# required when action=search"). Both sides express that contract explicitly:
#
# * **Code** — the registered args model is a ``RootModel`` wrapping a *discriminated
#   union* of per-action submodels (each a ``ToolArgs`` carrying ``action:
#   Literal["search"]``). We introspect the union members directly — NOT via
#   ``model_json_schema()``, whose top level is ``oneOf``/``$defs`` and would defeat
#   the flat canonicaliser.
# * **Database** — ``tool_def.parameters["$variants"]`` maps each action tag to a flat
#   param map (the very shape :func:`canon_db_params` already understands).
#
# The engine then diffs the two maps action-by-action, plus the discriminator's
# enum members.


def discriminated_union_members(
    model: type,
) -> tuple[str, dict[str, type[BaseModel]]] | None:
    """If ``model`` is a ``RootModel`` wrapping a discriminated ``Union`` of submodels,
    return ``(discriminator_field, {action_tag: submodel})``; otherwise ``None``.

    Returns ``None`` for plain ``BaseModel`` args models and ``NoArgs`` — those take
    the ordinary flat path.
    """
    if not (isinstance(model, type) and issubclass(model, RootModel)):
        return None
    root = model.model_fields.get("root")
    if root is None:
        return None
    ann = root.annotation
    # The discriminator can surface either on the FieldInfo (Pydantic lifts
    # ``Field(discriminator=...)`` onto it) or inside the ``Annotated`` metadata,
    # depending on how the annotation was normalised. Check both.
    disc: str | None = getattr(root, "discriminator", None)
    base: Any = ann
    metadata = getattr(ann, "__metadata__", None)
    if metadata is not None:  # Annotated[Union[...], Field(discriminator="action")]
        base = getattr(ann, "__origin__", ann)
        if disc is None:
            for meta in metadata:
                d = getattr(meta, "discriminator", None)
                if isinstance(d, str):
                    disc = d
    members = [
        m for m in get_args(base)
        if isinstance(m, type) and issubclass(m, BaseModel)
    ]
    if not isinstance(disc, str) or not members:
        return None
    out: dict[str, type[BaseModel]] = {}
    for m in members:
        field = m.model_fields.get(disc)
        if field is None:
            continue
        tags = get_args(field.annotation)  # Literal["search"] -> ("search",)
        tag = tags[0] if tags else None
        if isinstance(tag, str):
            out[tag] = m
    return (disc, out) if out else None


def canon_model_variant(
    submodel: type[BaseModel], discriminator: str
) -> dict[str, CanonParam]:
    """Canonicalise one union member, dropping the discriminator field itself
    (it lives only at the top level of the DB row, not inside each ``$variants`` entry)."""
    params = canon_model_params(submodel)
    params.pop(discriminator, None)
    return params


def canon_db_variants(params: Any) -> dict[str, dict[str, CanonParam]] | None:
    """Canonicalise ``tool_def.parameters["$variants"]`` into ``{action: {param: CanonParam}}``.
    Returns ``None`` when the row carries no per-action contract."""
    if not isinstance(params, dict):
        return None
    variants = params.get("$variants")
    if not isinstance(variants, dict) or not variants:
        return None
    out: dict[str, dict[str, CanonParam]] = {}
    for action, spec in variants.items():
        out[str(action)] = canon_db_params(spec) if isinstance(spec, dict) else {}
    return out


def db_discriminator_enum(params: Any, discriminator: str) -> set[str] | None:
    """Extract the discriminator's ``enum`` members from a DB ``parameters`` value
    (either flat or JSON-Schema-object shape). Returns ``None`` when absent."""
    if not isinstance(params, dict):
        return None
    node: Any = params
    if _is_json_schema_object(params):
        node = params.get("properties", {})
    spec = node.get(discriminator) if isinstance(node, dict) else None
    if not isinstance(spec, dict):
        return None
    enum = spec.get("enum")
    if isinstance(enum, list) and enum:
        return {str(v) for v in enum}
    return None
