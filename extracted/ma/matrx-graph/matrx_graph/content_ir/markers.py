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
    "declare_schema_kind",
    "normalize_nonidentity_markers",
    "drop_blank_kind_markers",
    "without_blank_kind_slot",
    "without_blank_kind_slots",
    "strip_kind_markers",
    "strip_optional_schema_kind_stamps",
]

# A pathological / cyclic ``$ref`` chain must not hang the reducer.
_MAX_REF_HOPS = 32

# Schema maps whose keys describe a schema or a dictionary's possible values,
# rather than JSON Schema keywords that may be normalized away.
_SCHEMA_KEYED_MAPS = frozenset({"properties", "$defs", "patternProperties"})


def strip_optional_schema_kind_stamps(
    node: Any, *, keys_are_data: bool = False, keep_blank_const: bool = False
) -> Any:
    """Return a schema copy without optional registry-added marker properties.

    The registry write trigger stamps ``__kind`` onto every object schema. That
    is storage normalization, not a producer contract change, so comparison
    may disregard its optional free-string legacy form and its current
    non-identity ``const: ""`` form. This is schema-only and pure: required and
    identity-bearing const or enum marker declarations are kept; the input
    schema is never mutated.

    ``keep_blank_const=True`` is for DRIFT detection (rule 31): a stored blank
    ``const ""`` is a defect, so removing it IS a change the publisher must see and
    write, even though the compatibility gate (default) rightly calls the removal
    backward compatible.
    """
    if isinstance(node, list):
        return [
            strip_optional_schema_kind_stamps(item, keep_blank_const=keep_blank_const)
            for item in node
        ]
    if not isinstance(node, dict):
        return node
    out = {
        key: strip_optional_schema_kind_stamps(
            value,
            keys_are_data=(not keys_are_data and key in _SCHEMA_KEYED_MAPS),
            keep_blank_const=keep_blank_const,
        )
        for key, value in node.items()
    }
    if keys_are_data:
        return out
    properties = out.get("properties")
    node_type = out.get("type")
    # A nullable object (``type: ["object", "null"]``) carries the same optional
    # stamp; reading only the bare ``"object"`` form called the rule-31 removal of
    # its blank ``const ""`` a breaking change (variable_definition.control, 2026-11-02).
    is_object = node_type == "object" or (isinstance(node_type, list) and "object" in node_type)
    if (
        is_object
        and isinstance(properties, dict)
        and (
            properties.get(KIND_KEY) == {"type": "string"}
            or (
                not keep_blank_const
                and properties.get(KIND_KEY) == {"type": "string", "const": ""}
            )
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
    """The schema governing ``key``: a declared property first, else a matching ``patternProperties``
    pattern (FX18: a key matched only by a pattern, like ``testimony_room_<slug>``, was treated as
    unknown and lost its ``__kind``, so a section the kind REQUIRES to carry it failed)."""
    import re as _re

    branches = list(_branches(schema, root))
    for branch in branches:
        properties = branch.get("properties")
        if isinstance(properties, dict) and key in properties:
            return properties[key]
    for branch in branches:
        patterns = branch.get("patternProperties")
        if isinstance(patterns, dict):
            for pattern, sub in patterns.items():
                try:
                    if _re.search(pattern, key) and isinstance(sub, dict):
                        return sub
                except _re.error:
                    continue
    return None


def _items_schema(schema: dict[str, Any], root: dict[str, Any]) -> Any:
    for branch in _branches(schema, root):
        items = branch.get("items")
        if isinstance(items, dict):
            return items
    return None


#: Keywords that annotate a schema position without constraining what it accepts.
_ANNOTATION_KEYWORDS = frozenset(
    {"title", "description", "default", "examples", "$comment", "deprecated", "readOnly", "writeOnly"}
)


def _accepts_anything(schema: Any, root: dict[str, Any]) -> bool:
    """True when ``schema`` is a position that accepts EVERY instance: ``{}`` (pydantic's ``JsonValue``
    exports as ``$defs.JsonValue: {}``), reached through real ``$ref`` hops, with annotations only.

    An unresolvable ``$ref`` is NOT accepting (the validator cannot apply it — its verdict is a skip)."""
    hops = 0
    while isinstance(schema, dict):
        if not set(schema) - _ANNOTATION_KEYWORDS - {"$ref"}:
            if "$ref" not in schema:
                return True
        else:
            return False
        hops += 1
        if hops > _MAX_REF_HOPS:
            return False
        ref = str(schema["$ref"])
        if ref in ("#", "#/"):
            schema = root
            continue
        if not ref.startswith("#/$defs/"):
            return False
        schema = (root.get("$defs") or {}).get(ref.rsplit("/", 1)[-1])
    return schema is True


#: The keywords a container position may carry and still let a child that accepts anything be validated as
#: given (review 6h, I2). Each constrains only the container's own keys or type, never a child's content, and
#: never prints the instance in its error. Anything else — ``allOf``/``anyOf``/``oneOf``/``not``/``if`` (a sibling
#: branch may constrain the same child), ``const``/``enum``/``uniqueItems``/``contains`` (they compare the whole
#: child, markers included), ``unevaluated*``/``prefixItems``/``patternProperties`` (a second schema reaches the
#: child), ``min*``/``max*`` (their error prints the instance) — means the child is reduced as before.
_PLAIN_OBJECT_KEYWORDS = _ANNOTATION_KEYWORDS | {
    "type", "properties", "required", "additionalProperties", "propertyNames", "$defs", "definitions", "$schema",
}
_PLAIN_ARRAY_KEYWORDS = _ANNOTATION_KEYWORDS | {"type", "items", "$defs", "definitions", "$schema"}


def _plain_container(schema: Any, root: dict[str, Any], value: Any) -> bool:
    """True when ``schema`` (``value``'s position) reaches its children ONLY through the one child schema the
    reduction reads: pure ``$ref`` hops (no sibling keywords lost on the way), a ``type`` that admits ``value``,
    and keywords from the plain set alone. Then a child whose schema accepts anything is under no other
    constraint at all, so keeping its markers cannot change the verdict or a single error message."""
    hops = 0
    while isinstance(schema, dict) and "$ref" in schema:
        if set(schema) - _ANNOTATION_KEYWORDS - {"$ref"}:
            return False
        hops += 1
        if hops > _MAX_REF_HOPS:
            return False
        ref = str(schema["$ref"])
        if ref in ("#", "#/"):
            schema = root
            continue
        if not ref.startswith("#/$defs/"):
            return False
        schema = (root.get("$defs") or {}).get(ref.rsplit("/", 1)[-1])
    if not isinstance(schema, dict):
        return False
    if isinstance(value, dict):
        allowed, wanted = _PLAIN_OBJECT_KEYWORDS, "object"
    elif isinstance(value, list):
        allowed, wanted = _PLAIN_ARRAY_KEYWORDS, "array"
    else:
        return False
    if set(schema) - allowed:
        return False
    declared = schema.get("type", wanted)
    return declared == wanted or (isinstance(declared, list) and wanted in declared)


def _reduce(value: Any, schema: Any, root: dict[str, Any] | None, keep_free: bool = False) -> Any:
    # A position that accepts anything validates the same whatever it holds: the validation copy
    # keeps it as given instead of rebuilding it (L-SPEED 6e: a 900 KB list of rows under
    # ``items: {$ref: JsonValue}`` was copied leaf by leaf on every kind check of every step).
    # ``keep_free`` is True only while every container from the root down to here is plain
    # (:func:`_plain_container`), so the accept-anything schema is the ONLY one reaching this value.
    if keep_free and schema is not None and root is not None and _accepts_anything(schema, root):
        return value
    resolved: dict[str, Any] = {}
    if root is not None and schema is not None:
        resolved = _resolve_ref(schema, root)
    if keep_free:
        keep_free = schema is not None and root is not None and _plain_container(schema, root, value)

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
            out[key] = _reduce(item, child, root, keep_free)
        return out

    if isinstance(value, list):
        child = _items_schema(resolved, root or {}) if resolved else None
        return [_reduce(item, child, root, keep_free) for item in value]

    return value


def strip_kind_markers(value: Any, schema: dict[str, Any] | None = None) -> Any:
    """Reduce a block-shape value to the wire shape ``schema`` describes.

    Removes the ``__kind`` discriminator at every depth EXCEPT where ``schema``
    declares it as a real property. With no ``schema``, removes every marker.
    Pure and idempotent; non-container values are returned unchanged.
    """
    root = schema if isinstance(schema, dict) else None
    return _reduce(value, root, root)


def reduce_for_validation(value: Any, schema: dict[str, Any]) -> Any:
    """The copy a kind check validates: blank markers dropped (:func:`normalize_nonidentity_markers`), then
    :func:`strip_kind_markers` — except that a subtree whose ONLY governing schema accepts anything (reached
    through plain containers alone, :func:`_plain_container`) is kept as given. The verdict and every error are
    identical (``tests/test_a_kind_check_skip_never_changes_a_verdict.py`` diffs it against the full reduction);
    only the copying is skipped. Never
    for storage: a stored or returned value is reduced by :func:`strip_kind_markers` itself."""
    if not isinstance(schema, dict):
        return strip_kind_markers(value)
    return _reduce(_normalize(value, schema, schema, keep_free=True), schema, schema, keep_free=True)


def _marker_required(schema: dict[str, Any], root: dict[str, Any]) -> bool:
    """True when some branch at this position REQUIRES ``__kind``."""
    return any(KIND_KEY in (branch.get("required") or ()) for branch in _branches(schema, root))


def _normalize(value: Any, schema: Any, root: dict[str, Any], keep_free: bool = False) -> Any:
    if keep_free and schema is not None and _accepts_anything(schema, root):
        return value  # the only schema reaching it accepts anything (reduce_for_validation)
    resolved = _resolve_ref(schema, root) if schema is not None else {}
    if keep_free:
        keep_free = schema is not None and _plain_container(schema, root, value)
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if key == KIND_KEY and item in ("", None) and not (
                resolved and _marker_required(resolved, root)
            ):
                continue  # rule 31: a blank marker is absent, never a value
            child = _property_schema(resolved, root, key) if resolved else None
            out[key] = _normalize(item, child, root, keep_free) if child is not None else item
        return out
    if isinstance(value, list):
        child = _items_schema(resolved, root) if resolved else None
        return [_normalize(item, child, root, keep_free) if child is not None else item for item in value]
    return value


def drop_blank_kind_markers(value: Any) -> Any:
    """Every ``"__kind": ""`` (or ``null``) removed, at any depth; NAMED values untouched.

    Schema-free twin of :func:`normalize_nonidentity_markers` for STORED values
    (kind examples, samples) whose blank markers were stamped by the retired
    ``const ""`` (rule 31). Pure: the input is never mutated.
    """
    if isinstance(value, dict):
        return {
            key: drop_blank_kind_markers(item)
            for key, item in value.items()
            if not (key == KIND_KEY and item in ("", None))
        }
    if isinstance(value, list):
        return [drop_blank_kind_markers(item) for item in value]
    return value


def _is_blank_slot(marker: Any) -> bool:
    """A ``__kind`` property schema that can only hold the blank: ``const`` empty, or ``enum`` of only it."""
    if not isinstance(marker, dict):
        return False
    const = marker.get("const")
    enum = marker.get("enum")
    return (isinstance(const, str) and not const) or (
        isinstance(enum, list) and bool(enum) and all(isinstance(v, str) and not v for v in enum)
    )


def without_blank_kind_slot(node: dict[str, Any]) -> dict[str, Any]:
    """This object schema level without its BLANK ``__kind`` slot (rule 31: a kind is NAMED or ABSENT).

    Only a slot that can hold nothing but ``""`` leaves ``properties``, ``required`` and
    ``propertyOrdering``; a NAMED slot is returned untouched (rule 32: nothing destroys a kind name).
    Shallow and pure: the input is never mutated."""
    props = node.get("properties")
    if not (isinstance(props, dict) and _is_blank_slot(props.get(KIND_KEY))):
        return node
    out = dict(node)
    out["properties"] = {k: v for k, v in props.items() if k != KIND_KEY}
    for key in ("required", "propertyOrdering"):
        if isinstance(out.get(key), list):
            out[key] = [k for k in out[key] if k != KIND_KEY]
    return out


def without_blank_kind_slots(schema: Any) -> Any:
    """:func:`without_blank_kind_slot` at every depth (a copy). Named slots are kept everywhere."""
    if isinstance(schema, list):
        return [without_blank_kind_slots(v) for v in schema]
    if not isinstance(schema, dict):
        return schema
    return without_blank_kind_slot({k: without_blank_kind_slots(v) for k, v in schema.items()})


def declare_schema_kind(node: dict[str, Any], kind: str, *, description: str | None = None) -> dict[str, Any]:
    """This object schema level declaring ``__kind`` as the required ``const`` ``kind``, FIRST in
    ``properties`` (a constrained decoder writes keys in ``properties`` order). Any earlier marker
    declaration is REPLACED by the named one, never removed. Shallow and pure."""
    if not kind:
        raise ValueError("declare_schema_kind needs a kind name: a blank is never a kind (rule 31)")
    marker: dict[str, Any] = {"type": "string", "const": kind}
    if description:
        marker["description"] = description
    props = node.get("properties") if isinstance(node.get("properties"), dict) else {}
    out = dict(node)
    declared = {KIND_KEY: marker, **props}
    declared[KIND_KEY] = marker
    out["properties"] = declared
    required = node.get("required")
    if isinstance(required, list):
        if KIND_KEY not in required:
            out["required"] = [KIND_KEY, *required]
    else:
        out["required"] = [KIND_KEY]
    return out


def normalize_nonidentity_markers(value: Any, schema: dict[str, Any] | None) -> Any:
    """Accept-and-drop BLANK ``__kind`` markers (Content IR rule 31).

    A ``"__kind": ""`` (or ``null``) anywhere in ``value`` is removed — a blank is
    never a kind, so the key is absent — except where the schema REQUIRES the
    marker (left for the blank-kind alarm to report, never guessed). A NAMED
    value is never touched, wherever it sits (rule 32: nothing destroys a kind
    name); validators judge a local marker-reduced copy, so it is read, never
    refused. Nothing is ever written as ``""``. Pure: the input is never mutated.

    Called at the agent-output parse funnel (``matrx_ai.agents.output``) and on
    the local copy kind validation reads (``matrx_graph.kinds``).
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
