"""Display-only projection and rendering for verified supervisor session evidence."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory, inventory_failure_result
from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import LifecycleAssessment
from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, classify_agent_task_inventory
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun


@dataclass(frozen=True)
class SessionEvidenceDiagnostic:
    """A source-labelled failure retained for supervisor presentation."""

    source: str
    failure_category: FailureCategory | None = None
    http_status: int | None = None
    detail: str = ""


@dataclass(frozen=True)
class SessionEvidencePresentation:
    """Typed activity evidence and only identities verified by collected records."""

    status: SessionOutcome
    display_status: SessionOutcome
    reason: str
    session_active: bool | None
    task_id: str | None = None
    session_id: str | None = None
    diagnostics: tuple[SessionEvidenceDiagnostic, ...] = ()


class SessionEvidenceBuilder:
    """Accumulate presentation facts alongside evidence already collected by the supervisor."""

    def __init__(self) -> None:
        self.diagnostics: list[SessionEvidenceDiagnostic] = []
        self.identities: list[tuple[str, str]] = []

    def record_exception(
        self, source: str, exc: Exception, errors: list[str] | None = None, label: str = "", detail: str = ""
    ) -> None:
        self.diagnostics.append(diagnostic_from_exception(source, exc, detail=detail))
        if errors is not None:
            errors.append(f"{label}: {exc}" if label else str(exc))

    def record_clock_exception(self, task_id: str, session_id: str, exc: Exception) -> str:
        target = session_id or "task"
        self.diagnostics.append(diagnostic_from_exception("session-lookup", exc, detail=f"clock:{task_id}:{target}"))
        return f"clock:{task_id}:{target}:{exc}"

    def classify_and_record_inventory(
        self,
        inventory: AgentTaskInventory,
        now: datetime,
        first_observed_at: dict[str, dict[str, str]],
    ) -> LifecycleAssessment:
        assessment = classify_agent_task_inventory(
            inventory,
            now=now,
            first_observed_at=first_observed_at,
        )
        self.record_lifecycle_inventory(inventory, assessment, now, first_observed_at)
        return assessment

    def record_lifecycle_inventory(
        self,
        inventory: AgentTaskInventory,
        assessment: LifecycleAssessment,
        now: datetime,
        first_observed_at: dict[str, dict[str, str]],
    ) -> None:
        failure_category = inventory.failure_category or assessment.failure_category
        http_status = inventory.http_status if inventory.http_status is not None else assessment.http_status
        if not inventory.complete or failure_category is not None or http_status is not None:
            self.diagnostics.append(
                SessionEvidenceDiagnostic(
                    "lifecycle-reconciliation",
                    failure_category,
                    http_status,
                    ", ".join(inventory.incomplete_reasons) or assessment.reason,
                )
            )
        if assessment.blocking is not True:
            return
        for lifecycle in inventory.tasks:
            clocks = first_observed_at.get(lifecycle.task_id, {})
            for session in lifecycle.sessions:
                session_lifecycle = replace(
                    lifecycle,
                    state="completed",
                    created_at="",
                    started_at="",
                    idle_at="",
                    sessions=(session,),
                )
                if session.session_id and _lifecycle_is_blocking(inventory, session_lifecycle, now, clocks):
                    self.identities.append((lifecycle.task_id, session.session_id))
            if lifecycle.task_id and _lifecycle_is_blocking(inventory, lifecycle, now, clocks):
                self.identities.append((lifecycle.task_id, ""))

    def record_blocking_writer_assessments(
        self, assessments: Sequence[tuple[WorkflowRun, LifecycleAssessment]]
    ) -> list[LifecycleAssessment]:
        blocking: list[LifecycleAssessment] = []
        for run, assessment in assessments:
            if assessment.blocking is True:
                blocking.append(assessment)
                if (
                    run.status.casefold() in {"idle", "in_progress", "running", "waiting", "waiting_for_user"}
                    and assessment.since is not None
                ):
                    self.identities.append((run.task_id, run.session_id))
        return blocking

    def build(self, status: str, reason: str) -> SessionEvidencePresentation:
        session_active = (
            True
            if status in {"blocking", "blocking_with_expired_lifecycle"}
            else False
            if status in {"no_blocking_lifecycle", "expired_ignored_not_completed"}
            else None
        )
        return project_session_evidence(
            session_active=session_active,
            reason=reason or "lifecycle-inventory-unavailable",
            identities=self.identities,
            diagnostics=self.diagnostics,
        )


def diagnostic_from_exception(source: str, exc: Exception, *, detail: str = "") -> SessionEvidenceDiagnostic:
    """Retain structured inventory failure facts without changing collection behavior."""
    try:
        failure = inventory_failure_result(exc)
    except Exception:
        category = None
        status = getattr(exc, "http_status", None)
        status = status if type(status) is int else None
    else:
        category, status = failure.failure_category, failure.http_status
    return SessionEvidenceDiagnostic(source, category, status, detail or str(exc))


def _lifecycle_is_blocking(
    inventory: AgentTaskInventory,
    lifecycle: AgentTaskLifecycle,
    now: datetime,
    first_observed_at: dict[str, str],
) -> bool:
    task_scoped = {"task-detail", "malformed-session", "missing-session-id"}
    reasons = tuple(
        reason
        for reason in inventory.incomplete_reasons
        if reason.partition(":")[0] not in task_scoped or reason.partition(":")[2] == lifecycle.task_id
    )
    single_inventory = AgentTaskInventory(
        (lifecycle,),
        inventory.complete,
        reasons,
        availability=inventory.availability,
        failure_category=inventory.failure_category,
        http_status=inventory.http_status,
    )
    return (
        classify_agent_task_inventory(
            single_inventory,
            now=now,
            first_observed_at={lifecycle.task_id: first_observed_at},
        ).blocking
        is True
    )


def project_session_evidence(
    *,
    session_active: bool | None,
    reason: str,
    identities: Sequence[tuple[str, str]] = (),
    diagnostics: Sequence[SessionEvidenceDiagnostic] = (),
) -> SessionEvidencePresentation:
    """Select one coherent session-bearing record, falling back to a verified task."""
    status = {True: SessionOutcome.ACTIVE, False: SessionOutcome.NONE, None: SessionOutcome.UNKNOWN}[session_active]
    task_id = session_id = None
    for task, session in identities:
        verified_task = task if isinstance(task, str) and task.strip() else None
        verified_session = session if isinstance(session, str) and session.strip() else None
        if verified_session is not None:
            task_id, session_id = verified_task, verified_session
            break
        if task_id is None:
            task_id = verified_task
    display_status = status
    result_diagnostics = list(diagnostics)
    if session_active is True and task_id is None and session_id is None:
        display_status = SessionOutcome.UNKNOWN
        result_diagnostics.append(
            SessionEvidenceDiagnostic(
                "identity-verification",
                detail="active evidence has no verified task or session ID",
            )
        )
    return SessionEvidencePresentation(
        status=status,
        display_status=display_status,
        reason=reason,
        session_active=session_active,
        task_id=task_id,
        session_id=session_id,
        diagnostics=tuple(result_diagnostics),
    )


def session_evidence_to_dict(evidence: SessionEvidencePresentation | None) -> dict[str, Any] | None:
    """Return the stable, JSON-compatible display projection."""
    if evidence is None:
        return None
    return {
        "status": evidence.status.value,
        "display_status": evidence.display_status.value,
        "reason": evidence.reason,
        "session_active": evidence.session_active,
        "task_id": evidence.task_id,
        "session_id": evidence.session_id,
        "diagnostics": [
            {
                "source": diagnostic.source,
                "failure_class": diagnostic.failure_category.value if diagnostic.failure_category else None,
                "http_status": diagnostic.http_status,
                "detail": diagnostic.detail,
            }
            for diagnostic in evidence.diagnostics
        ],
    }


def _render_diagnostic(item: Mapping[str, Any]) -> str:
    failure_class = item.get("failure_class") or "unclassified"
    status = f", HTTP {item['http_status']}" if item.get("http_status") is not None else ""
    detail = f": {item['detail']}" if item.get("detail") else ""
    return f"{item.get('source', 'unknown-source')} ({failure_class}{status}){detail}"


def render_session_evidence(payload: Mapping[str, Any]) -> str:
    """Render one projection without presenting unverifiable activity as active."""
    details = [f"session_active={payload.get('session_active')}"]
    details.extend(f"{key}={payload[key]}" for key in ("task_id", "session_id") if payload.get(key))
    details.extend(_render_diagnostic(item) for item in payload.get("diagnostics", ()) if isinstance(item, Mapping))
    return (
        f"session evidence `{payload.get('display_status', SessionOutcome.UNKNOWN.value)}` "
        f"({payload.get('reason', 'reason unavailable')}; {'; '.join(details)})"
    )


def render_lifecycle_observation(observation: Mapping[str, Any]) -> str:
    """Render existing lifecycle audit fields and the shared session projection."""
    text = (
        f"\n- PR #{observation['pr_number']}: agent-task lifecycle `{observation['status']}` ({observation['reason']})"
    )
    if observation.get("incomplete_reasons"):
        text += f"; incomplete evidence: {', '.join(observation['incomplete_reasons'])}"
    session_evidence = observation.get("session_evidence")
    return f"{text}; {render_session_evidence(session_evidence)}" if isinstance(session_evidence, Mapping) else text


def build_session_evidence_audit(evidence: Sequence[Any]) -> list[dict[str, Any]]:
    """Build a separate audit projection without changing the lifecycle-audit schema."""
    return [
        {
            "pr_number": item.pr_number,
            "session_evidence": session_evidence_to_dict(item.session_evidence),
        }
        for item in evidence
        if item.agent_task_lifecycle_status or (item.session_evidence is not None and item.session_evidence.diagnostics)
    ]


def render_session_evidence_observation(observation: Mapping[str, Any]) -> str:
    """Render session evidence separately from the stable lifecycle audit row."""
    session_evidence = observation.get("session_evidence")
    if not isinstance(session_evidence, Mapping):
        return ""
    return f"\n- PR #{observation['pr_number']}: {render_session_evidence(session_evidence)}"
