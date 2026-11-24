"""Deep value-vs-JSON-Schema validation — the engine's strict-input primitive.

A node's declared input contract is a JSON Schema (for a dynamic-output source
node like ``io.user_input`` it's the SAME schema its run form is generated
from). The permissive ``spec.input_schema`` used at the node boundary
(``extra="allow"``, zero fields for dynamic nodes) cannot enforce the
author-defined field types, enums, or required-ness — so a wrong-typed or
out-of-enum value would flow straight through and only surface as a confusing
failure two steps downstream.

``validate_instance`` closes that gap. It is recursive by construction —
nested objects, arrays, enums, types, ``required`` and ``$ref`` are all checked
at any depth — because it delegates to ``jsonschema``. It returns human-readable
per-field messages (empty list = valid) so the caller can raise ONE structured
error naming every field that's wrong, not just the first.

This is deliberately a small, standalone, side-effect-free function so it can be
reused beyond the scheduler (host pre-flight checks, the node-catalog parity
guard) without importing the executor.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def _no_document(uri: str) -> None:
    return None


def _ref_registry(retrieve: Callable[[str], dict[str, Any] | None]) -> Any:
    """A ``referencing`` registry that fetches each unknown URI through ``retrieve``."""
    from referencing import Registry
    from referencing.exceptions import NoSuchResource
    from referencing.jsonschema import DRAFT202012

    def _fetch(uri: str) -> Any:
        contents = retrieve(uri)
        if not isinstance(contents, dict):
            raise NoSuchResource(ref=uri)
        return DRAFT202012.create_resource(contents)

    return Registry(retrieve=_fetch)


def validate_instance(
    schema: dict[str, Any],
    instance: Any,
    *,
    retrieve: Callable[[str], dict[str, Any] | None] | None = None,
) -> list[str]:
    """Per-field errors (``[]`` = valid OR skipped). See :func:`validate_instance_checked`
    when a skip must be told apart from a pass."""
    errors, _checked = validate_instance_checked(schema, instance, retrieve=retrieve)
    return errors


def validate_instance_checked(
    schema: dict[str, Any],
    instance: Any,
    *,
    retrieve: Callable[[str], dict[str, Any] | None] | None = None,
) -> tuple[list[str], bool]:
    """Validate ``instance`` against JSON Schema ``schema``; return per-field
    error strings (``[]`` = valid).

    A malformed *instance* fails closed with messages — that's the point.

    A malformed *schema* is OUR bug, not the user's, so this fails OPEN (returns
    ``[]``) rather than blocking a user's run — but it LOGS LOUDLY (never
    silent) so the platform defect surfaces. The compile-time layer that
    metaschema-checks a node's compiled ``effective_output_schema`` is
    ``schema_validity_errors`` below (wired into ``compile.py``); this runtime
    log remains the last line of defense for schemas that arrive from the kind
    catalog or other post-compile sources, so keep it loud.

    ``retrieve`` resolves a ``$ref`` to another document by its URI (a kind schema
    referencing a sibling kind, ``variable_component.schema.json``), or None when the
    caller has no such document. A ``$ref`` nothing resolves is the same platform bug as
    a malformed schema: it fails open, loudly, instead of raising into the caller (it
    once crashed the saved-reply splitter, 2026-11-02).

    Returns ``(errors, checked)``: ``checked`` is False when the schema could not be
    applied (malformed, or a ``$ref`` nothing resolves) — a SKIP, which a caller must
    never read as a pass (records ``#/$defs/JsonValue``, 2026-11-03).
    """
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing.exceptions import Unresolvable

    try:
        # Never the network: a ``$ref`` resolves only inside the schema or through ``retrieve``.
        validator = Draft202012Validator(schema, registry=_ref_registry(retrieve or _no_document))
        # iter_errors is lazy — a malformed schema can raise SchemaError only
        # once consumed, so materialize the list inside the guard.
        raw = sorted(
            validator.iter_errors(instance),
            key=lambda e: list(e.absolute_path),
        )
    except jsonschema.exceptions.SchemaError as exc:
        logger.error(
            "validate_instance: MALFORMED compiled schema — validation SKIPPED "
            "(failing open). This is a platform bug, not user input. schema=%r err=%s",
            schema,
            exc,
        )
        return [], False
    except Unresolvable as exc:
        logger.error(
            "validate_instance: UNRESOLVABLE $ref in schema — validation SKIPPED "
            "(failing open). This is a platform bug, not user input. schema id=%r err=%r",
            schema.get("$id") if isinstance(schema, dict) else None,
            exc,
        )
        return [], False

    errors: list[str] = []
    for err in raw:
        location = ".".join(str(part) for part in err.absolute_path) or "(value)"
        errors.append(f"{location}: {err.message}")
    return errors, True


_JSON_TYPE_NAMES: dict[type, str] = {
    dict: "object", list: "array", str: "string", bool: "boolean",
    int: "integer", float: "number", type(None): "null",
}


def _violation_path(err: Any, inherited: frozenset[str] = frozenset()) -> str:
    """The failing JSON path, built ONLY from schema-side names.

    An array index is a position, never content, so it is kept. An object key is
    kept only when the schema itself names it on this error's schema path — a key
    the schema does not declare (an open map) is the producer's data and becomes
    ``*``.
    """
    declared = inherited | {part for part in err.schema_path if isinstance(part, str)}
    parts: list[str] = []
    for part in err.absolute_path:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            parts.append(("." if parts else "") + (part if part in declared else "*"))
    return "".join(parts) or "(root)"


def _violation_detail(err: Any, inherited: frozenset[str] = frozenset()) -> str:
    """What the schema expected at this position — schema-side words only."""
    keyword = err.validator
    expected = err.validator_value
    if keyword == "required" and isinstance(err.instance, dict):
        missing = [name for name in expected if name not in err.instance]
        return "required " + ", ".join(repr(name) for name in missing[:5])
    if keyword == "type":
        got = _JSON_TYPE_NAMES.get(type(err.instance), "value")
        return f"type: expected {expected!r}, got {got}"
    if keyword == "const":
        return f"const: expected {expected!r}"
    if keyword == "enum" and isinstance(expected, list):
        shown = ", ".join(repr(item) for item in expected[:6])
        more = f", +{len(expected) - 6} more" if len(expected) > 6 else ""
        return f"enum: expected one of [{shown}{more}]"
    if keyword == "additionalProperties" and isinstance(err.instance, dict):
        return "additionalProperties: undeclared key(s) present"
    if keyword in {"anyOf", "oneOf"}:
        # The closest branch is the one the value got DEEPEST into: a branch rejected
        # at its own root for being the wrong type (``null`` beside an object) is noise.
        context = list(err.context or [])
        if not context:
            return f"{keyword}: no branch matched"
        deeper = [e for e in context if e.relative_path or e.validator != "type"] or context
        inner = max(deeper, key=lambda e: len(e.relative_path))
        names = inherited | {part for part in err.schema_path if isinstance(part, str)}
        return (
            f"{keyword}: no branch matched; closest: "
            f"{_violation_path(inner, names)}: {_violation_detail(inner, names)}"
        )
    if isinstance(expected, (int, float, str)) and not isinstance(expected, bool):
        return f"{keyword}: {expected!r}"
    return str(keyword)


def describe_violations(
    schema: dict[str, Any],
    instance: Any,
    *,
    limit: int = 5,
    retrieve: Callable[[str], dict[str, Any] | None] | None = None,
) -> list[str]:
    """``validate_instance``'s twin for DIAGNOSTICS that may be stored or logged.

    Each line names the failing JSON path, the JSON Schema keyword and what the
    schema expected — ``claims[0]: required 'source_value'``,
    ``rankings[15].__kind: const: expected 'source_authority_ranking'`` — and never
    copies a rejected VALUE (the producer's content), so it is safe in
    ``ops.system_error``. Validation semantics are identical to
    ``validate_instance`` (same validator, same ``$ref`` posture, fails open on a
    malformed schema).
    """
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing.exceptions import Unresolvable

    try:
        validator = Draft202012Validator(schema, registry=_ref_registry(retrieve or _no_document))
        raw = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    except (jsonschema.exceptions.SchemaError, Unresolvable):
        return []
    lines: list[str] = []
    for err in raw:
        line = f"{_violation_path(err)}: {_violation_detail(err)}"
        if line not in lines:
            lines.append(line)
    total = len(lines)
    lines = lines[:limit]
    if total > limit:
        lines.append(f"(+{total - limit} more violation(s))")
    return lines


def schema_validity_errors(schema: Any) -> list[str]:
    """Check that ``schema`` is itself a structurally valid JSON Schema
    (Draft 2020-12 metaschema); return human-readable findings (``[]`` = valid).

    This is the compile-time/resolution-time twin of ``validate_instance``'s
    runtime fail-open guard: instead of discovering a malformed schema when the
    first instance is validated (and skipping loudly), callers can prove schema
    validity up front — ``compile.py`` runs it on every compiled
    ``effective_output_schema``, and the kind catalog (``matrx_graph.kinds``)
    runs it on every resolved ``emitted_json_schema`` so a broken registration
    surfaces as the named degraded reason ``schema_invalid``.

    Pure and side-effect-free: no logging, no policy — the caller decides
    whether findings are loud-only or fatal (enforcement flags).
    """
    if not isinstance(schema, dict):
        return [f"schema must be a JSON object, got {type(schema).__name__}"]
    import jsonschema
    from jsonschema import Draft202012Validator

    try:
        Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "(root)"
        return [f"{location}: {exc.message}"]
    return []


def resume_value_validation_errors(
    interrupt_payload: dict[str, object] | None,
    resume_value: object,
) -> list[str]:
    """Return every schema problem that must block an interrupted resume.

    The interrupt payload is durable checkpoint data, so this function is the
    shared admission seam for HTTP preflight, queued workers, and direct engine
    callers. A malformed authored schema fails closed: it is a platform/author
    defect, but accepting an unvalidated approval would be worse.
    """
    if not interrupt_payload:
        return []
    schema = interrupt_payload.get("schema_hint")
    if schema is None:
        return []
    if not isinstance(schema, dict):
        return [f"(schema): expected a JSON object, got {type(schema).__name__}"]

    schema_errors = schema_validity_errors(schema)
    if schema_errors:
        return [f"(schema): {message}" for message in schema_errors]
    return validate_instance(schema, resume_value)
