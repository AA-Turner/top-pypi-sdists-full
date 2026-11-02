"""THE ONE declared-shape probe — what a step's output offers, read off its schema.

Three layers each need the same answer to "what is actually in there?" and had
their own half of it:

* ``matrx_graph.validation`` walked a mapping source path against the upstream
  output schema (an unprovable path stays quiet, a provably-absent segment on a
  CLOSED level is an error);
* nothing at all checked the ``$item.<path>`` templates inside
  ``data.map_template`` / ``control.map`` — those were authored blind and died
  mid-run (Newsroom Desk, 2026-09-12: ``$item.entries`` over a
  ``gather_result.values`` element, four paid ledger agents spent first);
* the workflow-authoring tool an agent uses had no way to SHOW an author the
  upstream shape it was wiring from, so it guessed.

This module is that shared probe: resolve a path through a declared JSON
schema, get the item schema of a list, and describe a level's fields WITH their
descriptions (the descriptions are the whole point — ``gather_result.values``
says in its own words that it is the RAW per-item result and
``structured_outputs`` is the per-item structured payload).

Everything here is declaration-only: it never sees a run's data, and it says
NOTHING where the schema stops describing (an open object, an untyped value, a
``JsonValue`` element). An unprovable path is not a finding.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from matrx_graph.paths import first_segment, parse_path, source_paths

__all__ = [
    "model_json_schema",
    "resolve_ref",
    "schema_at_path",
    "path_problem",
    "kind_path_problem",
    "item_schema_of",
    "declared_fields",
    "declared_field_names",
    "is_described",
    "template_item_paths",
    "upstream_shape_notes",
    "TEMPLATE_HOSTS",
]

#: Nodes whose config carries a per-element ``$item`` template, and the input
#: key holding the list those elements come from. The authoring-time template
#: check reads this; extend it when adding a list-shaping node.
#: ``node_type -> (config_key, list_input_key)``
TEMPLATE_HOSTS: dict[str, tuple[str, str]] = {
    "data.map_template": ("template", "items"),
    "control.map": ("payload_template", "items"),
}

#: How much of a field's declared description travels in an authoring-tool
#: digest. Enough to carry the meaning ("THE RAW per-item results…"), bounded so
#: a 51-node workflow's shape notes cannot blow an author's context.
DESCRIPTION_CAP = 300


#: One rendered schema per model class for the process. Pydantic re-derives the schema on every
#: ``model_json_schema()`` call (~7 ms for a node output model); validation probes it once per edge
#: mapping, so a 63-edge definition spent ~1 s per validate+compile on the run-start path.
#: Callers only read the returned dict — never mutate it.
_SCHEMA_CACHE: dict[type, dict[str, Any]] = {}


def model_json_schema(model: type[BaseModel]) -> dict[str, Any]:
    """A model's JSON schema (cached per class), or ``{}`` when it will not render."""
    cached = _SCHEMA_CACHE.get(model)
    if cached is not None:
        return cached
    try:
        schema = model.model_json_schema()
    except Exception:  # noqa: BLE001 — a schema that won't render can't be probed
        schema = {}
    _SCHEMA_CACHE[model] = schema
    return schema


def resolve_ref(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    """Follow a local ``$ref`` into ``$defs`` (one hop is all our models emit)."""
    ref = schema.get("$ref")
    if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
        return schema
    return root.get("$defs", {}).get(ref.split("/")[-1], {}) or schema


def _is_index(kind: str, key: str | int) -> bool:
    # ``*`` (each element, ``matrx_graph.paths``) walks into a list's items like an index.
    return kind == "i" or key == "*" or (isinstance(key, str) and key.lstrip("-").isdigit())


def path_problem(
    root: dict[str, Any],
    path: str,
    *,
    start: dict[str, Any] | None = None,
    origin: str = "the output",
) -> str | None:
    """Why ``path`` can NEVER resolve inside ``root`` — or None.

    Walks the declared schema segment by segment (objects, ``$ref``s and array
    ``items``) using the SAME path grammar the engine routes with
    (``matrx_graph.paths``). It reports a problem only where the schema is
    CLOSED at that level and provably lacks the segment: the moment the walk
    reaches an open object, an untyped value, or anything the schema does not
    describe, it stops and says nothing.

    ``start`` begins the walk at a sub-schema (an element of a list, say) and
    ``origin`` names that place in the message.
    """
    for alternative in source_paths(path):
        problem = _one_path_problem(root, alternative, start=start, origin=origin)
        if problem is not None:
            return problem
    return None


def kind_path_problem(
    kind_schema: dict[str, Any],
    source_key: str,
    *,
    beside: set[str] | frozenset[str] | tuple[str, ...] = (),
    origin: str = "the declared output kind",
) -> str | None:
    """Why ``source_key`` can NEVER resolve against a step's DECLARED OUTPUT KIND — or None.

    The ONE judgment the save gate (``content_ir.authoring_gate``) and the run
    (``Scheduler._kind_path_problem``) share. Each ``??`` alternative is judged on its
    own: an alternative that opens with a key the step hands BESIDE its kind
    (``run_envelope``, ``ctx.declare_beside_kind``, ``__kind``) is not the kind's and is
    never judged; every other alternative is walked against the kind's schema, exactly
    as :func:`path_problem` walks each alternative. ``answer ?? final_text`` on a typed
    agent that hands ``final_text`` beside its kind is judged only on ``answer``.
    """
    skip = {str(f) for f in beside} | {"__kind"}
    for alternative in source_paths(source_key):
        if alternative.startswith("$") or first_segment(alternative) in skip:
            continue
        problem = _one_path_problem(kind_schema, alternative, start=None, origin=origin)
        if problem is not None:
            return problem
    return None


def _one_path_problem(
    root: dict[str, Any], path: str, *, start: dict[str, Any] | None, origin: str
) -> str | None:
    current: dict[str, Any] = root if start is None else start
    walked: list[str] = []
    for kind, key in parse_path(path):
        current = resolve_ref(current, root)
        if _is_index(kind, key):
            items = current.get("items")
            if isinstance(items, dict):
                current = items
                walked.append(str(key))
                continue
            return None  # not described as a list here — unprovable, stay quiet
        props = current.get("properties")
        if not isinstance(props, dict):
            return None  # no declared shape at this level — unprovable
        if key in props:
            current = props[key] if isinstance(props[key], dict) else {}
            walked.append(str(key))
            continue
        if current.get("additionalProperties") is False:
            where = origin if not walked else "'" + ".".join(walked) + "'"
            return (
                f"segment '{key}' is not declared on {where} "
                f"(which declares {sorted(props)} and accepts nothing else)"
            )
        return None  # open at this level — the key may legitimately arrive
    return None


def schema_at_path(
    root: dict[str, Any], path: str, *, start: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """The declared sub-schema at ``path``, or None where the declaration stops."""
    current: dict[str, Any] = root if start is None else start
    for kind, key in parse_path(path):
        current = resolve_ref(current, root)
        if _is_index(kind, key):
            items = current.get("items")
            if not isinstance(items, dict):
                return None
            current = items
            continue
        props = current.get("properties")
        if not isinstance(props, dict):
            return None
        nxt = props.get(key)
        if not isinstance(nxt, dict):
            return None
        current = nxt
    return resolve_ref(current, root)


def item_schema_of(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any] | None:
    """The element schema of a declared array, or None when it is not an array."""
    schema = resolve_ref(schema, root)
    items = schema.get("items")
    if not isinstance(items, dict):
        return None
    return resolve_ref(items, root)


def is_described(schema: dict[str, Any] | None) -> bool:
    """True when this level declares object properties we can reason about.

    ``list[JsonValue]``'s element resolves to an ``anyOf`` with no
    ``properties`` — undescribed, so nothing static may be claimed about it.
    """
    return isinstance(schema, dict) and isinstance(schema.get("properties"), dict)


def declared_fields(
    schema: dict[str, Any] | None,
    root: dict[str, Any],
    *,
    description_cap: int = DESCRIPTION_CAP,
) -> dict[str, str]:
    """``{field: description}`` for a level's declared properties.

    The descriptions are what an author is missing — ``values`` vs
    ``structured_outputs`` is a decision only its own words settle.
    """
    if not is_described(schema):
        return {}
    out: dict[str, str] = {}
    for name, prop in (schema or {}).get("properties", {}).items():  # type: ignore[union-attr]
        prop = resolve_ref(prop, root) if isinstance(prop, dict) else {}
        desc = prop.get("description") if isinstance(prop, dict) else None
        text = str(desc).strip() if isinstance(desc, str) else ""
        if len(text) > description_cap:
            text = text[:description_cap].rstrip() + "…"
        out[str(name)] = text
    return out


def declared_field_names(schema: dict[str, Any] | None) -> list[str]:
    """Sorted property names at a level (empty when undescribed)."""
    if not is_described(schema):
        return []
    return sorted(str(k) for k in (schema or {}).get("properties", {}))  # type: ignore[union-attr]


def template_item_paths(template: Any, *, prefix: str = "$item.") -> list[str]:
    """Every ``$item.<path>`` (or ``$in.<path>``) path inside a template.

    Recurses dicts and lists exactly as ``substitute_template`` does, including
    through a ``{"$cycle": [...]}`` pool, so the static check sees every path
    the run would resolve. Indirect ``{sibling}`` segments are skipped — their
    segment is data, not a declaration.
    """
    found: list[str] = []
    if isinstance(template, str):
        if template.startswith(prefix):
            path = template[len(prefix) :]
            if path and "{" not in path:
                found.append(path)
        return found
    if isinstance(template, dict):
        for value in template.values():
            found.extend(template_item_paths(value, prefix=prefix))
        return found
    if isinstance(template, list):
        for value in template:
            found.extend(template_item_paths(value, prefix=prefix))
        return found
    return found


#: How many upstream sources one authoring digest describes before it says how
#: many more there are. A 51-node Masterwork must not spend an author's context
#: on shapes; the ones it is WIRING are what it needs.
SHAPE_NOTES_CAP = 12


def upstream_shape_notes(definition: Any, registry: Any = None) -> list[dict[str, Any]]:
    """What every step in this definition is actually reading FROM — declared.

    One entry per upstream node an edge maps out of: its declared output kind,
    the fields it emits WITH their descriptions, and the paths this definition's
    edges currently read. Template-hosting nodes (``data.map_template``,
    ``control.map``) additionally get ``element`` — the shape of ONE item of the
    list their ``$item`` template runs over, or an explicit statement that the
    element shape is undeclared, which is the one thing an author cannot guess
    and the Newsroom Desk failure (2026-09-12) turned on.

    Declaration-only and side-effect free, so any authoring surface (the agent
    tool, a REST route, the Studio) can hand it straight back to whoever is
    wiring. Returns ``[]`` when nothing can be said.
    """
    from matrx_graph.executor.registry import default_registry
    from matrx_graph.types.definition import Definition

    registry = registry or default_registry()
    if not isinstance(definition, Definition):
        try:
            definition = Definition.model_validate(definition)
        except Exception:  # noqa: BLE001 — a definition that won't parse has no shapes
            return []

    specs: dict[str, Any] = {}
    for node in definition.nodes:
        try:
            if registry.has(node.spec_type):
                specs[node.id] = registry.get(node.spec_type).spec
        except Exception:  # noqa: BLE001 — an unregistered type is reported elsewhere
            continue

    notes: dict[str, dict[str, Any]] = {}
    element_notes: list[dict[str, Any]] = []

    for edge in definition.edges:
        spec = specs.get(edge.source)
        if spec is None or spec.dynamic_output:
            continue
        root = model_json_schema(spec.output_schema)
        entry = notes.get(edge.source)
        if entry is None:
            entry = {
                "node_id": edge.source,
                "node_type": spec.node_type,
                "output_kind": spec.output_kind,
                "emits": declared_fields(root, root),
                "read_by": [],
            }
            notes[edge.source] = entry
        mappings = edge.data.get("mappings")
        read = (
            {str(k): v for k, v in mappings.items()}
            if isinstance(mappings, dict) and mappings
            else "the whole payload (no field mappings)"
        )
        entry["read_by"].append({"node_id": edge.target, "reads": read})

        target_spec = specs.get(edge.target)
        host = TEMPLATE_HOSTS.get(target_spec.node_type) if target_spec is not None else None
        if host is None:
            continue
        config_key, list_input = host
        target_node = next((n for n in definition.nodes if n.id == edge.target), None)
        template = (
            target_node.config.get(config_key)
            if target_node is not None and isinstance(target_node.config, dict)
            else None
        )
        paths = template_item_paths(template)
        if isinstance(mappings, dict):
            if list_input not in mappings or not isinstance(mappings[list_input], str):
                continue
            source_path = mappings[list_input]
        else:
            source_path = list_input
        list_schema = schema_at_path(root, source_path)
        element = item_schema_of(list_schema, root) if list_schema is not None else None
        note: dict[str, Any] = {
            "node_id": edge.target,
            "node_type": target_spec.node_type if target_spec else None,
            "template_paths": [f"$item.{p}" for p in paths],
            "items_come_from": {"node_id": edge.source, "path": source_path},
        }
        if is_described(element):
            note["element_fields"] = declared_fields(element, root)
        else:
            note["element_fields"] = None
            note["element_is_undeclared"] = (
                f"'{source_path}' is declared as a list of undescribed values, so "
                f"nothing can check these template paths before the run. Read the "
                f"description of '{source_path}' on '{edge.source}' above and be sure "
                f"each path exists on ONE ELEMENT of it — a raw per-item step result "
                f"carries its structured payload one level down."
            )
        element_notes.append(note)

    ordered = list(notes.values())
    out: list[dict[str, Any]] = ordered[:SHAPE_NOTES_CAP]
    if len(ordered) > SHAPE_NOTES_CAP:
        out.append(
            {
                "note": (
                    f"{len(ordered) - SHAPE_NOTES_CAP} more upstream source(s) not "
                    f"shown — ask workflow_catalog get_node_type for their schemas."
                )
            }
        )
    out.extend(element_notes)
    return out
