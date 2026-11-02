"""``__kind`` marker reduction — kept ONLY for the doors that still need it.

🚨 THE TWO-SCHEMA DOCTRINE IS DEAD (Arman, 2026-08-23). This module's header
used to describe a kind as having a BLOCK shape (markers) and a WIRE shape
(marker-free), with ``emitted_json_schema`` being the wire export and
"everything on the Python side validates against the WIRE shape." That was the
architecture of the bug, not a design:

  ``emitted_json_schema`` is BOTH what every Python validator reads AND what
  ``matrx_ai.kinds.response_format_for_kind`` binds an agent to. A marker-free
  export therefore meant 493 of 738 live kinds shipped a schema that FORBADE
  their own identity, and a producer bound to one was STRUCTURALLY UNABLE to
  say what it was emitting. That is why stored data lost its identity: not
  because someone chose to strip it, but because the schema had no place to put
  it.

**Every kind schema now DECLARES ``__kind`` at every object position** — a
``const`` plus ``required`` where the kind is identified, declared-but-optional
elsewhere so no closed object can ever REJECT the marker a nested kind carries.
Both emitted columns carry it, and both generators emit it
(``scripts/shape/emit-kind-rows.ts``, ``kind_authoring._create_single_kind``).

WHAT SURVIVES HERE, AND WHY
---------------------------
``strip_kind_markers`` remains for the two lawful doors — the AGENT PROMPT
(what a model reads is prose, not a payload) and EXTERNAL EGRESS (a value
leaving for a foreign contract) — plus VALIDATION TOLERANCE against a row still
pinned to a pre-2026-08-23 schema version, where it reduces a LOCAL copy and
only a verdict leaves. ``reduce_for_ingestion`` remains as the ingestion gate's
shrinking legacy shim. Guard: ``scripts/check_kind_marker_law.py``.

WHY IT IS SCHEMA-AWARE (and not a blind recursive delete)
---------------------------------------------------------
A handful of python-owned kinds have a hand-written ``emitted_json_schema``
that is passed through VERBATIM (the D156 path in ``kindBinding.ts``, for
kinds too nested for ``fields_from_json_schema``). Some of those declare
``__kind`` as a real property and even ``require`` it —
``video_transcript_research`` does exactly that at its root. Blind deletion
turns those into the mirror-image false failure ("``__kind`` is a required
property"), which is how the previous root-only stripper behaved and why
``media.youtube_analyzer`` could not declare its kind either.

So the rule is the one the canonical envelope partitioner already uses
(``matrx_ai.processing.blocks.envelope._partition``: unknown key → out):

    drop ``__kind`` at every position the schema does not declare it;
    keep it wherever the schema does.

Schema-free callers (``schema=None``) get the plain doctrine — every marker is
an envelope marker, so every marker goes.

The reduction is pure (never mutates its input) and IDEMPOTENT:
``strip(strip(x, s), s) == strip(x, s)``, which matters because it sits on
paths that may already have been reduced upstream.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.envelope import KIND_KEY

__all__ = [
    "normalize_nonidentity_markers",
    "strip_kind_markers",
    "strip_optional_schema_kind_stamps",
]

# A pathological / cyclic ``$ref`` chain must not hang the reducer.
_MAX_REF_HOPS = 32

# Schema maps whose keys describe a schema or a dictionary's possible values,
# rather than JSON Schema keywords that may be normalized away.
_SCHEMA_KEYED_MAPS = frozenset({"properties", "$defs", "patternProperties"})


def strip_optional_schema_kind_stamps(node: Any, *, keys_are_data: bool = False) -> Any:
    """Return a schema copy without optional registry-added marker properties.

    The registry write trigger stamps ``__kind`` onto every object schema. That
    is storage normalization, not a producer contract change, so comparison
    may disregard its optional free-string legacy form and its current
    non-identity ``const: ""`` form. This is schema-only and pure: required and
    identity-bearing const or enum marker declarations are kept; the input
    schema is never mutated.
    """
    if isinstance(node, list):
        return [strip_optional_schema_kind_stamps(item) for item in node]
    if not isinstance(node, dict):
        return node
    out = {
        key: strip_optional_schema_kind_stamps(
            value, keys_are_data=(not keys_are_data and key in _SCHEMA_KEYED_MAPS)
        )
        for key, value in node.items()
    }
    if keys_are_data:
        return out
    properties = out.get("properties")
    if (
        out.get("type") == "object"
        and isinstance(properties, dict)
        and properties.get(KIND_KEY) in (
            {"type": "string"},
            {"type": "string", "const": ""},
        )
        and KIND_KEY not in set(out.get("required") or ())
    ):
        properties = {key: value for key, value in properties.items() if key != KIND_KEY}
        if properties:
            out["properties"] = properties
        else:
            out.pop("properties")
        if not out.get("required"):
            out.pop("required", None)
    return out


def _resolve_ref(schema: Any, root: dict[str, Any]) -> dict[str, Any]:
    """Follow ``$ref`` to its target. ``"#"`` is the recursive-root form the
    kind exporter emits for self-referencing kinds (``kind-to-json-schema.ts``
    ``refFor``); an unresolvable ref degrades to "no schema here", which makes
    the caller fall back to schema-free reduction for that subtree."""
    hops = 0
    while isinstance(schema, dict) and "$ref" in schema:
        hops += 1
        if hops > _MAX_REF_HOPS:
            return {}
        ref = str(schema["$ref"])
        if ref in ("#", "#/"):
            return root
        target = (root.get("$defs") or {}).get(ref.rsplit("/", 1)[-1])
        if not isinstance(target, dict):
            return {}
        schema = target
    return schema if isinstance(schema, dict) else {}


def _branches(schema: dict[str, Any], root: dict[str, Any]) -> list[dict[str, Any]]:
    """The schema node itself plus every ``anyOf``/``oneOf``/``allOf`` member,
    each ``$ref``-resolved. A union whose members disagree about ``__kind`` is
    read permissively (see ``_declares_kind``)."""
    out = [schema]
    for keyword in ("anyOf", "oneOf", "allOf"):
        members = schema.get(keyword)
        if isinstance(members, list):
            out.extend(_resolve_ref(m, root) for m in members if isinstance(m, dict))
    return out


def _declares_kind(schema: dict[str, Any], root: dict[str, Any]) -> bool:
    """True when ANY branch of this position declares ``__kind`` as a real
    property. Deliberately permissive: keeping a marker the schema might
    accept costs nothing (the value still validates), while dropping one the
    schema requires is a permanent false failure."""
    for branch in _branches(schema, root):
        properties = branch.get("properties")
        if isinstance(properties, dict) and KIND_KEY in properties:
            return True
    return False


def _property_schema(schema: dict[str, Any], root: dict[str, Any], key: str) -> Any:
    for branch in _branches(schema, root):
        properties = branch.get("properties")
        if isinstance(properties, dict) and key in properties:
            return properties[key]
    return None


def _items_schema(schema: dict[str, Any], root: dict[str, Any]) -> Any:
    for branch in _branches(schema, root):
        items = branch.get("items")
        if isinstance(items, dict):
            return items
    return None


def _reduce(value: Any, schema: Any, root: dict[str, Any] | None) -> Any:
    resolved: dict[str, Any] = {}
    if root is not None and schema is not None:
        resolved = _resolve_ref(schema, root)

    if isinstance(value, dict):
        # Schema-free (root is None) OR this position is unknown to the schema
        # ({} from an unresolvable ref): apply the plain doctrine — the marker
        # is an envelope marker, so it goes.
        keep_marker = bool(resolved) and _declares_kind(resolved, root or {})
        out: dict[str, Any] = {}
        for key, item in value.items():
            if key == KIND_KEY and not keep_marker:
                continue
            child = _property_schema(resolved, root or {}, key) if resolved else None
            out[key] = _reduce(item, child, root)
        return out

    if isinstance(value, list):
        child = _items_schema(resolved, root or {}) if resolved else None
        return [_reduce(item, child, root) for item in value]

    return value


def strip_kind_markers(value: Any, schema: dict[str, Any] | None = None) -> Any:
    """Reduce a block-shape value to the wire shape ``schema`` describes.

    Removes the ``__kind`` discriminator at every depth EXCEPT where ``schema``
    declares it as a real property. With no ``schema``, removes every marker.
    Pure and idempotent; non-container values are returned unchanged.
    """
    root = schema if isinstance(schema, dict) else None
    return _reduce(value, root, root)


def _is_nonidentity_marker(prop: Any) -> bool:
    """A ``__kind`` declaration that says "no kind here": ``const ""``."""
    return isinstance(prop, dict) and prop.get("const") == ""


def _marker_is_nonidentity(schema: dict[str, Any], root: dict[str, Any]) -> bool:
    """True when every branch that declares ``__kind`` here declares the
    non-identity ``const ""`` — the position is a plain sub-structure
    (``KindSubModel``), so any marker a payload carries there is noise."""
    declared = [
        branch["properties"][KIND_KEY]
        for branch in _branches(schema, root)
        if isinstance(branch.get("properties"), dict) and KIND_KEY in branch["properties"]
    ]
    return bool(declared) and all(_is_nonidentity_marker(p) for p in declared)


def _normalize(value: Any, schema: Any, root: dict[str, Any]) -> Any:
    resolved = _resolve_ref(schema, root) if schema is not None else {}
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            child = _property_schema(resolved, root, key) if resolved else None
            out[key] = _normalize(item, child, root) if child is not None else item
        if (
            KIND_KEY in out
            and out[KIND_KEY] != ""
            and resolved
            and _marker_is_nonidentity(resolved, root)
        ):
            out[KIND_KEY] = ""
        return out
    if isinstance(value, list):
        child = _items_schema(resolved, root) if resolved else None
        return [_normalize(item, child, root) if child is not None else item for item in value]
    return value


def normalize_nonidentity_markers(value: Any, schema: dict[str, Any] | None) -> Any:
    """Accept-and-normalize junk ``__kind`` values on plain sub-structures.

    Wherever ``schema`` declares ``__kind`` as the non-identity ``const ""``
    (every ``KindSubModel`` position), a payload's marker there is set to
    ``""`` — whatever an agent or an old stored row wrote (``"x"``,
    ``"grew_from"``, ``null``). The key is never removed (the marker is part
    of the data) and never added when absent. Positions that declare a real
    identity, or nothing, are untouched. Pure: the input is never mutated.

    Called at the agent-output parse funnel (``matrx_ai.agents.output``) and on
    the local copy kind validation reads (``matrx_graph.kinds``), so old data
    and a provider that ignored the const are read, never refused.
    """
    if not isinstance(schema, dict):
        return value
    return _normalize(value, schema, schema)


def _pattern_accepts_marker(schema: dict[str, Any]) -> bool:
    """True when a ``patternProperties`` pattern matches ``__kind``."""
    patterns = schema.get("patternProperties")
    if not isinstance(patterns, dict):
        return False
    import re as _re

    for pattern in patterns:
        try:
            if _re.search(pattern, KIND_KEY):
                return True
        except _re.error:
            return True  # unparseable pattern: fail open, keep the marker
    return False


def _conjunctive_forbids(node: dict[str, Any], root: dict[str, Any]) -> bool:
    """Would this node — with its ``allOf`` members merged — reject ``__kind``?

    ``allOf`` is CONJUNCTIVE: pydantic wraps ``$ref``s in it and validators
    merge the members, so a single closed member closes the whole position
    unless any member declares (or pattern-accepts) the marker.
    """
    members = [node]
    all_of = node.get("allOf")
    if isinstance(all_of, list):
        members += [_resolve_ref(m, root) for m in all_of if isinstance(m, dict)]
    closed = any(m.get("additionalProperties") is False for m in members)
    if not closed:
        return False
    for m in members:
        properties = m.get("properties")
        if isinstance(properties, dict) and KIND_KEY in properties:
            return False
        if _pattern_accepts_marker(m):
            return False
    return True


def _forbids_marker(resolved: dict[str, Any], root: dict[str, Any]) -> bool:
    """True when this position would REJECT ``__kind`` at validation.

    Union semantics matter (round-1 adversarial F5): pydantic tries every
    ``anyOf``/``oneOf`` branch, so the marker survives if ANY object-shaped
    branch accepts it — the position forbids only when EVERY object-shaped
    branch forbids. ``Optional[ClosedModel]`` (`anyOf: [closed, null]`) is
    therefore FORBIDDING: the null branch can never validate a dict, and the
    one object branch is closed. Non-object positions never forbid.
    """
    if not resolved:
        return False
    disjuncts: list[dict[str, Any]] = []
    for keyword in ("anyOf", "oneOf"):
        members = resolved.get(keyword)
        if isinstance(members, list):
            disjuncts += [_resolve_ref(m, root) for m in members if isinstance(m, dict)]
    if not disjuncts:
        return _conjunctive_forbids(resolved, root)

    def _objecty(node: dict[str, Any]) -> bool:
        if node.get("type") == "object" or isinstance(node.get("properties"), dict):
            return True
        ap = node.get("additionalProperties")
        if ap is not None:
            return True
        all_of = node.get("allOf")
        if isinstance(all_of, list):
            return any(
                _objecty(_resolve_ref(m, root)) for m in all_of if isinstance(m, dict)
            )
        return False

    object_branches = [d for d in disjuncts if _objecty(d)]
    if _objecty(resolved):
        object_branches.append(resolved)
    if not object_branches:
        return False
    return all(_conjunctive_forbids(branch, root) for branch in object_branches)


def _child_schema_for_ingestion(
    resolved: dict[str, Any], root: dict[str, Any], key: str
) -> Any:
    """The schema governing ``key``'s value — through properties,
    ``patternProperties``, and schema-valued ``additionalProperties``
    (``dict[str, Model]`` — round-1 F5's missed traversal)."""
    declared = _property_schema(resolved, root, key)
    if declared is not None:
        return declared
    import re as _re

    for branch in _branches(resolved, root):
        patterns = branch.get("patternProperties")
        if isinstance(patterns, dict):
            for pattern, sub in patterns.items():
                try:
                    if _re.search(pattern, key) and isinstance(sub, dict):
                        return sub
                except _re.error:
                    continue
        additional = branch.get("additionalProperties")
        if isinstance(additional, dict):
            return additional
    return None


def _reduce_for_ingestion(value: Any, schema: Any, root: dict[str, Any] | None) -> Any:
    resolved: dict[str, Any] = {}
    if root is not None and schema is not None:
        resolved = _resolve_ref(schema, root)

    if isinstance(value, dict):
        drop_marker = _forbids_marker(resolved, root or {})
        out: dict[str, Any] = {}
        for key, item in value.items():
            if key == KIND_KEY and drop_marker:
                continue
            child = (
                _child_schema_for_ingestion(resolved, root or {}, key) if resolved else None
            )
            out[key] = _reduce_for_ingestion(item, child, root)
        return out

    if isinstance(value, list):
        child = _items_schema(resolved, root or {}) if resolved else None
        return [_reduce_for_ingestion(item, child, root) for item in value]

    return value


def reduce_for_ingestion(value: Any, schema: dict[str, Any] | None = None) -> Any:
    """The ingestion gate's reducer — the ONE-SHAPE inverse of
    :func:`strip_kind_markers`.

    ``strip_kind_markers`` strips everywhere the schema does not DECLARE the
    marker — the old wire-shape doctrine, still correct at its two surviving
    doors (agent prompts, external egress). Ingestion is the opposite world:
    identity travels by default, and the marker is removed ONLY at positions
    where the receiving schema would fatally REJECT it (an explicitly closed
    object that does not declare it — the legacy ``extra="forbid"`` shim).
    Open objects, untyped dict args, unions, and unknown positions all keep
    the discriminator, so a kind-filtered edge's instances arrive still
    saying what they are. Pure and idempotent.
    """
    root = schema if isinstance(schema, dict) else None
    return _reduce_for_ingestion(value, root, root)
