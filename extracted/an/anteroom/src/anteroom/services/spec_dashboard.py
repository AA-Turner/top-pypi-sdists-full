"""Spec portfolio dashboard aggregation (#1016)."""

from __future__ import annotations

from typing import Any

from anteroom.services import artifact_storage, workflow_storage
from anteroom.services.spec_diff import derive_stale_reason
from anteroom.services.spec_schema import (
    VALID_PHASE_NAMES,
    DashboardTotals,
    RunSummary,
    SpecDashboard,
    SpecPhaseStatus,
    SpecSummary,
    get_phase_status,
)


def _derive_overall_status(
    phases: dict[str, str],
    run_counts: dict[str, int],
) -> str:
    """Derive overall spec status from phase statuses and run state.

    Priority: blocked > stale > draft > in_progress > all_approved.
    """
    if run_counts.get("blocked", 0) > 0:
        return "blocked"

    statuses = set(phases.values())
    if "stale" in statuses:
        return "stale"
    if statuses == {"draft"}:
        return "draft"
    if statuses == {"approved"}:
        return "all_approved"
    return "in_progress"


def get_spec_dashboard(
    db: Any,
    *,
    space_id: str | None = None,
    project_path: str | None = None,
    status: str | None = None,
    namespace: str | None = None,
    has_runs: bool | None = None,
    phase: str | None = None,
    phase_status: str | None = None,
) -> SpecDashboard:
    """Build the spec portfolio dashboard."""
    artifacts = artifact_storage.list_artifacts(
        db,
        artifact_type="spec",
        space_id=space_id,
        project_path=project_path,
    )

    if namespace:
        artifacts = [a for a in artifacts if a.get("namespace") == namespace]

    summaries: list[SpecSummary] = []
    filters_applied: dict[str, str] = {}
    if status:
        filters_applied["status"] = status
    if namespace:
        filters_applied["namespace"] = namespace
    if has_runs is not None:
        filters_applied["has_runs"] = str(has_runs).lower()
    if phase:
        filters_applied["phase"] = phase
    if phase_status:
        filters_applied["phase_status"] = phase_status

    for art in artifacts:
        fqn = art["fqn"]
        metadata = art.get("metadata") or {}

        # Phase statuses
        phases: dict[str, str] = {}
        for phase_name in VALID_PHASE_NAMES:
            phases[phase_name] = get_phase_status(metadata, phase_name).value

        # Run summary
        run_counts = workflow_storage.count_runs_by_spec(db, fqn)
        run_summary = RunSummary(**run_counts)

        # Filter by has_runs
        if has_runs is True and run_summary.total == 0:
            continue
        if has_runs is False and run_summary.total > 0:
            continue

        # Overall status
        overall = _derive_overall_status(phases, run_counts)

        # Filter by status
        if status and overall != status:
            continue

        # Filter by phase + phase_status
        if phase and phase_status:
            if phase not in VALID_PHASE_NAMES:
                continue
            if phases.get(phase) != phase_status:
                continue

        # Stale reasons (only for stale phases)
        stale_reasons: dict[str, str] = {}
        for stale_phase, stale_phase_status in phases.items():
            if stale_phase_status == SpecPhaseStatus.STALE.value:
                reason = derive_stale_reason(db, art["id"], stale_phase, metadata)
                if reason:
                    stale_reasons[stale_phase] = reason

        # Determine mode
        content = art.get("content", "")
        mode = "feature"
        if content and "mode:" in content:
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("mode:"):
                    val = stripped.split(":", 1)[1].strip().strip("\"'")
                    if val == "bugfix":
                        mode = "bugfix"
                    break

        summaries.append(
            SpecSummary(
                fqn=fqn,
                mode=mode,
                source=art.get("source", ""),
                phases=phases,
                overall_status=overall,
                stale_reasons=stale_reasons,
                run_summary=run_summary,
                updated_at=art.get("updated_at", ""),
            )
        )

    totals = DashboardTotals(
        total_specs=len(summaries),
        all_approved=sum(1 for s in summaries if s.overall_status == "all_approved"),
        in_progress=sum(1 for s in summaries if s.overall_status == "in_progress"),
        stale=sum(1 for s in summaries if s.overall_status == "stale"),
        blocked=sum(1 for s in summaries if s.overall_status == "blocked"),
        draft=sum(1 for s in summaries if s.overall_status == "draft"),
    )

    return SpecDashboard(
        specs=summaries,
        totals=totals,
        filters_applied=filters_applied,
    )
