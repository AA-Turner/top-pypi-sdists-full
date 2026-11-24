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
    "STORE_STRUCTURE_KEYS",
    "PROVISIONAL_LABELS",
    "SELF",
    "ChildRelation",
    "child_relations",
    "declarations_for",
    "fields_for_kind",
    "output_kind_of",
    "table_kind_binding_of",
    "bound_kind_value",
    "bound_link_ids",
    "bound_through_reads",
    "coerce_link_fields",
    "LinkFieldRefused",
    "LINKED_RECORD",
    "record_kind_value",
    "related_ids",
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
    # The run that produced the row (its request id), stamped by the chain door: one run, one row.
    "output_run",
)

#: Keys the record store READS as structure in every record's document, never as a column: ``parent_id`` is the
#: record's containment parent (``custom.containment_parent`` casts it to uuid on every write). A kind property of
#: that name (``content_plan_node.parent_id``, a plan's own node label) written under it either fails the whole write
#: (22P02 — nothing stored) or, when it happens to be a uuid, silently moves the record inside another one. Such a
#: property gets its own column under a free key (``parent_id_2``), mapped back by ``config.kind_key``.
#: (``from``/``to``/``carrying`` are structure only on relation records; ``custom.record_carrying_edges`` casts them
#: only there since 2026-11-17, so a kind's ``to`` stays ``to``.)
STORE_STRUCTURE_KEYS: tuple[str, ...] = ("parent_id",)

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
    "output_run": "Run",
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


def shared_choices_marker(key: str) -> str:
    """The marker the store finds a platform choice column's one per-organization choices set by."""
    return f"{AGENT_OUTPUT}.{key}"


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
        "output_run": {"type": "text"},
    }
    out: list[KindField] = []
    for i, key in enumerate(PLATFORM_KEYS):
        spec = specs[key]
        config = dict(agent)
        if spec.get("options"):
            # #91: ONE choices set per organization for each platform choice column — the store's
            # custom._options_table_shared_or_new finds or makes it by this marker, never a
            # "State choices" / "Reason choices" table per output table.
            config["shared_choices"] = shared_choices_marker(key)
        declaration = {
            "key": key,
            "label": PROVISIONAL_LABELS[key],
            "sort": 10_000 + 10 * i,
            "required": False,
            **spec,
            "config": config,
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
    taken: set[str] = set(PLATFORM_KEYS) | set(STORE_STRUCTURE_KEYS)
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


# --------------------------------------------------------------------------- a record as its kind
#
# B2 of the kinds connection (common-docs ``systems/data/custom-data/projects/data-for-every-client/discovery/K-kinds-connection.md``
# §7): a record id -> the kind value it stands for, as the viewer. The READS are the store's
# (``matrx_records`` ``RecordStore.record_as_kind``, ``@ai-matrx/records`` ``recordAsKind``); what
# is decided from what was read is here, PURE, and twinned byte-for-byte by ``@ai-matrx/records``
# ``src/kind-fields.ts`` (golden ``tests/fixtures/record_as_kind_golden.json``). The access check
# stays the store's: a value the read door masked is handed in as withheld and never shown.


@dataclass(frozen=True)
class ChildRelation:
    """A relation Field of an output table that holds contained records of ``child_kind``."""

    key: str
    kind_key: str
    child_kind: str
    #: The child output table (the Field's ``relation_target``); ``None`` when the Field has none.
    target_table_id: str | None
    many: bool


def output_kind_of(table_document: Mapping[str, Any] | None) -> str | None:
    """The registry kind an OUTPUT table holds (``kept_for = agent_output`` + ``kind``), else None.

    Read from the Table's own document (``custom.read_record`` of the Table record), the one
    place ``land.py`` writes it. Any other table answers None: its records are ``table:<uuid>``.
    """
    if not isinstance(table_document, Mapping) or table_document.get("kept_for") != AGENT_OUTPUT:
        return None
    kind = table_document.get("kind")
    return kind if isinstance(kind, str) and kind.strip() else None


def table_kind_binding_of(facts: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """An ORDINARY table's bound kind (PF-4) from the facts door's ``kind_binding``, else None.

    ``{kind, fields, required, problem}``: the registered kind an owner chose (``custom.table_kind_set``),
    ``{<kind field>: <column key>}``, what the kind requires today (read live), and a plain sentence
    when the kind is no longer registered or is turned off. The twin of TS ``tableKindBindingOf``.
    """
    raw = facts.get("kind_binding") if isinstance(facts, Mapping) else None
    if not isinstance(raw, Mapping):
        return None
    kind = raw.get("kind").strip() if isinstance(raw.get("kind"), str) else ""
    mapping = raw.get("fields")
    if not kind or not isinstance(mapping, Mapping):
        return None
    fields = {
        str(name): column
        for name, column in mapping.items()
        if isinstance(column, str) and column and name != _KIND_KEY and not str(name).startswith("_")
    }
    fact_fields = facts.get("fields") if isinstance(facts, Mapping) else None
    through, record_id_fields = _followed_fields_of(mapping, fact_fields)
    required_raw = raw.get("required")
    required = (
        [k for k in required_raw if isinstance(k, str) and k != _KIND_KEY] if isinstance(required_raw, list) else []
    )
    problem = raw.get("problem")
    problem = problem if isinstance(problem, str) and problem.strip() else None
    binding: dict[str, Any] = {"kind": kind, "fields": fields, "required": required, "problem": problem}
    links = _link_columns_of(fields, fact_fields)
    if links:
        binding["links"] = links
    if through:
        binding["through"] = through
    if record_id_fields:
        binding["record_id_fields"] = record_id_fields
    return binding


def _followed_fields_of(mapping: Mapping[str, Any], fact_fields: Any) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """The kind fields bound to something other than one of the row's own columns (PF-GAUNTLET #98):

    * ``{"link": <link column>, "field": <key>}`` — a field ON THE LINKED RECORD (``Door › Owner repair approval
      limit``). Kept only when the link column is a record link of this table (a ``relation`` Field without
      ``allowed_types``); ``table_id`` is the Table it points at (``relation_target``), ``None`` when unsaid.
    * ``{"record_id": true}`` — the row's own record id.

    Twin of TS ``followedFieldsOf``.
    """
    through: dict[str, dict[str, Any]] = {}
    record_id_fields: list[str] = []
    by_key = (
        {str(f.get("key")): f for f in fact_fields if isinstance(f, Mapping)} if isinstance(fact_fields, list) else {}
    )
    for name, target in mapping.items():
        name = str(name)
        if not isinstance(target, Mapping) or name == _KIND_KEY or name.startswith("_"):
            continue
        if target.get("record_id") is True:
            record_id_fields.append(name)
            continue
        link, field = target.get("link"), target.get("field")
        if not (isinstance(link, str) and link and isinstance(field, str) and field):
            continue
        f = by_key.get(link)
        if f is None or f.get("type") != "relation":
            continue
        allowed = _config(f).get("allowed_types")
        if isinstance(allowed, list) and allowed:
            continue
        table_id = f.get("relation_target")
        through[name] = {"link": link, "field": field, "table_id": table_id if isinstance(table_id, str) and table_id else None}
    return through, record_id_fields


#: What a linked cell reads when its words could not be read. Never the id. Twin of TS ``LINKED_RECORD``.
LINKED_RECORD = "Linked record"


def _link_columns_of(mapped: Mapping[str, str], fact_fields: Any) -> dict[str, str | None]:
    """The mapped columns that are LINKS: ``{column: link Field id | None}`` (None = the relation door cannot say
    the words, a link to a platform record). Twin of TS ``linkColumnsOf``."""
    out: dict[str, str | None] = {}
    if not isinstance(fact_fields, list):
        return out
    by_key = {str(f.get("key")): f for f in fact_fields if isinstance(f, Mapping)}
    for column in dict.fromkeys(mapped.values()):
        f = by_key.get(column)
        if f is None or f.get("type") != "relation":
            continue
        allowed = _config(f).get("allowed_types")
        fid = f.get("id")
        out[column] = fid if isinstance(fid, str) and fid and not (isinstance(allowed, list) and allowed) else None
    return out


def _link_item_id(item: Any) -> str | None:
    """The id one link item names: a bare id, an ``{id}`` pair, or a relation address (``_record_id`` / ``id``).
    Twin of TS ``linkItemId``."""
    if isinstance(item, str):
        return item
    if not isinstance(item, Mapping):
        return None
    i = item.get("_record_id")
    if i is None:
        i = item.get("id")
    return i if isinstance(i, str) else None


def _link_ids_of(value: Any) -> list[str]:
    items = value if isinstance(value, list) else ([] if value is None or value == "" else [value])
    ids: list[str] = []
    for item in items:
        i = _link_item_id(item)
        if isinstance(i, str) and i.strip():
            ids.append(i.strip())
    return ids


_RECORD_ID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


class LinkFieldRefused(ValueError):
    """A value bound to a link column names no record; the message is the sentence the person reads."""


def _shape_words(value: Any) -> str:
    if isinstance(value, list):
        return "a list holding something that is not a record"
    if isinstance(value, Mapping):
        return "an object that names no record"
    if isinstance(value, str):
        return f'"{value[:40]}…"' if len(value) > 40 else f'"{value}"'
    if isinstance(value, bool):
        return "a boolean"
    if isinstance(value, int | float):
        return "a number"
    return f"a {type(value).__name__}"


def coerce_link_fields(fields: Any, row: Mapping[str, Any]) -> dict[str, Any]:
    """A row about to be written, with every value bound to a LINK column (a ``relation`` Field pointing at
    records) turned into what the store's write door takes for a link: the record id, or a list of ids.

    Accepted: a bare id, a list of ids, ``{id}`` pairs, a relation address (``{__kind: "relation", token:
    "record", _record_id | id}``) and a source row's own link cell — the one link-cell reading
    (:func:`bound_link_ids`). An empty value (None, "", []) stays as written. A value naming no record raises
    :class:`LinkFieldRefused` with a sentence naming the field; nothing is guessed. Non-link columns and
    entity-reference relations (``config.allowed_types``, which take ``{token, id}``) are left as given.
    Twin of TS ``coerceLinkFields``.
    """
    out = dict(row)
    if not isinstance(fields, list):
        return out
    for field in fields:
        if not isinstance(field, Mapping):
            continue
        key = field.get("key")
        if not isinstance(key, str) or not key or key not in row or field.get("type") != "relation":
            continue
        allowed = _config(field).get("allowed_types")
        if isinstance(allowed, list) and allowed:
            continue
        value = row[key]
        if value is None or value == "" or (isinstance(value, list) and not value):
            continue
        items = value if isinstance(value, list) else [value]
        ids: list[str] = []
        for item in items:
            i = (_link_item_id(item) or "").strip()
            if not _RECORD_ID.match(i):
                label = field.get("label") if isinstance(field.get("label"), str) and field.get("label") else key
                raise LinkFieldRefused(
                    f"{label} links to a record, and it was given "
                    f"{_shape_words(value if isinstance(value, list) else item)}, which is not a record. Nothing was saved."
                )
            ids.append(i)
        out[key] = ids if isinstance(value, list) else ids[0]
    return out


def bound_link_ids(
    binding: Mapping[str, Any], documents: Sequence[Mapping[str, Any]], withheld: Sequence[str] = ()
) -> dict[str, list[str]]:
    """Link Field id -> the linked record ids across these rows, de-duplicated: ONE batched ask per Field."""
    out: dict[str, list[str]] = {}
    links = binding.get("links") or {}
    for column in (binding.get("fields") or {}).values():
        field_id = links.get(column)
        if not field_id or column in withheld:
            continue
        seen = dict.fromkeys(out.get(field_id, []))
        for d in documents:
            seen.update(dict.fromkeys(_link_ids_of(d.get(column))))
        if seen:
            out[field_id] = list(seen)
    return out


def bound_through_reads(
    binding: Mapping[str, Any], documents: Sequence[Mapping[str, Any]], withheld: Sequence[str] = ()
) -> dict[str, dict[str, Any]]:
    """Link column -> ``{table_id, ids}``: the linked records these rows' followed fields read, de-duplicated —
    ONE batched read per link column, through the store's read door as the reader. A withheld link column, or one
    whose Table is unsaid, is never followed. Twin of TS ``boundThroughReads``."""
    out: dict[str, dict[str, Any]] = {}
    for spec in (binding.get("through") or {}).values():
        column, table_id = spec.get("link"), spec.get("table_id")
        if not column or not table_id or column in withheld or column in out:
            continue
        seen: dict[str, None] = {}
        for d in documents:
            seen.update(dict.fromkeys(_link_ids_of(d.get(column))))
        if seen:
            out[column] = {"table_id": table_id, "ids": list(seen)}
    return out


def bound_kind_value(
    binding: Mapping[str, Any],
    document: Mapping[str, Any],
    withheld: Sequence[str] = (),
    words: Mapping[str, Mapping[str, str]] | None = None,
    linked: Mapping[str, Mapping[str, Mapping[str, Any]]] | None = None,
    record_id: str | None = None,
) -> dict[str, Any]:
    """A row of a bound table as its kind value: ``{"value": {...}, "missing": [...]}`` (PF-4).

    Only mapped fields are built, under ``__kind`` = the bound slug; an empty value (absent, None, "")
    and a ``withheld`` column are left out; every required field left out is named in ``missing``.
    A field bound to ``<link> › <field>`` reads that field of the linked record from ``linked``
    (``{link column: {record id: the linked document as this reader read it}}``, see :func:`bound_through_reads`):
    one link gives its value, several give the list of values; a withheld link, an unread record or an empty
    value leaves it out. A field bound to the record id reads ``record_id``.
    The twin of TS ``boundKindValue``.
    """
    hidden = set(withheld)
    value: dict[str, Any] = {_KIND_KEY: binding["kind"]}
    for name, column in (binding.get("fields") or {}).items():
        if column in hidden:
            continue
        item = document.get(column)
        if item is None or item == "":
            continue
        links = binding.get("links") or {}
        if column in links:
            # A LINK reads as the linked row's words (many join with ", "); unread words leave "Linked record", never the id.
            ids = _link_ids_of(item)
            if not ids:
                continue
            named = (words or {}).get(links[column] or "") or {}
            value[name] = ", ".join(named.get(i) or LINKED_RECORD for i in ids)
            continue
        value[name] = item
    for name, spec in (binding.get("through") or {}).items():
        column = spec.get("link")
        if not column or column in hidden:
            continue
        ids = _link_ids_of(document.get(column))
        read = (linked or {}).get(column) or {}
        found = [
            v
            for v in ((read.get(i) or {}).get(spec.get("field")) for i in ids)
            if v is not None and v != "" and v != []
        ]
        if found:
            value[name] = found[0] if len(ids) == 1 else found
    if record_id:
        for name in binding.get("record_id_fields") or []:
            value[name] = record_id
    missing = [k for k in binding.get("required") or [] if k not in value]
    return {"value": value, "missing": missing}


def child_relations(fields: Sequence[Mapping[str, Any]]) -> list[ChildRelation]:
    """Every Field that holds contained records, in the table's Field order."""
    out: list[ChildRelation] = []
    for f in fields:
        cfg = _config(f)
        child = cfg.get("child_kind")
        if cfg.get("kept_by") == AGENT_OUTPUT or not isinstance(child, str) or not child:
            continue
        target = f.get("relation_target")
        out.append(
            ChildRelation(
                key=str(f.get("key")),
                kind_key=str(cfg.get("kind_key") or f.get("key")),
                child_kind=child,
                target_table_id=str(target) if isinstance(target, str) and target else None,
                many=cfg.get("kind_many") is True,
            )
        )
    return out


def related_ids(document: Mapping[str, Any], relation: ChildRelation) -> list[str]:
    """The contained record ids a document's relation Field holds, in their stored order."""
    raw = document.get(relation.key)
    items = raw if isinstance(raw, list) else ([] if raw is None else [raw])
    return [str(i) for i in items if isinstance(i, str) and i]


def record_kind_value(
    facts: Mapping[str, Any],
    document: Mapping[str, Any],
    *,
    kind: str | None = None,
    children: Sequence[tuple[str, int, Mapping[str, Any]]] = (),
    withheld: Sequence[str] = (),
) -> dict[str, Any]:
    """The kind value one record stands for, from its Table's facts and its read document.

    ``kind`` (an output table's registry kind, :func:`output_kind_of`) rebuilds the registry
    value through :func:`value_from_record`; the relation Fields that hold contained records
    are answered by ``children`` (each already a kind value), never by their ids. Without it the
    record is a record of its Table: ``{"__kind": "table:<table id>", ...its values}``.
    ``withheld`` are the keys the read door masked for this viewer: they are left out, never
    shown as a value. Keys starting with ``_`` (the door's ``_hidden``, ``_values``…) are never values.
    """
    hidden = set(withheld)
    fields = [f for f in facts.get("fields") or [] if isinstance(f, Mapping)]
    if kind:
        held_by_children = {r.key for r in child_relations(fields)}
        values = {
            k: v
            for k, v in document.items()
            if not k.startswith("_") and k not in hidden and k not in held_by_children
        }
        return value_from_record(values, children, fields, kind=kind)
    from matrx_graph.table_kinds import table_kind_slug

    out: dict[str, Any] = {_KIND_KEY: table_kind_slug(str(facts["table_id"]))}
    for k, v in document.items():
        if not k.startswith("_") and k not in hidden:
            out[k] = v
    return out
