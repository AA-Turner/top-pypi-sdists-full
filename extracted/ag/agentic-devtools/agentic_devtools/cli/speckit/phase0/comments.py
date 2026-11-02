"""Issue-comment marker parsing and attempt-ordering helpers (spec #1812, FR-004/FR-006).

This module implements the pure, provider-agnostic parts of the FR-004/FR-006
issue-comment idempotency contract: parsing the machine-readable marker line
rendered by :func:`agentic_devtools.cli.speckit.phase0.projections.render_marker`,
matching a candidate comment against a ``(chainOperationId, issueId)`` pair,
and comparing attempt coordinates so a publisher never overwrites a comment
with an earlier attempt's content.

Provider-specific comment lookup/update (author-aware matching against a live
issue thread) is out of scope for this module; it operates purely on already
retrieved comment bodies and metadata.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from agentic_devtools.cli.speckit.phase0.identifiers import validate_issue_id, validate_operation_id

__all__ = [
    "MarkerAttributes",
    "AttemptCoordinate",
    "parse_marker",
    "matches_chain",
    "parse_attempt_coordinate",
    "compare_attempt_coordinates",
]

_MARKER_PATTERN = re.compile(
    r"<!--\s*agdt:phase0-status\s+"
    r"schemaVersion=(?P<schema_version>1\.0)\s+"
    r"chainOperationId=(?P<chain_operation_id>\S+)\s+"
    r"operationId=(?P<operation_id>\S+)\s+"
    r"runId=(?P<run_id>\S+)\s+"
    r"issueId=(?P<issue_id>\S+)\s+"
    r"attemptStartedAt=(?P<attempt_started_at>\S+)\s*-->"
)

_RUN_ID_PATTERN = re.compile(
    r"^gh:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:(?P<workflow_run_id>[1-9]\d*):(?P<workflow_run_attempt>[1-9]\d*)$"
)
_RFC3339_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _is_rfc3339_utc_timestamp(value: str) -> bool:
    if _RFC3339_UTC_PATTERN.fullmatch(value) is None:
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class MarkerAttributes:
    """The parsed attributes of an FR-004 machine-readable marker line."""

    schema_version: str
    chain_operation_id: str
    operation_id: str
    run_id: str
    issue_id: str
    attempt_started_at: str


@dataclass(frozen=True)
class AttemptCoordinate:
    """The FR-004 total attempt order coordinate: ``(attemptStartedAt, workflowRunId, workflowRunAttempt)``."""

    attempt_started_at: str
    workflow_run_id: int
    workflow_run_attempt: int


def parse_marker(comment_body: str) -> MarkerAttributes | None:
    """Parse the FR-004 marker line from *comment_body*, if present.

    Args:
        comment_body: The full text of a candidate issue comment.

    Returns:
        The parsed :class:`MarkerAttributes`, or ``None`` when no
        well-formed ``agdt:phase0-status`` marker is found.
    """
    match = _MARKER_PATTERN.match(comment_body)
    if match is None:
        return None
    chain_operation_id = match.group("chain_operation_id")
    operation_id = match.group("operation_id")
    run_id = match.group("run_id")
    issue_id = match.group("issue_id")
    attempt_started_at = match.group("attempt_started_at")

    if not validate_operation_id(chain_operation_id) or not validate_operation_id(operation_id):
        return None
    # Cross-field consistency: the declared chainOperationId must equal the chain
    # embedded in operationId.  For non-retry (delivery/fallback) operations the
    # operation is the chain head, so the two fields must be identical.  For retry
    # operations the chain is encoded as the prefix of operationId; strip the three
    # fixed right-hand suffixes (<compact_ts>:<run_id>:<attempt>) to recover it.
    if operation_id.startswith("gh-retry:"):
        retry_parts = operation_id.rsplit(":", 3)
        embedded_chain = retry_parts[0][len("gh-retry:") :]
        if embedded_chain != chain_operation_id:
            return None
    elif operation_id != chain_operation_id:
        return None
    if _RUN_ID_PATTERN.fullmatch(run_id) is None:
        return None
    if not validate_issue_id(issue_id):
        return None
    if not _is_rfc3339_utc_timestamp(attempt_started_at):
        return None

    return MarkerAttributes(
        schema_version=match.group("schema_version"),
        chain_operation_id=chain_operation_id,
        operation_id=operation_id,
        run_id=run_id,
        issue_id=issue_id,
        attempt_started_at=attempt_started_at,
    )


def matches_chain(marker: MarkerAttributes, *, chain_operation_id: str, issue_id: str) -> bool:
    """Return whether *marker* identifies the same retry chain and issue (FR-006).

    Matching by marker attributes alone is necessary but not sufficient per
    FR-006 — callers MUST additionally verify comment authorship against the
    configured publication identity before treating a match as reusable.
    """
    return marker.chain_operation_id == chain_operation_id and marker.issue_id == issue_id


def parse_attempt_coordinate(*, attempt_started_at: str, run_id: str) -> AttemptCoordinate:
    """Derive the FR-004 attempt-order coordinate from a marker's fields.

    Args:
        attempt_started_at: The marker's ``attemptStartedAt`` value.
        run_id: The marker's ``runId`` value
            (``gh:<owner>/<repo>:<workflow_run_id>:<workflow_run_attempt>``).

    Returns:
        The :class:`AttemptCoordinate` used for total ordering.

    Raises:
        ValueError: If *run_id* is not in the canonical ``runId`` shape.
    """
    match = _RUN_ID_PATTERN.fullmatch(run_id)
    if match is None:
        raise ValueError(f"runId is not in the canonical gh:<owner>/<repo>:<run>:<attempt> shape: {run_id!r}")
    if not isinstance(attempt_started_at, str) or not _is_rfc3339_utc_timestamp(attempt_started_at):
        raise ValueError(f"attemptStartedAt is not in the canonical YYYY-MM-DDTHH:MM:SSZ shape: {attempt_started_at!r}")
    return AttemptCoordinate(
        attempt_started_at=attempt_started_at,
        workflow_run_id=int(match.group("workflow_run_id")),
        workflow_run_attempt=int(match.group("workflow_run_attempt")),
    )


def compare_attempt_coordinates(a: AttemptCoordinate, b: AttemptCoordinate) -> int:
    """Compare two attempt coordinates by the FR-004 total order.

    The coordinate is ``(attemptStartedAt, workflowRunId, workflowRunAttempt)``,
    compared by instant (not lexicographically) for the timestamp component and
    numerically for the two run-coordinate tie-breakers.

    Returns:
        A negative number if *a* precedes *b*, zero if they are equal, and a
        positive number if *a* follows *b*.
    """

    def _parse_instant(value: str) -> datetime:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.fromisoformat(normalized)

    time_a, time_b = _parse_instant(a.attempt_started_at), _parse_instant(b.attempt_started_at)
    if time_a != time_b:
        return -1 if time_a < time_b else 1
    if a.workflow_run_id != b.workflow_run_id:
        return -1 if a.workflow_run_id < b.workflow_run_id else 1
    if a.workflow_run_attempt != b.workflow_run_attempt:
        return -1 if a.workflow_run_attempt < b.workflow_run_attempt else 1
    return 0
