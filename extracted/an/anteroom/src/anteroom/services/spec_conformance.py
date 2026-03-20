"""Spec conformance checks -- deterministic verification of spec vs implementation (#1017).

V1 checks (all deterministic, no AI):
1. Task coverage: do all spec tasks have at least one completed workflow run?
2. Run health: any failed/blocked runs linked to this spec?
3. Phase status: are all phases approved, or are there stale/draft phases?
4. Temporal validity: were runs completed after the tasks phase was approved?
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection


class ConformanceSeverity(str, enum.Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class ConformanceFinding:
    severity: ConformanceSeverity
    category: str  # "task_coverage", "run_health", "phase_status", "temporal"
    message: str
    task_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConformanceResult:
    spec_fqn: str
    spec_version: int
    checked_at: str
    findings: list[ConformanceFinding]

    @property
    def conformant(self) -> bool:
        return not any(f.severity == ConformanceSeverity.ERROR for f in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_fqn": self.spec_fqn,
            "spec_version": self.spec_version,
            "checked_at": self.checked_at,
            "conformant": self.conformant,
            "findings": [
                {
                    "severity": f.severity.value,
                    "category": f.category,
                    "message": f.message,
                    "task_id": f.task_id,
                    "details": f.details,
                }
                for f in self.findings
            ],
        }


def run_conformance_check(db: "ThreadSafeConnection", fqn: str) -> ConformanceResult | None:
    """Run all deterministic conformance checks against a spec.

    Returns ConformanceResult, or None if spec not found.
    """
    from . import artifact_storage
    from .spec_service import get_spec
    from .workflow_storage import list_runs_by_spec

    result = get_spec(db, fqn)
    if result is None:
        return None
    art, spec = result

    versions = artifact_storage.list_artifact_versions(db, art["id"])
    current_version = versions[0]["version"] if versions else 1

    runs = list_runs_by_spec(db, fqn)

    findings: list[ConformanceFinding] = []

    _check_task_coverage(spec, runs, findings)
    _check_run_health(runs, findings)
    _check_phase_status(art["metadata"], findings)
    _check_temporal_validity(art["metadata"], runs, findings)

    return ConformanceResult(
        spec_fqn=fqn,
        spec_version=current_version,
        checked_at=datetime.now(timezone.utc).isoformat(),
        findings=findings,
    )


def _check_task_coverage(
    spec: Any,
    runs: list[dict[str, Any]],
    findings: list[ConformanceFinding],
) -> None:
    """Check that every spec task has at least one completed run."""
    completed_by_task: dict[str, int] = {}
    for run in runs:
        task_id = run.get("task_id")
        if task_id and run.get("status") == "completed":
            completed_by_task[task_id] = completed_by_task.get(task_id, 0) + 1

    for task in spec.tasks:
        count = completed_by_task.get(task.id, 0)
        if count == 0:
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.ERROR,
                    category="task_coverage",
                    message=f"Task '{task.id}' ({task.summary}) has no completed runs",
                    task_id=task.id,
                    details={"completed_runs": 0},
                )
            )
        else:
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.INFO,
                    category="task_coverage",
                    message=f"Task '{task.id}' has {count} completed run(s)",
                    task_id=task.id,
                    details={"completed_runs": count},
                )
            )


def _check_run_health(
    runs: list[dict[str, Any]],
    findings: list[ConformanceFinding],
) -> None:
    """Check for failed or blocked runs."""
    for run in runs:
        task_id = run.get("task_id")
        run_id = run.get("id", "unknown")
        status = run.get("status", "")

        if status == "failed":
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.ERROR,
                    category="run_health",
                    message=f"Run {run_id} failed",
                    task_id=task_id,
                    details={"run_id": run_id, "status": status},
                )
            )
        elif status in ("blocked", "cancelled"):
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.WARNING,
                    category="run_health",
                    message=f"Run {run_id} is {status}",
                    task_id=task_id,
                    details={"run_id": run_id, "status": status},
                )
            )


def _check_phase_status(
    metadata: dict[str, Any],
    findings: list[ConformanceFinding],
) -> None:
    """Check that all phases are approved."""
    from .spec_schema import VALID_PHASE_NAMES, SpecPhaseStatus, get_phase_status

    for phase_name in sorted(VALID_PHASE_NAMES):
        status = get_phase_status(metadata, phase_name)
        if status == SpecPhaseStatus.STALE:
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.WARNING,
                    category="phase_status",
                    message=f"Phase '{phase_name}' is stale -- re-approve before relying on conformance",
                    details={"phase": phase_name, "status": status.value},
                )
            )
        elif status == SpecPhaseStatus.DRAFT:
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.INFO,
                    category="phase_status",
                    message=f"Phase '{phase_name}' is still in draft",
                    details={"phase": phase_name, "status": status.value},
                )
            )


def _check_temporal_validity(
    metadata: dict[str, Any],
    runs: list[dict[str, Any]],
    findings: list[ConformanceFinding],
) -> None:
    """Check that completed runs finished after the tasks phase was approved."""
    phases = metadata.get("phases", {})
    tasks_phase = phases.get("tasks", {})
    tasks_approved_at = tasks_phase.get("approved_at")

    if not tasks_approved_at:
        findings.append(
            ConformanceFinding(
                severity=ConformanceSeverity.INFO,
                category="temporal",
                message="Tasks phase not yet approved -- skipping temporal validity check",
            )
        )
        return

    for run in runs:
        if run.get("status") != "completed":
            continue
        completed_at = run.get("completed_at")
        if not completed_at:
            continue
        task_id = run.get("task_id")
        run_id = run.get("id", "unknown")

        if completed_at < tasks_approved_at:
            findings.append(
                ConformanceFinding(
                    severity=ConformanceSeverity.WARNING,
                    category="temporal",
                    message=f"Run {run_id} completed before tasks phase was approved",
                    task_id=task_id,
                    details={
                        "run_id": run_id,
                        "run_completed": completed_at,
                        "tasks_approved": tasks_approved_at,
                    },
                )
            )
