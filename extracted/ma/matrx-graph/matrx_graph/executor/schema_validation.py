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
from typing import Any

logger = logging.getLogger(__name__)


def validate_instance(schema: dict[str, Any], instance: Any) -> list[str]:
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
    """
    import jsonschema
    from jsonschema import Draft202012Validator

    try:
        validator = Draft202012Validator(schema)
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
        return []

    errors: list[str] = []
    for err in raw:
        location = ".".join(str(part) for part in err.absolute_path) or "(value)"
        errors.append(f"{location}: {err.message}")
    return errors


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
