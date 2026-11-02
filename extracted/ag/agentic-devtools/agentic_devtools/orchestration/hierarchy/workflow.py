"""Orchestration engine: agent lifecycle, handoffs, review, and enforcement.

Wires together ``assignment.py``, ``context.py``, ``file_classification.py``,
``conflicts.py``, ``retry.py``, and ``trace.py`` into the end-to-end
hierarchy orchestration workflow (FR-001 through FR-018):

- Mechanical file-boundary enforcement (FR-010).
- Subtask → Feature → Epic handoff sequencing and review-stage enforcement
  (FR-009).
- Requirement/architectural violation propagation with corrective actions
  (FR-013).
- Context-provenance propagation into review records (NFR-005).
- Exhausted-source no-edit reduced-scope completion (FR-007, FR-015).
- User-visible status/failure messages identifying scope, stage, and reason
  (NFR-006).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from . import aggregation
from .assignment import HierarchyAssignment
from .conflicts import ConflictDetection, ConflictResolution
from .context import ContextInjectionRecord, ContextProvenance
from .protected_storage import ProtectedStorage
from .retry import AgentFailureEvent
from .scopes import ScopeAgent, provision_capabilities
from .trace import TraceEvent, TraceEventType, append_event, attach_provenance_to_event


@dataclass(frozen=True)
class WriteAttemptResult:
    """The outcome of enforcing a Subtask Agent's declared file boundary."""

    agent_id: str
    path: str
    allowed: bool


def provision_scope_agent(agent: ScopeAgent, available_tools: frozenset[str]) -> ScopeAgent:
    """Provision an agent's canonical capabilities without widening its scope."""
    capabilities = provision_capabilities(agent.scope_level, agent.specialization, available_tools)
    return replace(agent, capabilities=capabilities)


def enforce_file_boundary(
    agent: ScopeAgent,
    path: str,
    *,
    trace_path: Path | None = None,
    protected_storage: ProtectedStorage | None = None,
) -> WriteAttemptResult:
    """Mechanically enforce ``agent``'s declared file boundary for a write attempt (FR-010).

    Feature and Epic agents can never write (their boundary is always
    empty); a Subtask Agent may only write within its declared boundary. A
    blocked attempt is recorded as a ``scope_violation`` trace event when
    ``trace_path`` is provided, the attempted change is discarded, and the
    repository remains unmodified.
    """
    allowed = agent.may_write(path)
    if not allowed and trace_path is not None:
        event = TraceEvent(
            event_type=TraceEventType.SCOPE_VIOLATION,
            agent_scope=agent.scope_level.value,
            event_detail={
                "agent_id": agent.agent_id,
                "attempted_path": path,
                "enforcement": "blocked",
            },
        )
        append_event(trace_path, event, protected_storage=protected_storage)
    return WriteAttemptResult(agent_id=agent.agent_id, path=path, allowed=allowed)


@dataclass(frozen=True)
class ReviewDecision:
    """A higher-level agent's review decision on lower-scope output (FR-013)."""

    agent_id: str
    verdict: str  # "approved" | "rejected" | "revision_requested"
    requirement_ref: str | None = None
    violation_ref: str | None = None
    corrective_action: str | None = None
    provenance: ContextProvenance = ContextProvenance.VERIFIED

    def __post_init__(self) -> None:
        if self.verdict not in ("approved", "rejected", "revision_requested"):
            raise ValueError(f"Invalid verdict: {self.verdict!r}")
        if self.verdict in ("rejected", "revision_requested"):
            if self.violation_ref is None or self.corrective_action is None:
                msg = "violation_ref and corrective_action are required for rejected/revision_requested verdicts"
                raise ValueError(msg)

    def to_event_detail(self) -> dict[str, Any]:
        detail = {
            "agent_id": self.agent_id,
            "verdict": self.verdict,
            "requirement_ref": self.requirement_ref,
            "violation_ref": self.violation_ref,
            "corrective_action": self.corrective_action,
        }
        return attach_provenance_to_event(detail, self.provenance.value)


def propagate_context_provenance(
    context_records: list[ContextInjectionRecord],
    decision: ReviewDecision,
) -> ReviewDecision:
    """Propagate the originating context's provenance into a review decision.

    The review decision preserves the *least* authoritative provenance
    found among the injected context that informed it: if any field the
    reviewer relied on was ``unavailable`` or ``inferred``, the resulting
    decision's provenance MUST reflect that rather than being silently
    promoted to ``verified``.
    """
    worst = ContextProvenance.VERIFIED
    order = {ContextProvenance.VERIFIED: 0, ContextProvenance.INFERRED: 1, ContextProvenance.UNAVAILABLE: 2}
    for record in context_records:
        if record.agent_id != decision.agent_id:
            continue
        for injected_field in record.fields:
            if order[injected_field.provenance] > order[worst]:
                worst = injected_field.provenance
    return ReviewDecision(
        agent_id=decision.agent_id,
        verdict=decision.verdict,
        requirement_ref=decision.requirement_ref,
        violation_ref=decision.violation_ref,
        corrective_action=decision.corrective_action,
        provenance=worst,
    )


def record_handoff(
    trace_path: Path,
    *,
    from_agent_id: str,
    to_agent_id: str,
    outcome: str,
    agent_scope: str,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record a traceable handoff between adjacent hierarchy levels (FR-009, FR-012)."""
    event = TraceEvent(
        event_type=TraceEventType.HANDOFF,
        agent_scope=agent_scope,
        event_detail={"from_agent_id": from_agent_id, "to_agent_id": to_agent_id, "outcome": outcome},
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def record_review_decision(
    trace_path: Path,
    decision: ReviewDecision,
    *,
    agent_scope: str,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record a review decision trace event (FR-009, FR-012, FR-013)."""
    event = TraceEvent(
        event_type=TraceEventType.REVIEW_DECISION,
        agent_scope=agent_scope,
        event_detail=decision.to_event_detail(),
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def run_review_sequence(
    assignment: HierarchyAssignment,
    subtask_agent_ids: list[str],
    *,
    trace_path: Path,
    render_review: Callable[[ScopeAgent], ReviewDecision],
    protected_storage: ProtectedStorage | None = None,
) -> list[ReviewDecision]:
    """Enforce Subtask → Feature → Epic review-stage ordering (FR-009).

    ``render_review`` is called once per higher-level agent (Feature, then
    Epic) in that fixed order; each call's decision is recorded after one or
    more ``handoff`` events. When Subtask agents exist, every subtask emits a
    handoff to the first reviewer.
    When the Feature Agent is absent (or has failed and is excluded from
    ``assignment.review_order`` by the caller), the sequence proceeds
    directly to the Epic Agent and the absence of Feature review output is
    the caller's responsibility to record via a ``degradation`` event.
    """
    decisions: list[ReviewDecision] = []
    previous_agent_id = "orchestrator"
    for index, reviewer in enumerate(assignment.review_order):
        handoff_sources = subtask_agent_ids if index == 0 and subtask_agent_ids else [previous_agent_id]
        for source_agent_id in handoff_sources:
            record_handoff(
                trace_path,
                from_agent_id=source_agent_id,
                to_agent_id=reviewer.agent_id,
                outcome="pending_review",
                agent_scope=reviewer.scope_level.value,
                protected_storage=protected_storage,
            )
        decision = render_review(reviewer)
        if decision.agent_id != reviewer.agent_id:
            raise ValueError(
                f"ReviewDecision.agent_id {decision.agent_id!r} does not match "
                f"the current reviewer {reviewer.agent_id!r}; review provenance is corrupted"
            )
        record_review_decision(
            trace_path,
            decision,
            agent_scope=reviewer.scope_level.value,
            protected_storage=protected_storage,
        )
        decisions.append(decision)
        if decision.verdict in ("rejected", "revision_requested"):
            break
        previous_agent_id = reviewer.agent_id
    return decisions


def record_degradation(
    trace_path: Path,
    *,
    reason: str,
    missing_level: str | None,
    resulting_topology: tuple[str, ...],
    agent_id: str | None = None,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record a graceful-degradation decision (FR-015, FR-012)."""
    detail: dict[str, Any] = {
        "reason": reason,
        "missing_level": missing_level,
        "resulting_topology": list(resulting_topology),
    }
    if agent_id is not None:
        detail["agent_id"] = agent_id
    event = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail=detail,
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def record_agent_failure(
    trace_path: Path,
    agent_scope: str,
    failure: AgentFailureEvent,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record one FR-017 ``agent_failure`` trace event."""
    event = TraceEvent(
        event_type=TraceEventType.AGENT_FAILURE,
        agent_scope=agent_scope,
        event_detail=failure.to_event_detail(),
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def record_conflict_detected(
    trace_path: Path,
    detection: ConflictDetection,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record an FR-018 ``conflict_detected`` trace event (orchestrator-attributed)."""
    event = TraceEvent(
        event_type=TraceEventType.CONFLICT_DETECTED,
        agent_scope="orchestrator",
        event_detail=detection.to_event_detail(),
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def record_conflict_resolved(
    trace_path: Path,
    resolution: ConflictResolution,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record an FR-018 ``conflict_resolved`` trace event (orchestrator-attributed)."""
    event = TraceEvent(
        event_type=TraceEventType.CONFLICT_RESOLVED,
        agent_scope="orchestrator",
        event_detail=resolution.to_event_detail(),
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def record_no_edit_reduced_scope(
    trace_path: Path,
    *,
    agent_id: str,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record the FR-007/FR-015 no-edit reduced-scope outcome when no candidate list exists.

    This is reached only when a discovery-only Subtask Agent inspects the
    repository and still cannot establish any candidate file list. The
    workflow continues rather than stopping; it simply performs no edits
    for this subtask.
    """
    record_degradation(
        trace_path,
        reason="no_candidate_file_list_established",
        missing_level=None,
        resulting_topology=("subtask_no_edit",),
        agent_id=agent_id,
        protected_storage=protected_storage,
    )


@dataclass(frozen=True)
class WorkflowCompletion:
    """The final FR-012 ``workflow_completed`` payload for one orchestration run."""

    outcome: str  # "success" | "partial" | "failed"
    agents_completed: tuple[str, ...]
    agents_skipped: tuple[str, ...]
    final_disposition: str

    def to_event_detail(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "agents_completed": list(self.agents_completed),
            "agents_skipped": list(self.agents_skipped),
            "final_disposition": self.final_disposition,
        }


def record_workflow_completed(
    trace_path: Path,
    completion: WorkflowCompletion,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Record the terminal ``workflow_completed`` trace event (FR-012)."""
    event = TraceEvent(
        event_type=TraceEventType.WORKFLOW_COMPLETED,
        agent_scope="orchestrator",
        event_detail=completion.to_event_detail(),
    )
    append_event(trace_path, event, protected_storage=protected_storage)


def complete_workflow(
    trace_path: Path,
    completion: WorkflowCompletion,
    *,
    protected_storage: ProtectedStorage | None = None,
    trace_history_path: Path | None = None,
    degradation_history_path: Path | None = None,
    run_id: str = "",
    eligible_for_degradation_slo: bool = False,
    elapsed_seconds: float = 0.0,
) -> tuple[aggregation.AlertEvaluation | None, aggregation.AlertEvaluation | None]:
    """Record ``workflow_completed`` and append production SLO aggregation history.

    Wires terminal lifecycle results to NFR-002/NFR-003 by appending the
    completion/degradation terminal records and evaluating operator alerts.
    Lifecycle-start records must be appended when orchestration begins.
    Returns the ``(trace_alert, degradation_alert)`` evaluations (either may
    be ``None`` when the corresponding history path is not supplied).
    """
    record_workflow_completed(trace_path, completion, protected_storage=protected_storage)

    trace_alert = None
    degradation_alert = None
    if trace_history_path is not None:
        aggregation.append_trace_completeness_record(
            trace_history_path,
            run_id=run_id,
            complete=True,
            explicitly_cancelled=completion.final_disposition == "explicitly_cancelled",
        )
        trace_alert = aggregation.evaluate_trace_completeness_alert(trace_history_path)
    if degradation_history_path is not None and eligible_for_degradation_slo:
        aggregation.append_degradation_record(
            degradation_history_path,
            run_id=run_id,
            eligible=True,
            successful=completion.outcome in ("success", "partial")
            and completion.final_disposition != "manual_remediation_required",
            elapsed_seconds=elapsed_seconds,
            explicitly_cancelled=completion.final_disposition == "explicitly_cancelled",
        )
        degradation_alert = aggregation.evaluate_degradation_alert(degradation_history_path)

    return trace_alert, degradation_alert


# --- User-visible status messaging (NFR-006) ------------------------------


def status_message(
    *,
    scope: str,
    stage: str,
    reason: str,
) -> str:
    """Build a user-visible status/failure message identifying scope, stage, and reason.

    NFR-006 requires that any blocked or rejected result identifies the
    active scope, the current review stage, and an actionable reason.
    """
    return f"[{scope}] {stage}: {reason}"


def normal_progress_message(*, scope: str, stage: str) -> str:
    """A normal-progression status message (no failure)."""
    return status_message(scope=scope, stage=stage, reason="in progress")


def rejection_message(*, scope: str, stage: str, violation_ref: str, corrective_action: str) -> str:
    """A rejection status message with the violated requirement/decision and required action."""
    return status_message(
        scope=scope,
        stage=stage,
        reason=f"rejected — violates {violation_ref}; corrective action: {corrective_action}",
    )


def reduced_scope_message(*, scope: str, stage: str, missing_level: str | None) -> str:
    """A reduced-scope degradation status message."""
    reason = f"reduced scope — {missing_level} unavailable" if missing_level else "reduced scope"
    return status_message(scope=scope, stage=stage, reason=reason)


def blocked_message(*, scope: str, stage: str, attempted_path: str) -> str:
    """A blocked-write status message."""
    return status_message(
        scope=scope, stage=stage, reason=f"blocked write to '{attempted_path}' — outside declared boundary"
    )


def provisioning_failure_message(*, scope: str, capability: str) -> str:
    """A capability-provisioning-failure status message."""
    return status_message(scope=scope, stage="provisioning", reason=f"required capability '{capability}' unavailable")


def manual_remediation_message(*, scope: str, agent_id: str, cleanup_reason: str) -> str:
    """A manual-remediation-required status message (terminal cleanup failure)."""
    return status_message(
        scope=scope,
        stage="terminal_cleanup",
        reason=f"agent '{agent_id}' cleanup failed ({cleanup_reason}); manual remediation required",
    )
