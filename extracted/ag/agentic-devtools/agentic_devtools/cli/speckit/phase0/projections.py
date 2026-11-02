"""Human-facing projections for Phase 0 observability (spec #1812).

This module renders the same structured run document (see
:mod:`agentic_devtools.cli.speckit.phase0.observability`) into the three
human-facing surfaces defined by the specification:

- The FR-001 stdout projection (``PHASE0_RUN``/``PHASE0_STAGE`` lines).
- The FR-003 GitHub Actions step summary Markdown template.
- The FR-004 issue-comment Markdown template (with its machine-readable marker).

All renderers treat the structured run document as their sole source of
identifiers, stages, outcomes, freshness, and artifact fields (FR-003, FR-009),
and apply FR-012 sanitization/truncation to untrusted diagnostic text.
"""

from __future__ import annotations

import json
import re
from typing import Any

from agentic_devtools.cli.speckit.phase0.comments import parse_attempt_coordinate
from agentic_devtools.cli.speckit.phase0.identifiers import validate_issue_id, validate_operation_id
from agentic_devtools.cli.speckit.phase0.observability import (
    STAGE_NAMES,
    _is_rfc3339_utc_timestamp,
    compute_next_action,
    redact_secrets,
    sanitize_markdown,
    truncate_utf8,
)

__all__ = [
    "NONE_LITERAL",
    "NOT_EVALUATED_LITERAL",
    "render_stdout_projection",
    "render_actions_summary",
    "render_issue_comment_body",
    "render_marker",
]

NONE_LITERAL = "none"
NOT_EVALUATED_LITERAL = "not evaluated"

# Sentinel distinguishing "caller did not pass pre_publication_last_stage" from an
# explicit None snapshot (which represents a pre-stage cancellation where lastStage
# is legitimately null).
_UNSET: object = object()

_MARKER_TEMPLATE = (
    "<!-- agdt:phase0-status schemaVersion=1.0 chainOperationId={chain_operation_id} "
    "operationId={operation_id} runId={run_id} issueId={issue_id} "
    "attemptStartedAt={attempt_started_at} -->"
)

# Marker attribute values must not contain whitespace, control characters, or
# the literal "-->" / "--!>" terminator sequences that would close the HTML
# comment prematurely.
_MARKER_UNSAFE_RE = re.compile(r"[\s\x00-\x1f\x7f]|--!?>")


def _or_none(value: Any) -> str:
    return NONE_LITERAL if value is None else str(value)


def _validate_marker_param(name: str, value: str) -> None:
    """Raise ValueError if *value* is unsafe for interpolation into an HTML comment.

    Rejects empty values, whitespace, control characters, and the literal
    ``-->`` / ``--!>`` terminator sequences.
    """
    if not value:
        raise ValueError(f"Marker parameter {name!r} must be non-empty")
    if _MARKER_UNSAFE_RE.search(value):
        raise ValueError(
            f"Marker parameter {name!r} must not contain whitespace, control characters, '-->', or '--!>': {value!r}"
        )


def _render_diagnostic_field(value: str) -> str:
    """Sanitize and bound one untrusted diagnostic field for a Markdown surface (FR-012)."""
    return truncate_utf8(sanitize_markdown(redact_secrets(value)))


def _render_optional_diagnostic_field(value: str | None) -> str:
    """Render an optional untrusted diagnostic field, preserving ``none`` for nulls."""
    return NONE_LITERAL if value is None else _render_diagnostic_field(value)


def _select_property_discovery_snapshot(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the highest-sequence ``succeeded``/``partial`` ``property_discovery`` event, if any."""
    candidates = [
        event
        for event in events
        if event["stage"] == "property_discovery" and event["status"] in ("succeeded", "partial")
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda event: event["sequence"])


def _render_property_list(names: list[str]) -> str:
    if not names:
        return NONE_LITERAL
    return _render_diagnostic_field(", ".join(names))


def _render_property_fields(events: list[dict[str, Any]]) -> dict[str, Any]:
    snapshot = _select_property_discovery_snapshot(events)
    if snapshot is None:
        return {
            "captured": "not evaluated",
            "captured_count": "not evaluated",
            "excluded": "not evaluated",
            "excluded_count": "not evaluated",
            "missing": "not evaluated",
            "missing_count": "not evaluated",
            "missing_names": [],
        }

    captured_names = [entry["name"] for entry in snapshot["capturedProperties"]]
    excluded_names = [entry["name"] for entry in snapshot["excludedProperties"]]
    missing_names = list(snapshot["missingProperties"])

    return {
        "captured": _render_property_list(captured_names),
        "captured_count": str(len(captured_names)),
        "excluded": _render_property_list(excluded_names),
        "excluded_count": str(len(excluded_names)),
        "missing": _render_property_list(missing_names),
        "missing_count": str(len(missing_names)),
        "missing_names": missing_names,
    }


def _terminal_event_for_stage(events: list[dict[str, Any]], stage: str) -> dict[str, Any]:
    stage_events = [event for event in events if event["stage"] == stage]
    terminal = [event for event in stage_events if event["status"] != "in_progress"]
    pool = terminal if terminal else stage_events
    return max(pool, key=lambda event: event["sequence"])


def _stages_in_first_seen_order(events: list[dict[str, Any]], *, exclude: str | None = None) -> list[str]:
    seen: dict[str, int] = {}
    for event in events:
        stage = event["stage"]
        if exclude is not None and stage == exclude:
            continue
        if stage not in seen:
            seen[stage] = event["sequence"]
    return sorted(seen, key=lambda stage: seen[stage])


def _render_stage_bullets(events: list[dict[str, Any]], *, exclude: str | None = None) -> str:
    stages = _stages_in_first_seen_order(events, exclude=exclude)
    if not stages:
        return "- Stages:"

    lines = ["- Stages:"]
    for stage in stages:
        terminal_event = _terminal_event_for_stage(events, stage)
        message = _render_diagnostic_field(terminal_event["message"])
        lines.append(f"  - {stage}: {terminal_event['status']} \u2014 {message}")
    return "\n".join(lines)


def _render_freshness(freshness: str) -> str:
    return NOT_EVALUATED_LITERAL if freshness == "not-evaluated" else freshness


def _render_termination_code(termination_code: str | None) -> str:
    return _or_none(termination_code)


def _resolve_next_action(run: dict[str, Any], *, next_action: str | None) -> str:
    """Return the canonical FR-010 next action for *run* and validate caller input."""
    expected = compute_next_action(
        final_outcome=run["finalOutcome"],
        last_stage=run["lastStage"],
        artifact_branch=run["artifactBranch"],
        artifact_path=run["artifactPath"],
        commit_sha=run["commitSha"],
    )
    if next_action is None:
        if expected == NONE_LITERAL:
            return expected
        raise ValueError(f"next_action must be {expected!r} for final_outcome={run['finalOutcome']!r}")
    if next_action != expected:
        raise ValueError(f"next_action must equal derived value {expected!r}, got {next_action!r}")
    return expected


def render_stdout_projection(document: dict[str, Any]) -> str:
    """Render the exact FR-001 stdout projection for a structured run document.

    Args:
        document: A document produced by
            :func:`agentic_devtools.cli.speckit.phase0.observability.serialize_run_document`.

    Returns:
        The header line followed by one ``PHASE0_STAGE`` line per event, in
        ascending ``sequence`` order.
    """
    run = document["run"]
    header = (
        "PHASE0_RUN "
        f"run_id={run['runId']} "
        f"operation_id={run['operationId']} "
        f"issue={run['issueId']} "
        f"outcome={run['finalOutcome']} "
        f"last_stage={_or_none(run['lastStage'])} "
        f"updated_at={run['updatedAt']} "
        f"retry_of={_or_none(run['retryOfRunId'])} "
        f"retry_mode={_or_none(run['retryMode'])} "
        f"freshness={run['freshness']}"
    )

    lines = [header]
    for event in sorted(document["events"], key=lambda item: item["sequence"]):
        message_literal = json.dumps(event["message"], ensure_ascii=False)
        lines.append(
            "PHASE0_STAGE "
            f"seq={event['sequence']} "
            f"stage={event['stage']} "
            f"status={event['status']} "
            f"at={event['timestamp']} "
            f"code={_or_none(event['diagnosticCode'])} "
            f"message={message_literal}"
        )
    return "\n".join(lines)


def render_actions_summary(document: dict[str, Any], *, next_action: str | None) -> str:
    """Render the exact FR-003 GitHub Actions step summary Markdown for *document*.

    Args:
        document: A structured run document (see :func:`render_stdout_projection`).
        next_action: The FR-010 ``Next Action`` value. ``None`` is accepted only
            when the canonical derived value is ``none``.

    Returns:
        The Markdown text of the Actions step summary.
    """
    run = document["run"]
    events = document["events"]
    properties = _render_property_fields(events)
    resolved_next_action = _resolve_next_action(run, next_action=next_action)

    lines = [
        "## Phase 0 Status",
        "",
        f"- Repository: {run['repository']}",
        f"- Workflow Run ID: {run['workflowRunId']}",
        f"- Workflow Run Attempt: {run['workflowRunAttempt']}",
        f"- Run ID: {run['runId']}",
        f"- Operation ID: {run['operationId']}",
        f"- Issue: {run['issueId']}",
        f"- Trigger: {run['trigger']}",
        f"- Source: {run['source']}",
        f"- Provider: {run['provider']}",
        f"- Issue Type: {NONE_LITERAL if run['issueType'] is None else _render_diagnostic_field(run['issueType'])}",
        f"- Configuration Decision: {run['configurationDecision']}",
        f"- Configuration Reason: {_render_diagnostic_field(run['configurationReason'])}",
        f"- Freshness: {_render_freshness(run['freshness'])}",
        f"- Last Known Stage: {_or_none(run['lastStage'])}",
        f"- Selected Template: {_render_optional_diagnostic_field(run['selectedTemplate'])}",
        f"- Captured Properties: {properties['captured']}",
        f"- Captured Count: {properties['captured_count']}",
        f"- Excluded Properties: {properties['excluded']}",
        f"- Excluded Count: {properties['excluded_count']}",
        f"- Missing Properties: {properties['missing']}",
        f"- Missing Count: {properties['missing_count']}",
        f"- Artifact Branch: {_render_optional_diagnostic_field(run['artifactBranch'])}",
        f"- Artifact File: {_render_optional_diagnostic_field(run['artifactPath'])}",
        f"- Commit: {_render_optional_diagnostic_field(run['commitSha'])}",
        f"- Pull Request: {_or_none(run['pullRequestUrl'])}",
        f"- Workflow Run: {run['workflowRunUrl']}",
        f"- Retry Of: {_or_none(run['retryOfRunId'])}",
        f"- Retry Mode: {_or_none(run['retryMode'])}",
        "",
        _render_stage_bullets(events),
        "",
        f"- Final Outcome: {run['finalOutcome']}",
        f"- Termination Code: {_render_termination_code(document['terminationCode'])}",
        f"- Next Action: {resolved_next_action}",
    ]
    return "\n".join(lines)


def render_marker(
    *,
    chain_operation_id: str,
    operation_id: str,
    run_id: str,
    issue_id: str,
    attempt_started_at: str,
) -> str:
    """Render the exact FR-004 machine-readable HTML comment marker line.

    Raises:
        ValueError: If any parameter is empty, contains whitespace, control
            characters, or the sequence ``-->`` / ``--!>`` (which would
            terminate the HTML comment and allow content injection).
    """
    _validate_marker_param("chain_operation_id", chain_operation_id)
    _validate_marker_param("operation_id", operation_id)
    _validate_marker_param("run_id", run_id)
    _validate_marker_param("issue_id", issue_id)
    _validate_marker_param("attempt_started_at", attempt_started_at)
    if not validate_operation_id(chain_operation_id):
        raise ValueError(f"chain_operation_id is not a valid operationId: {chain_operation_id!r}")
    if not validate_operation_id(operation_id):
        raise ValueError(f"operation_id is not a valid operationId: {operation_id!r}")
    if operation_id.startswith("gh-retry:"):
        parts = operation_id.rsplit(":", 3)
        if len(parts) != 4 or parts[0][len("gh-retry:") :] != chain_operation_id:
            raise ValueError("chain_operation_id does not match the chain embedded in operation_id")
    elif operation_id != chain_operation_id:
        raise ValueError("chain_operation_id must match operation_id for non-retry runs")
    if not validate_issue_id(issue_id):
        raise ValueError(f"issue_id is not a valid issueId: {issue_id!r}")
    parse_attempt_coordinate(attempt_started_at=attempt_started_at, run_id=run_id)
    return _MARKER_TEMPLATE.format(
        chain_operation_id=chain_operation_id,
        operation_id=operation_id,
        run_id=run_id,
        issue_id=issue_id,
        attempt_started_at=attempt_started_at,
    )


def render_issue_comment_body(
    document: dict[str, Any],
    *,
    chain_operation_id: str,
    next_action: str | None,
    pre_publication_last_stage: str | None | object = _UNSET,
    pre_publication_updated_at: str | None = None,
    supersedes_identity: str | None = None,
    superseded_by_identity: str | None = None,
) -> str:
    """Render the exact FR-004 issue-comment marker plus Markdown body for *document*.

    Args:
        document: A structured run document (see :func:`render_stdout_projection`).
        chain_operation_id: The originating (non-retry) operation's ``operationId``.
        next_action: The FR-010 ``Next Action`` value. ``None`` is accepted only
            when the canonical derived value is ``none``.
        pre_publication_last_stage: The pre-publication snapshot of
            ``run.lastStage``, captured before the ``issue_comment`` stage is
            attempted. Pass ``None`` explicitly to represent a pre-stage
            cancellation (``lastStage`` was legitimately null at snapshot time).
            When omitted entirely the post-publication ``run['lastStage']`` is
            used as the fallback.
        pre_publication_updated_at: The pre-publication snapshot of
            ``run.updatedAt``. Defaults to ``run['updatedAt']`` when omitted.
        supersedes_identity: The previous publication identity when identity
            rotation occurred, else ``None``.
        superseded_by_identity: The current publication identity when identity
            rotation occurred, else ``None``.

    Returns:
        The full comment body: the marker line followed by the Markdown
        template, with the ``issue_comment`` stage excluded from the stage list.
    """
    run = document["run"]
    events = document["events"]
    resolved_next_action = _resolve_next_action(run, next_action=next_action)
    properties = _render_property_fields(events)
    if run["retryOfRunId"] is None:
        if chain_operation_id != run["operationId"]:
            raise ValueError("chain_operation_id must match run.operationId for non-retry runs")
    else:
        # Extract the embedded chain by stripping the "gh-retry:" prefix and
        # removing the three fixed-format suffixes (time:run_id:attempt) from
        # the right.  A startswith/prefix check is ambiguous because delivery
        # IDs can themselves contain colons.
        parts = run["operationId"][len("gh-retry:") :].rsplit(":", 3)
        if len(parts) != 4 or parts[0] != chain_operation_id:
            raise ValueError("chain_operation_id does not match the chain embedded in run.operationId for retry runs")

    last_stage = pre_publication_last_stage if pre_publication_last_stage is not _UNSET else run["lastStage"]
    if last_stage is not None and last_stage not in STAGE_NAMES:
        raise ValueError(f"pre_publication_last_stage must be a valid Phase 0 stage name, got {last_stage!r}")
    if pre_publication_updated_at is not None and not _is_rfc3339_utc_timestamp(pre_publication_updated_at):
        raise ValueError(
            f"pre_publication_updated_at must be a canonical RFC3339 UTC timestamp, got {pre_publication_updated_at!r}"
        )
    updated_at = pre_publication_updated_at if pre_publication_updated_at is not None else run["updatedAt"]

    # FR-006: supersession fields are a pair — either both present (rotation) or both absent.
    if (supersedes_identity is None) != (superseded_by_identity is None):
        raise ValueError(
            "supersedes_identity and superseded_by_identity must both be provided or both be None; "
            "supply both when identity rotation occurred, omit both when it did not"
        )

    property_guidance = (
        "not evaluated"
        if properties["missing"] == "not evaluated"
        else (
            NONE_LITERAL
            if not properties["missing_names"]
            else _render_diagnostic_field("Provide values for: " + ", ".join(properties["missing_names"]))
        )
    )

    marker = render_marker(
        chain_operation_id=chain_operation_id,
        operation_id=run["operationId"],
        run_id=run["runId"],
        issue_id=run["issueId"],
        attempt_started_at=run["startedAt"],
    )

    supersedes_rendered = _render_diagnostic_field(supersedes_identity) if supersedes_identity else NONE_LITERAL
    superseded_by_rendered = (
        _render_diagnostic_field(superseded_by_identity) if superseded_by_identity else NONE_LITERAL
    )

    lines = [
        marker,
        "## Phase 0 Status",
        "",
        f"- Repository: {run['repository']}",
        f"- Workflow Run ID: {run['workflowRunId']}",
        f"- Workflow Run Attempt: {run['workflowRunAttempt']}",
        f"- Run ID: {run['runId']}",
        f"- Operation ID: {run['operationId']}",
        f"- Issue: {run['issueId']}",
        f"- Updated: {updated_at}",
        f"- Outcome: {run['finalOutcome']}",
        f"- Configuration Decision: {run['configurationDecision']}",
        f"- Configuration Reason: {_render_diagnostic_field(run['configurationReason'])}",
        f"- Last Known Stage: {_or_none(last_stage)}",
        f"- Freshness: {_render_freshness(run['freshness'])}",
        f"- Captured Properties: {properties['captured']}",
        f"- Excluded Properties: {properties['excluded']}",
        f"- Missing Properties: {properties['missing']}",
        f"- Property Guidance: {property_guidance}",
        f"- Selected Template: {_render_optional_diagnostic_field(run['selectedTemplate'])}",
        f"- Artifact Branch: {_render_optional_diagnostic_field(run['artifactBranch'])}",
        f"- Artifact File: {_render_optional_diagnostic_field(run['artifactPath'])}",
        f"- Commit: {_render_optional_diagnostic_field(run['commitSha'])}",
        f"- Pull Request: {_or_none(run['pullRequestUrl'])}",
        f"- Workflow Run: {run['workflowRunUrl']}",
        f"- Supersedes Identity: {supersedes_rendered}",
        f"- Superseded By Identity: {superseded_by_rendered}",
        f"- Retry Of: {_or_none(run['retryOfRunId'])}",
        f"- Retry Mode: {_or_none(run['retryMode'])}",
        "",
        _render_stage_bullets(events, exclude="issue_comment"),
        "",
        f"- Next Action: {resolved_next_action}",
        f"- Termination Code: {_render_termination_code(document['terminationCode'])}",
    ]
    return "\n".join(lines)
