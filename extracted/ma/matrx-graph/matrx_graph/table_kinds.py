"""A table is a kind: ``table:<uuid>`` and the three schemas derived from its Fields.

KINDS-GLUE wave 3 §1–2 (common-docs ``projects/data-doctrine-adoption/v6/KINDS-GLUE-WAVE3-DESIGN.md``).
``table:<uuid>`` names "a record of that Table". It is never a registry row: its schema is
derived, at the moment it is asked for, from the Table's live Fields as the store's door
``custom.table_kind_facts`` (N1) answers them. :class:`TableKindFacts` is that door's JSON
verbatim — same keys, no reshaping.

ONE MAPPING, THREE OUTPUTS. ``table_kind_mapping.json`` (a verbatim copy of
``@ai-matrx/records`` ``src/table-kind-mapping.json``; ``scripts/generate_table_kind_mapping.py
--check`` keeps them equal) decides, per field kind:

* **stored** — the JSON Schema a value is validated against in Python (mirrors
  ``custom.validate_values``: types, nulls, list membership, relation id shape and ceiling, the
  date cast, the type field's required Fields; and ``custom._undeclared_key_guard``: closed only
  on a ``fields`` Table, ``custom.record_platform_keys()`` always allowed). Never sent to a
  provider. Uses the door's ``column_source`` / ``platform_keys`` / per-Field ``field_kind``
  when it carries them, else derives them (``fields``, the mapping's keys, ``field_kind_of``).
* **authored** — a plain object every provider binds: no ``allOf`` / ``if`` /
  ``patternProperties``; computed, signature and attachment Fields omitted.
* **render** — the content-ir ``KindSchema`` the web draws with; never stricter than the store.

Each is Fields-only here (``json_schema_for`` / ``render_schema_for``); the control keys are
wave 2's one function (``kind_control_keys``), applied by ``stored_schema`` /
``authored_schema`` / ``render_schema``. The TypeScript twin is ``@ai-matrx/records``
``src/table-kind.ts``; both produce byte-identical JSON for the golden fixture (guard 3 (a)).
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Mapping
from functools import cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from matrx_graph.kind_control_keys import with_control_key_fields, with_control_keys

__all__ = [
    "TABLE_KIND_PREFIX",
    "TableKindFacts",
    "TableKindRefused",
    "authored_schema",
    "field_kind_of",
    "is_table_kind",
    "json_schema_for",
    "render_schema",
    "render_schema_for",
    "stored_schema",
    "table_id_of",
    "table_kind_mapping",
    "table_kind_slug",
]

TABLE_KIND_PREFIX = "table:"
_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
_KIND_KEY = "__kind"


class TableKindRefused(Exception):
    """The store refused to answer a Table's facts; ``sentence`` is the store's own words."""

    def __init__(self, sentence: str) -> None:
        super().__init__(sentence)
        self.sentence = sentence


class TableKindFacts(BaseModel):
    """``custom.table_kind_facts(p_table_id)`` verbatim (N1). Unknown keys are kept."""

    model_config = ConfigDict(extra="allow", frozen=True)

    organization_id: str
    table_id: str
    name: str | None = None
    title_field: str | None = None
    agent_writable: bool = True
    purpose: str | None = None
    version: int | None = None
    type_field: str | None = None
    stamp: str | None = None
    fields: list[dict[str, Any]] = []
    choices: dict[str, list[dict[str, Any]]] = {}
    #: ``custom.table_column_source`` (``fields`` / ``free_form`` / ``code``) once the door carries
    #: it; absent, the mapping's default (``fields``: the Field rows are the columns).
    column_source: str | None = None
    #: ``custom.record_platform_keys()`` once the door carries it; absent, the mapping's keys.
    platform_keys: list[str] | None = None


def is_table_kind(slug: object) -> bool:
    """``table:`` + a lowercase canonical uuid."""
    return (
        isinstance(slug, str)
        and slug.startswith(TABLE_KIND_PREFIX)
        and bool(_UUID.match(slug[len(TABLE_KIND_PREFIX) :]))
    )


def table_kind_slug(table_id: str) -> str:
    slug = TABLE_KIND_PREFIX + str(table_id).strip().lower()
    if not is_table_kind(slug):
        raise ValueError(f"{table_id!r} is not a table id")
    return slug


def table_id_of(slug: str) -> str:
    if not is_table_kind(slug):
        raise ValueError(f"{slug!r} is not a table kind")
    return slug[len(TABLE_KIND_PREFIX) :]


@cache
def table_kind_mapping() -> dict[str, Any]:
    """The one mapping (a verbatim copy of the records package's file)."""
    return json.loads((Path(__file__).parent / "table_kind_mapping.json").read_text())


# --------------------------------------------------------------------------- field kinds


def _truthy(value: object) -> bool:
    return value is True or value == "true"


def _parity_type(d: Mapping[str, Any]) -> str | None:
    """Twin of ``custom.parity_type`` — the first answer wins."""
    m = table_kind_mapping()
    t, fmt = d.get("type"), d.get("format")
    cfg = d.get("config") if isinstance(d.get("config"), dict) else {}
    if t == "boolean":
        return "checkbox"
    if t == "list":
        return "multi_select" if _truthy(d.get("multi")) else "select"
    if t == "relation" and d.get("relation_target") == m["kernels"]["file"]:
        return "attachment"
    if t == "relation" and d.get("relation_target") == m["kernels"]["person"]:
        return "member"
    if t == "formula" and "pick" in cfg:
        return "lookup"
    if t == "formula" and "agg" in cfg:
        return "rollup"
    if t == "formula" and "expr" in cfg:
        return "formula"
    if t == "text" and fmt in ("url", "email", "phone"):
        return str(fmt)
    if t == "range" and fmt == "percent":
        return "percent"
    if t == "range" and d.get("unit") and fmt == "currency":
        return "currency"
    if t == "range" and cfg.get("kind") in ("date", "datetime"):
        return "datetime"
    return None


def field_kind_of(d: Mapping[str, Any]) -> str | None:
    """Twin of ``custom.field_kind_of``: the field kind a stored Field document declares."""
    m = table_kind_mapping()
    t, fmt = d.get("type"), d.get("format")
    cfg = d.get("config") if isinstance(d.get("config"), dict) else {}
    if t == "range" and fmt in ("rating", "duration"):
        return str(fmt)
    if t == "text" and fmt in ("address", "barcode", "rich_text", "signature"):
        return str(fmt)
    if t == "list" and fmt == "status":
        return "status"
    if t == "formula" and fmt == "count" and cfg.get("agg") == "count":
        return "count"
    if t == "formula" and cfg.get("system") in m["system_kinds"]:
        return str(cfg["system"])
    if t == "relation" and isinstance(cfg.get("allowed_types"), list):
        return "entity_reference"
    parity = _parity_type(d)
    if parity is not None:
        return parity
    if t == "text":
        return "long_text" if fmt == "long" or _truthy(cfg.get("multiline")) else "text"
    if t == "range":
        return "number"
    if t == "relation":
        return "relation"
    return None


def _field_kind(d: Mapping[str, Any]) -> str | None:
    """The store's own ``field_kind`` when the facts carry it (``custom.field_kind_of`` per
    Field, asked of the door); otherwise this twin's derivation of the same answer."""
    if "field_kind" in d:
        kind = d.get("field_kind")
        return kind if isinstance(kind, str) else None
    return field_kind_of(d)


def _kind_spec(d: Mapping[str, Any]) -> dict[str, Any]:
    m = table_kind_mapping()
    kind = _field_kind(d) or m["by_behaviour"].get(str(d.get("type")), "formula")
    return m["kinds"].get(kind) or m["kinds"]["formula"]


# --------------------------------------------------------------------------- per Field


def _unconditional_rules(d: Mapping[str, Any]) -> list[dict[str, Any]]:
    out = []
    for rule in d.get("rules") or []:
        if isinstance(rule, dict) and not rule.get("applies_to_types"):
            out.append(rule)
    return out


def _number(value: object) -> int | float | None:
    """A rule's number, written the way JSON.stringify writes it (6.0 is 6) — byte parity."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str) and re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", value):
        value = float(value)
    if isinstance(value, float):
        return int(value) if value.is_integer() else value
    if isinstance(value, int):
        return value
    return None


def _choice_tokens(facts: Mapping[str, Any], key: str) -> list[str]:
    tokens: list[str] = []
    for choice in (facts.get("choices") or {}).get(key) or []:
        for token in (choice.get("key"), choice.get("label"), choice.get("id")):
            if isinstance(token, str) and token and token not in tokens:
                tokens.append(token)
    return tokens


def _live_choice_keys(facts: Mapping[str, Any], key: str) -> list[str]:
    keys: list[str] = []
    for choice in (facts.get("choices") or {}).get(key) or []:
        k = choice.get("key")
        if not choice.get("retired") and isinstance(k, str) and k and k not in keys:
            keys.append(k)
    return keys


def _item(facts: Mapping[str, Any], d: Mapping[str, Any], mode: Literal["stored", "authored"]) -> dict[str, Any]:
    """One value of this Field (before multi / relation list / nulls)."""
    m = table_kind_mapping()
    spec = _kind_spec(d)
    shape = spec["shape"]
    cfg = d.get("config") if isinstance(d.get("config"), dict) else {}
    key = str(d.get("key"))
    if shape in ("string", "number", "boolean"):
        item = copy.deepcopy(spec["value"])
        for rule in _unconditional_rules(d):
            kind, value = rule.get("kind"), _number(rule.get("value"))
            if shape == "number" and kind == "min" and value is not None:
                item["minimum"] = value
            elif shape == "number" and kind == "max" and value is not None:
                item["maximum"] = value
            elif shape == "string" and kind == "length" and value is not None:
                # The longest only: the store's shortest rule exempts a blank, which a JSON
                # Schema minLength cannot, so it is left to the store.
                item["maxLength"] = int(value)
        if spec.get("rating") and "maximum" not in item:
            item["maximum"] = m["rating_max"]
        if spec.get("unit") and d.get("unit") and mode == "stored":
            item["x-matrx-unit"] = d.get("unit")
        return item
    if shape == "datetime":
        if mode == "stored":
            # The store casts a string to timestamptz; the pattern refuses what no cast can read.
            return {"type": ["number", "string"], "pattern": m["stored_patterns"]["datetime"]}
        return {"type": "string", "format": "date" if cfg.get("kind") == "date" else "date-time"}
    if shape == "choice":
        if _truthy(cfg.get("allow_other")):
            return {"type": "string"}
        if mode == "stored":
            return {"type": "string", "enum": _choice_tokens(facts, key)}
        live = _live_choice_keys(facts, key)
        if not live or len(live) > m["choice_enum_limit"]:
            return {"type": "string"}
        return {"type": "string", "enum": live}
    if shape == "relation":
        if mode == "stored":
            # custom.validate_values refuses a value that is not an id by this very regex.
            return {"type": "string", "format": "uuid", "pattern": m["stored_patterns"]["record_id"]}
        return {"type": "string", "format": "uuid"}
    if shape == "entity_reference":
        allowed = [t for t in cfg.get("allowed_types") or [] if isinstance(t, str)]
        item = {
            "type": "object",
            "properties": {
                "token": {"type": "string", "enum": allowed},
                "id": {"type": "string", "format": "uuid"},
            },
            "required": ["token", "id"],
        }
        if mode == "stored":
            item["properties"]["id"]["pattern"] = m["stored_patterns"]["record_id"]
        if mode == "authored":
            item["additionalProperties"] = False
        return item
    if shape == "address":
        part = {"type": ["string", "null"], "maxLength": m["address_part_max"]}
        if mode == "authored":
            part = {"type": "string", "maxLength": m["address_part_max"]}
        item = {
            "type": "object",
            "properties": {p: dict(part) for p in m["address_parts"]},
            "additionalProperties": False,
        }
        if mode == "stored":
            item["minProperties"] = 1
        return item
    return {"readOnly": True}


def _is_typed(d: Mapping[str, Any]) -> bool:
    applies = d.get("applies_to_types")
    return isinstance(applies, list) and len(applies) > 0


def _stored_value(facts: Mapping[str, Any], d: Mapping[str, Any]) -> dict[str, Any]:
    spec = _kind_spec(d)
    shape = spec["shape"]
    if shape == "computed":
        return {"readOnly": True}
    item = _item(facts, d, "stored")
    required = _truthy(d.get("required")) and not _is_typed(d)
    if shape in ("relation", "entity_reference"):
        many: dict[str, Any] = {"type": "array", "items": item}
        ceiling = _number(d.get("relation_max"))
        if ceiling is not None:
            many["maxItems"] = int(ceiling)
        if required:
            many["minItems"] = 1
        value: dict[str, Any] = {"anyOf": [item, many]}
    elif _truthy(d.get("multi")):
        value = {"type": "array", "items": item}
        if required:
            value["minItems"] = 1
    else:
        value = item
    if required:
        return value
    return {"anyOf": [value, {"type": "null"}]}


def _authored_value(facts: Mapping[str, Any], d: Mapping[str, Any], type_labels: list[str]) -> dict[str, Any]:
    spec = _kind_spec(d)
    shape = spec["shape"]
    item = _item(facts, d, "authored")
    if shape in ("relation", "entity_reference"):
        value: dict[str, Any] = {"type": "array", "items": item}
        ceiling = _number(d.get("relation_max"))
        if ceiling is not None:
            value["maxItems"] = int(ceiling)
    elif _truthy(d.get("multi")):
        value = {"type": "array", "items": item}
    else:
        value = item
    extras: list[str] = []
    if spec.get("unit") and d.get("unit"):
        extras.append(f"Amount in {d.get('unit')}.")
    if spec.get("hint"):
        extras.append(str(spec["hint"]))
    if type_labels:
        extras.append(f"Only for {', '.join(type_labels)} records.")
    label = str(d.get("label") or d.get("key"))
    value["description"] = f"{label}. {' '.join(extras)}" if extras else label
    return value


def _is_authored(d: Mapping[str, Any]) -> bool:
    spec = _kind_spec(d)
    return spec["shape"] != "computed" and spec.get("authored", True) is not False


def _type_choice(facts: Mapping[str, Any], word: str) -> dict[str, Any] | None:
    type_field = facts.get("type_field")
    for choice in (facts.get("choices") or {}).get(type_field or "") or []:
        if word in (choice.get("key"), choice.get("label"), choice.get("id")):
            return choice
    return None


def _type_synonyms(facts: Mapping[str, Any], word: str) -> tuple[str, list[str]]:
    choice = _type_choice(facts, word)
    if choice is None:
        return word, [word]
    out: list[str] = []
    for token in (choice.get("key"), choice.get("label"), choice.get("id")):
        if isinstance(token, str) and token and token not in out:
            out.append(token)
    return str(choice.get("key") or word), out


def _type_labels(facts: Mapping[str, Any], d: Mapping[str, Any]) -> list[str]:
    labels: list[str] = []
    for word in d.get("applies_to_types") or []:
        choice = _type_choice(facts, str(word))
        label = str(choice.get("label") or choice.get("key")) if choice else str(word)
        if label not in labels:
            labels.append(label)
    return labels


# --------------------------------------------------------------------------- whole schemas


def _facts(facts: TableKindFacts | Mapping[str, Any]) -> dict[str, Any]:
    return facts.model_dump() if isinstance(facts, TableKindFacts) else dict(facts)


def json_schema_for(
    facts: TableKindFacts | Mapping[str, Any], mode: Literal["stored", "authored"]
) -> dict[str, Any]:
    """The Fields-only JSON Schema of a record of this Table (no control keys)."""
    f = _facts(facts)
    slug = table_kind_slug(str(f["table_id"]))
    fields = [d for d in f.get("fields") or [] if isinstance(d, dict) and d.get("key")]
    properties: dict[str, Any] = {_KIND_KEY: {"const": slug}}
    required = [_KIND_KEY]

    if mode == "stored":
        branches: dict[str, dict[str, Any]] = {}
        for d in fields:
            key = str(d["key"])
            properties[key] = _stored_value(f, d)
            computed = _kind_spec(d)["shape"] == "computed"
            if not _truthy(d.get("required")) or computed:
                continue
            if not _is_typed(d):
                required.append(key)
                continue
            if not f.get("type_field"):
                continue
            for word in d.get("applies_to_types") or []:
                type_key, synonyms = _type_synonyms(f, str(word))
                branch = branches.setdefault(
                    type_key,
                    {
                        "if": {
                            "properties": {str(f["type_field"]): {"enum": synonyms}},
                            "required": [str(f["type_field"])],
                        },
                        "then": {"required": [], "properties": {}},
                    },
                )
                if key not in branch["then"]["required"]:
                    branch["then"]["required"].append(key)
                    branch["then"]["properties"][key] = {"not": {"type": "null"}}
        m = table_kind_mapping()
        platform_keys = f.get("platform_keys")
        if not isinstance(platform_keys, list):
            platform_keys = list(m["platform_keys"])
        for name in platform_keys:
            # A key the platform writes into every record (custom.record_platform_keys()); a
            # Field of the same name is the column and keeps its own shape.
            if isinstance(name, str) and name not in properties:
                properties[name] = copy.deepcopy(m["platform_keys"].get(name, {}))
        schema: dict[str, Any] = {
            "type": "object",
            "properties": properties,
            "patternProperties": {"^_": {}},
            "required": required,
        }
        # custom._undeclared_key_guard judges only a `fields` Table: a free_form (document) or
        # code Table keeps any key, so its schema stays open (custom.table_column_source).
        if (f.get("column_source") or m["column_source_default"]) == "fields":
            schema["additionalProperties"] = False
        if branches:
            schema["allOf"] = list(branches.values())
        return schema

    for d in fields:
        if not _is_authored(d):
            continue
        key = str(d["key"])
        typed = _is_typed(d)
        properties[key] = _authored_value(f, d, _type_labels(f, d) if typed else [])
        if _truthy(d.get("required")) and not typed:
            required.append(key)
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def render_schema_for(facts: TableKindFacts | Mapping[str, Any]) -> dict[str, Any]:
    """The Fields-only content-ir ``KindSchema`` (as JSON) the web draws a record with."""
    m = table_kind_mapping()
    f = _facts(facts)
    slug = table_kind_slug(str(f["table_id"]))
    out: dict[str, Any] = {}
    for d in f.get("fields") or []:
        if not isinstance(d, dict) or not d.get("key"):
            continue
        key = str(d["key"])
        spec = _kind_spec(d)
        shape = spec["shape"]
        multi = _truthy(d.get("multi"))
        cfg = d.get("config") if isinstance(d.get("config"), dict) else {}
        if shape == "choice":
            field: dict[str, Any] = {
                "type": "string[]" if multi else "enum",
                "values": _choice_tokens(f, key),
            }
            if _truthy(cfg.get("allow_other")):
                field["open"] = True
        else:
            field = copy.deepcopy(m["render"][shape]["many" if multi else "one"])
        field["nullable"] = True
        out[key] = field
    return {"kind": slug, "fields": out}


def stored_schema(facts: TableKindFacts | Mapping[str, Any]) -> dict[str, Any]:
    """What a stored or streamed record of this Table is validated against (control keys in)."""
    return with_control_keys(json_schema_for(facts, "stored"), mode="stored")


def authored_schema(
    facts: TableKindFacts | Mapping[str, Any], *, many: bool = False, allow_edit: bool = False
) -> dict[str, Any]:
    """What a model bound to "a record of this Table" is shown."""
    return with_control_keys(
        json_schema_for(facts, "authored"), mode="authored", many=many, allow_edit=allow_edit
    )


def render_schema(facts: TableKindFacts | Mapping[str, Any]) -> dict[str, Any]:
    """The web's ``KindSchema`` with the control keys as optional render fields."""
    return with_control_key_fields(render_schema_for(facts))
