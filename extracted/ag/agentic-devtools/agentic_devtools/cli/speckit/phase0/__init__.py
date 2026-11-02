"""Speckit Phase 0 workflow core (spec #1799) plus observability (spec #1812).

Phase 0 is the label-triggered normalization stage that precedes Phase 1: it
derives a deterministic branch for a source issue, seeds it with a canonical
``issue.md`` artifact, commits it, and opens a pull request.

This package exposes the deterministic derivation and configuration helpers
that the orchestration layer builds on, plus the structured logging,
projection, freshness, and identifier primitives that give maintainers
visibility into Phase 0 runs (FR-001 through FR-012).
"""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.comments import (
    AttemptCoordinate,
    MarkerAttributes,
    compare_attempt_coordinates,
    matches_chain,
    parse_attempt_coordinate,
    parse_marker,
)
from agentic_devtools.cli.speckit.phase0.freshness import (
    DEFAULT_STALENESS_THRESHOLD_DAYS,
    evaluate_freshness,
    parse_last_refreshed,
    render_freshness_for_humans,
    resolve_staleness_threshold_days,
)
from agentic_devtools.cli.speckit.phase0.helpers import (
    derive_artifact_location,
    derive_branch_name,
    derive_issue_key,
    resolve_phase_0_enabled,
)
from agentic_devtools.cli.speckit.phase0.identifiers import (
    canonicalize_json,
    decode_issue_id,
    derive_operation_id_fallback,
    derive_operation_id_from_delivery,
    derive_retry_operation_id,
    derive_run_id,
    derive_source,
    encode_issue_id,
    format_compact_utc_timestamp,
    format_rfc3339_utc,
    validate_issue_id,
    validate_operation_id,
)
from agentic_devtools.cli.speckit.phase0.observability import (
    CONFIGURATION_DECISIONS,
    PROVIDERS,
    RETRY_MODES,
    RUN_OUTCOMES,
    SCHEMA_VERSION,
    SOURCES,
    STAGE_NAMES,
    TERMINATION_CODES,
    Recorder,
    RunRecord,
    StageEvent,
    compute_next_action,
    compute_resumability,
    normalize_missing_properties,
    normalize_property_entries,
    redact_secrets,
    sanitize_control_characters,
    sanitize_markdown,
    serialize_run_document,
    truncate_utf8,
    write_log,
)
from agentic_devtools.cli.speckit.phase0.projections import (
    render_actions_summary,
    render_issue_comment_body,
    render_marker,
    render_stdout_projection,
)

__all__ = [
    # Phase 0 core (spec #1799)
    "derive_artifact_location",
    "derive_branch_name",
    "derive_issue_key",
    "resolve_phase_0_enabled",
    # Identifiers (spec #1812, FR-001)
    "canonicalize_json",
    "decode_issue_id",
    "derive_operation_id_fallback",
    "derive_operation_id_from_delivery",
    "derive_retry_operation_id",
    "derive_run_id",
    "derive_source",
    "encode_issue_id",
    "format_compact_utc_timestamp",
    "format_rfc3339_utc",
    "validate_issue_id",
    "validate_operation_id",
    # Freshness (spec #1812, FR-007/FR-007a/FR-007b)
    "DEFAULT_STALENESS_THRESHOLD_DAYS",
    "evaluate_freshness",
    "parse_last_refreshed",
    "render_freshness_for_humans",
    "resolve_staleness_threshold_days",
    # Observability models and recording (spec #1812, FR-001, FR-010, FR-011, FR-012)
    "CONFIGURATION_DECISIONS",
    "PROVIDERS",
    "RETRY_MODES",
    "RUN_OUTCOMES",
    "SCHEMA_VERSION",
    "SOURCES",
    "STAGE_NAMES",
    "TERMINATION_CODES",
    "Recorder",
    "RunRecord",
    "StageEvent",
    "compute_next_action",
    "compute_resumability",
    "normalize_missing_properties",
    "normalize_property_entries",
    "redact_secrets",
    "sanitize_control_characters",
    "sanitize_markdown",
    "serialize_run_document",
    "truncate_utf8",
    "write_log",
    # Projections (spec #1812, FR-003, FR-004, FR-009)
    "render_actions_summary",
    "render_issue_comment_body",
    "render_marker",
    "render_stdout_projection",
    # Issue-comment marker parsing (spec #1812, FR-004, FR-006)
    "AttemptCoordinate",
    "MarkerAttributes",
    "compare_attempt_coordinates",
    "matches_chain",
    "parse_attempt_coordinate",
    "parse_marker",
]
