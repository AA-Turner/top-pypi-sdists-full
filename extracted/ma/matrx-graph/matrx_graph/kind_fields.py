"""A registered kind's OUTPUT TABLE, as Field declarations — wave 3's mapping run in reverse.

KINDS-GLUE wave 2 slice 1b (common-docs ``projects/data-doctrine-adoption/v6/KINDS-GLUE-WAVE2-DESIGN.md``
§2.3). Wave 3's :func:`matrx_graph.table_kinds.json_schema_for` turns a Table's Fields into the JSON
Schema of a record; :func:`fields_for_kind` turns a registered kind's JSON Schema (plus its owned
``content_ir.kind_edge`` rows) into the Fields of that kind's per-organization output table.

PURE. No database call, no I/O. The caller (wave 2's lander) reads the kind's schema and edges,
ensures each CHILD kind's output table first, and resolves every relation Field's target with
:func:`declarations_for`. A relation names its target as a kind (``KindField.child_kind``), or as
:data:`SELF` for a Field pointing back into this same table (``output_replaced_by``, a recursive
kind such as ``decision_node.yes``): the table id is not known until the table exists, so the
lander ensures the table without those Fields and then adds them (``custom.table_ensure`` adds a
missing Field and never retypes one).

WHAT THE STORE DECIDES, NOT THIS MODULE. Whether a relation OWNS what it points at is the target
table's fact (``contained_by_relation`` on the child output table — ``platform.relation_declaration``
refuses a Field that declares a ``flavor``), so a relation Field here carries only its target and
its ceiling. A child output table is ensured with ``contained_by_relation: true``
(:data:`CHILD_TABLE_SPEC`).

EVERY FIELD SAYS WHERE ITS VALUE CAME FROM, in its own ``config`` (read back verbatim through
``custom.table_kind_facts``): ``kind_key`` is the kind property it holds (a store key is
lower-case snake case, a kind property may be camelCase), ``child_kind`` the kind a relation's
records are, ``holds_json`` that a ``long_text`` holds the property's JSON. :func:`record_values_for`
splits a kind value into the parent record's values and its contained records;
:func:`value_from_record` rebuilds the kind value from them — both read only those Field facts, so
the round trip runs against a table's READ-BACK Fields (guard W2-G4).

PLATFORM FIELDS carry ``config.kept_by = "agent_output"``: the live N-C3 contract
(``custom._value_envelope``, chairdoors2_h) refuses a person's write to them except setting
``output_kept = true``, and N-C1 (``custom.record_write_graph_superseding``, chairdoors2_i) writes
them by these exact keys (``output_state`` ∈ ``draft`` / ``superseded``, ``output_chain``,
``output_generation``, ``output_reason``, ``output_kept``, ``output_out_of_date``,
``output_replaced_by`` as a relation). Their labels are PROVISIONAL (design §12: no screen string
ships before the chair's vocabulary approval); they live in :data:`PROVISIONAL_LABELS`.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

__all__ = [
    "AGENT_OUTPUT",
    "CHILD_TABLE_SPEC",
    "KindEdgeSpec",
    "KindField",
    "KindFieldsRefused",
    "PLATFORM_KEYS",
    "PROVISIONAL_LABELS",
    "SELF",
    "declarations_for",
    "fields_for_kind",
    "record_values_for",
    "title_field_for",
    "value_from_record",
]

AGENT_OUTPUT = "agent_output"
#: A relation whose target is the table being declared.
SELF = "__self__"
#: The table-level fact a CHILD kind's output table is ensured with: its records are contained.
CHILD_TABLE_SPEC: dict[str, Any] = {"contained_by_relation": True}

_KIND_KEY = "__kind"
_MAX_KEY = 48
_LONG_TEXT_FROM = 500
#: The seeded default of ``records.children.fan_out_ceiling``: a many-relation's ceiling.
_DEFAULT_CHILDREN_CEILING = 500

PLATFORM_KEYS: tuple[str, ...] = (
    "output_state",
    "output_kept",
    "output_out_of_date",
    "output_chain",
    "output_generation",
    "output_replaced_by",
    "output_reason",
    "output_conversation",
    "output_conversation_id",
    "output_agent",
    "output_turn",
    "output_kept_into",
    "output_leftover",
)

#: Screen strings, provisional until the chair's vocabulary approval (design §12).
PROVISIONAL_LABELS: dict[str, str] = {
    "output_state": "State",
    "output_kept": "Kept",
    "output_out_of_date": "Out of date",
    "output_chain": "Series",
    "output_generation": "Version",
    "output_replaced_by": "Replaced by",
    "output_reason": "Reason",
    "output_conversation": "Conversation",
    "output_conversation_id": "Conversation ID",
    "output_agent": "Agent",
    "output_turn": "Turn",
    "output_kept_into": "Kept in",
    "output_leftover": "Unplaced values",
}

#: N-C1's values, verbatim (chairdoors2_i writes ``draft`` and ``superseded``).
_STATES = ["draft", "superseded"]
_REASONS = [
    "first",
    "continued",
    "regenerated",
    "rewound",
    "edited",
    "agent_replaces",
    "agent_new",
    "same_turn_sibling",
    "branched",
    "moved",
    "split",
    "migrated",
]


class KindFieldsRefused(ValueError):
    """A kind value cannot be placed in its table's Fields; nothing should be written."""


@dataclass(frozen=True)
class KindEdgeSpec:
    """One owned ``content_ir.kind_edge`` row: ``field_name`` holds records of ``child_kind``."""

    field_name: str
    child_kind: str
    position: int | None = None


@dataclass(frozen=True)
class KindField:
    """One Field of an output table: a ``custom.field_declare`` spec, its target still a kind."""

    declaration: dict[str, Any]
    #: A relation's target: a child kind, or :data:`SELF`. ``None`` for every other Field.
    child_kind: str | None = None

    @property
    def key(self) -> str:
        return str(self.declaration["key"])


# --------------------------------------------------------------------------- schema reading


def _resolve(root: Mapping[str, Any], node: Any, depth: int = 0) -> dict[str, Any]:
    """Follow a local ``$ref`` and drop a ``null`` branch, so what is left is the value's shape."""
    if not isinstance(node, Mapping) or depth > 16:
        return {}
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/"):
        target: Any = root
        for part in ref[2:].split("/"):
            target = target.get(part) if isinstance(target, Mapping) else None
        merged = {k: v for k, v in node.items() if k != "$ref"}
        return {**_resolve(root, target, depth + 1), **merged}
    for union in ("anyOf", "oneOf"):
        branches = node.get(union)
        if isinstance(branches, list):
            live = [b for b in branches if not (isinstance(b, Mapping) and b.get("type") == "null")]
            if len(live) == 1:
                rest = {k: v for k, v in node.items() if k != union}
                return {**_resolve(root, live[0], depth + 1), **rest}
    out = dict(node)
    t = out.get("type")
    if isinstance(t, list):
        live_types = [x for x in t if x != "null"]
        if len(live_types) == 1:
            out["type"] = live_types[0]
    return out


def _string_enum(shape: Mapping[str, Any]) -> list[str] | None:
    values = shape.get("enum")
    if isinstance(values, list) and values and all(isinstance(v, str) and v for v in values):
        return list(dict.fromkeys(values))
    return None


# --------------------------------------------------------------------------- keys and labels


def _fit(key: str) -> str:
    if len(key) <= _MAX_KEY:
        return key
    return f"{key[:39]}_{hashlib.sha1(key.encode()).hexdigest()[:8]}"


def _store_key(name: str) -> str:
    snake = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()
    snake = re.sub(r"[^a-z0-9]+", "_", snake).strip("_")
    if not snake or not snake[0].isalpha():
        snake = f"f_{snake}"
    return _fit(snake)


def _label(name: str) -> str:
    words = re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", name).replace("_", " ").split()
    text = " ".join(words).lower()
    return text[:1].upper() + text[1:] if text else name


# --------------------------------------------------------------------------- one property


def _value_field(root: Mapping[str, Any], shape: Mapping[str, Any]) -> dict[str, Any]:
    """The declaration of a property that is not a child list (design §2.3's table)."""
    t = shape.get("type")
    options = _string_enum(shape)
    if options is not None:
        return {"type": "select", "options": options}
    if t == "array":
        items = _string_enum(_resolve(root, shape.get("items")))
        if items is not None:
            return {"type": "multi_select", "options": items}
    if t == "string":
        fmt = shape.get("format")
        if fmt == "email":
            return {"type": "email"}
        if fmt in ("uri", "url", "iri"):
            return {"type": "url"}
        if fmt in ("date", "date-time"):
            return {"type": "datetime", "kind": "date" if fmt == "date" else "datetime"}
        long = shape.get("maxLength")
        if (isinstance(long, int) and long > _LONG_TEXT_FROM) or shape.get("x-multiline") is True or fmt in (
            "textarea",
            "markdown",
        ):
            return {"type": "long_text"}
        return {"type": "text"}
    if t in ("number", "integer"):
        unit = shape.get("x-matrx-unit")
        if isinstance(unit, str) and unit.strip().lower() in ("%", "percent"):
            return {"type": "percent"}
        if isinstance(unit, str) and unit.strip():
            return {"type": "currency", "unit": unit.strip()}
        return {"type": "number"}
    if t == "boolean":
        return {"type": "checkbox"}
    return {"type": "long_text", "config": {"holds_json": True}}


# --------------------------------------------------------------------------- the Fields


def _platform_fields() -> list[KindField]:
    agent = {"kept_by": AGENT_OUTPUT}
    specs: dict[str, dict[str, Any]] = {
        "output_state": {"type": "select", "options": list(_STATES)},
        "output_kept": {"type": "checkbox"},
        "output_out_of_date": {"type": "checkbox"},
        "output_chain": {"type": "text"},
        "output_generation": {"type": "number"},
        "output_replaced_by": {"type": "relation", "relation_max": 1},
        "output_reason": {"type": "select", "options": list(_REASONS)},
        "output_conversation": {"type": "text"},
        "output_conversation_id": {"type": "text"},
        "output_agent": {"type": "text"},
        "output_turn": {"type": "number"},
        "output_kept_into": {"type": "text"},
        "output_leftover": {"type": "long_text"},
    }
    out: list[KindField] = []
    for i, key in enumerate(PLATFORM_KEYS):
        spec = specs[key]
        declaration = {
            "key": key,
            "label": PROVISIONAL_LABELS[key],
            "sort": 10_000 + 10 * i,
            "required": False,
            **spec,
            "config": dict(agent),
        }
        out.append(KindField(declaration, child_kind=SELF if spec["type"] == "relation" else None))
    return out


def _edges(edges: Sequence[KindEdgeSpec | Mapping[str, Any]]) -> dict[str, list[str]]:
    """field -> its child kinds, in the edge's position order (then name)."""
    rows: list[tuple[str, int, str]] = []
    for e in edges:
        if isinstance(e, KindEdgeSpec):
            field, child, pos = e.field_name, e.child_kind, e.position
        else:
            field, child, pos = e.get("field_name"), e.get("child_kind"), e.get("position")
        if isinstance(field, str) and field and isinstance(child, str) and child:
            rows.append((field, pos if isinstance(pos, int) else 0, child))
    rows.sort(key=lambda r: (r[1], r[2]))
    by_field: dict[str, list[str]] = {}
    for field, _, child in rows:
        members = by_field.setdefault(field, [])
        if child not in members:
            members.append(child)
    return by_field


def fields_for_kind(
    schema: Mapping[str, Any],
    edges: Sequence[KindEdgeSpec | Mapping[str, Any]] = (),
    *,
    kind: str | None = None,
    children_ceiling: int = _DEFAULT_CHILDREN_CEILING,
) -> list[KindField]:
    """Every Field of this kind's output table: the kind's own, then the platform Fields.

    ``schema`` is the kind's emitted JSON Schema (``content_ir.kind_definition.emitted_json_schema``);
    ``edges`` its owned ``kind_edge`` rows. A field with edges gets ONE relation Field PER CHILD
    KIND (``cards`` → ``cards__flashcard``, ``cards__enhanced_flashcard`` …): one relation Field
    targets one Table, so a union needs one Field per member. Given ``kind``, an edge back to the
    kind itself (``decision_node.yes``) targets :data:`SELF`.
    """
    root = _resolve(schema, schema)
    properties = root.get("properties") if isinstance(root.get("properties"), Mapping) else {}
    by_field = _edges(edges)
    taken: set[str] = set(PLATFORM_KEYS)
    out: list[KindField] = []

    def claim(key: str) -> str:
        candidate, n = key, 2
        while candidate in taken:
            candidate = _fit(f"{key}_{n}")
            n += 1
        taken.add(candidate)
        return candidate

    sort = 0
    for name, raw in (properties or {}).items():
        if not isinstance(name, str) or name == _KIND_KEY or name.startswith("_"):
            continue
        shape = _resolve(schema, raw)
        sort += 10
        children = by_field.get(name)
        if children:
            many = shape.get("type") == "array"
            for child in children:
                key = claim(_fit(f"{_store_key(name)}__{_store_key(child)}"))
                declaration = {
                    "key": key,
                    "label": f"{_label(name)} ({_label(child).lower()})" if len(children) > 1 else _label(name),
                    "sort": sort,
                    "required": False,
                    "type": "relation",
                    "multi": many,
                    "relation_max": max(1, children_ceiling) if many else 1,
                    "config": {"kind_key": name, "child_kind": child, "kind_many": many},
                }
                out.append(KindField(declaration, child_kind=SELF if kind is not None and child == kind else child))
            continue
        spec = _value_field(schema, shape)
        config = {"kind_key": name, **spec.pop("config", {})}
        out.append(
            KindField(
                {
                    "key": claim(_store_key(name)),
                    "label": _label(name),
                    "sort": sort,
                    "required": False,
                    **spec,
                    "config": config,
                }
            )
        )
    platform = _platform_fields()
    return _unique_labels(out, platform) + platform


def _label_norm(label: str) -> str:
    return " ".join(label.split()).lower()


def _unique_labels(own: list[KindField], platform: Sequence[KindField]) -> list[KindField]:
    """THE STORE REFUSES TWO COLUMNS WITH ONE LABEL (``You already have a column called "Reason"``).

    A kind property titled ``reason`` collided with the platform ``Reason`` Field, so every
    ``brand_basics`` output was refused and NOTHING WAS STORED (MKT-161). The platform labels are
    reserved first; a kind's own Field whose label is already taken (by a platform Field or an
    earlier one) is told apart with a number: ``Reason (2)``. Keys are untouched.
    """
    seen = {_label_norm(str(f.declaration["label"])) for f in platform}
    for f in own:
        label = str(f.declaration["label"])
        candidate, n = label, 2
        while _label_norm(candidate) in seen:
            candidate = f"{label} ({n})"
            n += 1
        seen.add(_label_norm(candidate))
        f.declaration["label"] = candidate
    return own


def declarations_for(
    fields: Sequence[KindField], targets: Mapping[str, str], *, self_table_id: str | None = None
) -> list[dict[str, Any]]:
    """``custom.field_declare`` specs with every relation's target resolved.

    ``targets`` maps a child kind to its output table id. A relation whose target is not known yet
    (a :data:`SELF` relation before the table exists) is left out — the lander ensures again once
    it is known. A child kind with no table is a ``KeyError``: never a Field silently missing.
    """
    out: list[dict[str, Any]] = []
    for f in fields:
        if f.child_kind is None:
            out.append(dict(f.declaration))
            continue
        target = self_table_id if f.child_kind == SELF else targets[f.child_kind]
        if target is None:
            continue
        out.append({**f.declaration, "relation_target": target})
    return out


def title_field_for(fields: Sequence[KindField]) -> str:
    """The Field a record of this table is called by: ``title``, else the first plain text."""
    kinds = [f for f in fields if f.child_kind is None and _config(f.declaration).get("kept_by") != AGENT_OUTPUT]
    for f in kinds:
        if f.key in ("title", "name"):
            return f.key
    for f in kinds:
        if f.declaration.get("type") == "text":
            return f.key
    return kinds[0].key if kinds else "output_agent"


# --------------------------------------------------------------------------- values <-> records


def _config(field: Mapping[str, Any]) -> Mapping[str, Any]:
    cfg = field.get("config")
    return cfg if isinstance(cfg, Mapping) else {}


def record_values_for(
    value: Mapping[str, Any], fields: Sequence[Mapping[str, Any]]
) -> tuple[dict[str, Any], list[tuple[str, int, dict[str, Any]]]]:
    """Split a kind value into its record's values and its contained records.

    ``fields`` are Field documents (a declaration, or a table's read-back Fields). Answers
    ``(values, children)`` where each child is ``(relation field key, position, child value)``.
    A list item whose ``__kind`` no relation Field of its property holds, and a property with no
    Field, are REFUSED by name — the caller files them (``output_leftover``), never drops them.
    """
    by_kind_key: dict[str, list[Mapping[str, Any]]] = {}
    for f in fields:
        if _config(f).get("kept_by") == AGENT_OUTPUT:
            continue
        kind_key = _config(f).get("kind_key")
        if isinstance(kind_key, str):
            by_kind_key.setdefault(kind_key, []).append(f)
    values: dict[str, Any] = {}
    children: list[tuple[str, int, dict[str, Any]]] = []
    for name, item in value.items():
        if name == _KIND_KEY or name.startswith("_"):
            continue
        owners = by_kind_key.get(name)
        if not owners:
            raise KindFieldsRefused(f"{name!r} has no Field in this table")
        relations = {str(_config(f).get("child_kind")): f for f in owners if _config(f).get("child_kind")}
        if relations:
            items = item if isinstance(item, list) else ([] if item is None else [item])
            for position, child in enumerate(items):
                if not isinstance(child, Mapping):
                    raise KindFieldsRefused(f"item {position} of {name!r} is not a record")
                child_kind = child.get(_KIND_KEY)
                if child_kind is None and len(relations) == 1:
                    child_kind = next(iter(relations))
                owner = relations.get(str(child_kind))
                if owner is None:
                    raise KindFieldsRefused(
                        f"item {position} of {name!r} is a {child_kind!r}, and no Field of this table holds one"
                    )
                children.append((str(owner["key"]), position, dict(child)))
            continue
        owner = owners[0]
        values[str(owner["key"])] = json.dumps(item) if _config(owner).get("holds_json") is True else item
    return values, children


def value_from_record(
    values: Mapping[str, Any],
    children: Sequence[tuple[str, int, Mapping[str, Any]]],
    fields: Sequence[Mapping[str, Any]],
    *,
    kind: str | None = None,
) -> dict[str, Any]:
    """The kind value a record and its contained records stand for (the inverse of the split)."""
    out: dict[str, Any] = {_KIND_KEY: kind} if kind else {}
    by_key = {str(f.get("key")): f for f in fields}
    for key, item in values.items():
        f = by_key.get(key)
        if f is None or _config(f).get("kept_by") == AGENT_OUTPUT:
            continue
        name = str(_config(f).get("kind_key") or key)
        out[name] = json.loads(item) if _config(f).get("holds_json") is True and isinstance(item, str) else item
    grouped: dict[str, list[tuple[int, Mapping[str, Any]]]] = {}
    many: dict[str, bool] = {}
    for key, position, child in children:
        f = by_key.get(key)
        if f is None:
            raise KindFieldsRefused(f"a contained record names {key!r}, which is no Field of this table")
        name = str(_config(f).get("kind_key") or key)
        grouped.setdefault(name, []).append((position, child))
        many[name] = many.get(name, False) or _config(f).get("kind_many") is True
    for name, items in grouped.items():
        ordered = [dict(c) for _, c in sorted(items, key=lambda pc: pc[0])]
        out[name] = ordered if many[name] else ordered[0]
    return out
