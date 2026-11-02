"""Pipeline-only rendering of the PR snapshot and typed session evidence."""

from __future__ import annotations

import html
from dataclasses import replace

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.session_evidence_presentation import (
    SessionEvidenceDiagnostic,
    SessionEvidencePresentation,
    project_session_evidence,
    render_session_evidence,
    session_evidence_to_dict,
)


def _render_state_snapshot(
    snapshot: PRStateSnapshot,
    derived_unresolved_threads: int | None = None,
    session_evidence: SessionState | tuple[SessionState, SessionState] | SessionEvidencePresentation | None = None,
) -> str:
    """Render snapshot fields and any typed session evidence collected in this run."""

    def project_state(state: SessionState) -> SessionEvidencePresentation:
        failure_source = state.failure_source
        source = {
            "agent-task-inventory": "session-lookup",
            "agent-task-lifecycle": "lifecycle-reconciliation",
            "unsupported-agent-task-lifecycle": "lifecycle-reconciliation",
        }.get(failure_source or "", failure_source or "session-lookup")
        diagnostics = (
            (SessionEvidenceDiagnostic(source, state.failure_category, state.http_status, failure_source or ""),)
            if failure_source or state.failure_category is not None or state.http_status is not None
            else ()
        )
        projection = project_session_evidence(
            session_active={SessionOutcome.ACTIVE: True, SessionOutcome.UNKNOWN: None}.get(state.outcome, False),
            reason=failure_source or state.outcome.value,
            identities=((state.task_id or "", ""),),
            diagnostics=diagnostics,
        )
        return replace(projection, status=state.outcome)

    def sanitize(value: str) -> str:
        normalized = value.replace("\r\n", "\n").replace("\r", "\n")
        escaped = html.escape(normalized, quote=False)
        return escaped.replace("|", "\\|").replace("\n", "<br>")

    if isinstance(session_evidence, tuple):
        session_projection, lifecycle_projection = (project_state(state) for state in session_evidence)
        projections = (session_projection, lifecycle_projection)
        diagnostics = tuple(item for projection in projections for item in projection.diagnostics)
        identities = tuple((projection.task_id or "", projection.session_id or "") for projection in projections)
        not_found = any(
            item.failure_category is FailureCategory.HTTP_NOT_FOUND or item.http_status == 404 for item in diagnostics
        )
        active = session_projection.display_status is SessionOutcome.ACTIVE and not not_found
        combined = project_session_evidence(
            session_active=True
            if active
            else None
            if not_found or session_projection.display_status is SessionOutcome.UNKNOWN
            else False,
            reason="incomplete-session-evidence" if not_found else session_projection.reason,
            identities=identities,
            diagnostics=diagnostics,
        )
        session_evidence = replace(
            combined,
            status=SessionOutcome.UNKNOWN if not_found else session_projection.status,
        )
    elif isinstance(session_evidence, SessionState):
        session_evidence = project_state(session_evidence)

    head_sha_short = sanitize(snapshot.head_sha[:7])
    review_state = sanitize(snapshot.review_state or "none")
    inline_count = snapshot.copilot_review_inline_count
    inline_count_unknown = inline_count is None or inline_count < 0
    show_inline_suffix = (
        snapshot.review_state == "COMMENTED" or inline_count_unknown or (inline_count is not None and inline_count > 0)
    )
    if show_inline_suffix:
        if inline_count_unknown:
            inline_suffix = " (inline unknown)"
        else:
            inline_suffix = f" ({sanitize(str(inline_count))} inline)"
    else:
        inline_suffix = ""
    labels = sanitize(", ".join(snapshot.labels) if snapshot.labels else "none")
    if snapshot.unresolved_threads_degraded:
        unresolved_threads = f"degraded / unknown (blocking sentinel {sanitize(str(snapshot.unresolved_threads))})"
    else:
        unresolved_threads = sanitize(str(snapshot.unresolved_threads))
    if derived_unresolved_threads is not None and derived_unresolved_threads != snapshot.unresolved_threads:
        unresolved_threads += f" (gates saw: {sanitize(str(derived_unresolved_threads))})"

    session_line = "- Copilot session active: N/A"
    evidence_payload = session_evidence_to_dict(session_evidence)
    if evidence_payload is not None:
        session_line = f"- Copilot session: {sanitize(render_session_evidence(evidence_payload))}"

    lines = [
        f"- HEAD: `{head_sha_short}`",
        f"- Commits above merge-base: {sanitize(str(snapshot.commit_count))}",
        session_line,
        f"- Copilot review on HEAD: {review_state}{inline_suffix}",
        f"- CI: {sanitize(snapshot.ci_status)}",
        f"- Unresolved threads: {unresolved_threads}",
        f"- Draft: {sanitize(str(snapshot.is_draft))}",
        f"- Labels: {labels}",
    ]
    return "\n".join(lines)


def combine_current_run_session_evidence(
    session_state: SessionState | None,
    lifecycle_state: SessionState | None,
) -> SessionState | tuple[SessionState, SessionState] | None:
    """Return current-run evidence, preserving source identity and order."""
    if session_state is None:
        return lifecycle_state
    if lifecycle_state is None:
        return session_state
    return session_state, lifecycle_state
