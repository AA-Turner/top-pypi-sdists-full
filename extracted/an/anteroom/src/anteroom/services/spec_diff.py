"""Spec diff and invalidation — phase-level diffing and deterministic stale-marking.

Invalidation rules (V1):
1. Requirements changed AND design is approved → design becomes stale
2. Requirements changed AND tasks is approved → tasks becomes stale
3. Design changed AND tasks is approved → tasks becomes stale
"""

from __future__ import annotations

import difflib
import hashlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from .spec_schema import (
    PhaseChange,
    SpecContent,
    SpecDiff,
    SpecPhaseStatus,
    TaskChange,
    parse_spec_content,
)


def diff_spec_versions(
    old: SpecContent,
    new: SpecContent,
    *,
    version_from: int = 0,
    version_to: int = 0,
) -> SpecDiff:
    """Compare two ``SpecContent`` instances and produce a ``SpecDiff``."""
    phase_changes = [
        _diff_phase("requirements", old.requirements, new.requirements),
        _diff_phase("design", old.design, new.design),
    ]
    task_changes = _diff_tasks(old.tasks, new.tasks)
    # Tasks phase is "changed" if the task list itself changed
    tasks_content_old = _tasks_fingerprint(old.tasks)
    tasks_content_new = _tasks_fingerprint(new.tasks)
    phase_changes.append(
        PhaseChange(
            phase="tasks",
            content_changed=tasks_content_old != tasks_content_new,
            content_diff=(
                _unified_diff(tasks_content_old, tasks_content_new) if tasks_content_old != tasks_content_new else None
            ),
        )
    )
    return SpecDiff(
        version_from=version_from,
        version_to=version_to,
        phase_changes=phase_changes,
        task_changes=task_changes,
        invalidations=[],
    )


def evaluate_invalidation_rules(
    old: SpecContent,
    new: SpecContent,
    current_metadata: dict[str, Any],
) -> list[tuple[str, str]]:
    """Evaluate the three deterministic invalidation rules.

    Returns ``[(phase, reason), ...]`` for phases that should become stale.
    Only ``approved`` phases can become stale — ``draft`` phases are unaffected.
    """
    invalidations: list[tuple[str, str]] = []
    phases = current_metadata.get("phases", {})

    req_changed = _phase_hash(old.requirements) != _phase_hash(new.requirements)
    design_changed = _phase_hash(old.design) != _phase_hash(new.design)

    if req_changed:
        design_status = phases.get("design", {}).get("status", "draft")
        if design_status == SpecPhaseStatus.APPROVED.value:
            invalidations.append(("design", "requirements changed after design was approved"))
        tasks_status = phases.get("tasks", {}).get("status", "draft")
        if tasks_status == SpecPhaseStatus.APPROVED.value:
            invalidations.append(("tasks", "requirements changed after tasks were approved"))

    if design_changed:
        tasks_status = phases.get("tasks", {}).get("status", "draft")
        if tasks_status == SpecPhaseStatus.APPROVED.value:
            # Avoid duplicate if already invalidated by requirements change
            if ("tasks", "requirements changed after tasks were approved") not in invalidations:
                invalidations.append(("tasks", "design changed after tasks were approved"))

    return invalidations


def apply_invalidations(
    metadata: dict[str, Any],
    invalidations: list[tuple[str, str]],
) -> dict[str, Any]:
    """Return new metadata with affected phases set to ``stale``.

    Preserves ``approved_at``, ``approved_by``, and ``approved_at_version``
    so the stale reason can be derived later.
    """
    if not invalidations:
        return metadata

    new_meta = dict(metadata)
    phases = dict(new_meta.get("phases", {}))

    for phase, _reason in invalidations:
        phase_data = dict(phases.get(phase, {}))
        phase_data["status"] = SpecPhaseStatus.STALE.value
        phases[phase] = phase_data

    new_meta["phases"] = phases
    return new_meta


def derive_stale_reason(
    db: ThreadSafeConnection,
    artifact_id: str,
    phase: str,
    metadata: dict[str, Any],
) -> str | None:
    """Derive a human-readable stale reason by diffing current content against approved version.

    Returns ``None`` if the phase is not stale.
    """
    from . import artifact_storage

    phases = metadata.get("phases", {})
    phase_data = phases.get(phase, {})
    if phase_data.get("status") != SpecPhaseStatus.STALE.value:
        return None

    approved_ver = phase_data.get("approved_at_version")
    if approved_ver is None:
        return f"Phase '{phase}' is stale (upstream content changed)"

    versions = artifact_storage.list_artifact_versions(db, artifact_id)
    approved_content = None
    for v in versions:
        if v["version"] == approved_ver:
            approved_content = v["content"]
            break

    if approved_content is None:
        return f"Phase '{phase}' is stale (approved version {approved_ver} not found)"

    # Get current content from latest version
    current_content = versions[0]["content"] if versions else None
    if current_content is None:
        return f"Phase '{phase}' is stale (no current version)"

    try:
        old_spec = parse_spec_content(approved_content)
        new_spec = parse_spec_content(current_content)
    except Exception:
        return f"Phase '{phase}' is stale (upstream content changed)"

    # Determine which upstream phase changed
    changed_phases: list[str] = []
    if phase in ("design", "tasks") and _phase_hash(old_spec.requirements) != _phase_hash(new_spec.requirements):
        changed_phases.append("requirements")
    if phase == "tasks" and _phase_hash(old_spec.design) != _phase_hash(new_spec.design):
        changed_phases.append("design")

    if changed_phases:
        return f"Phase '{phase}' is stale: {', '.join(changed_phases)} changed since approval at version {approved_ver}"
    return f"Phase '{phase}' is stale (upstream content changed since version {approved_ver})"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _phase_hash(content: str) -> str:
    return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()


def _diff_phase(phase: str, old_text: str, new_text: str) -> PhaseChange:
    changed = _phase_hash(old_text) != _phase_hash(new_text)
    return PhaseChange(
        phase=phase,
        content_changed=changed,
        content_diff=_unified_diff(old_text, new_text) if changed else None,
    )


def _unified_diff(old: str, new: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            old.strip().splitlines(),
            new.strip().splitlines(),
            lineterm="",
        )
    )


def _tasks_fingerprint(tasks: list[Any]) -> str:
    """Produce a stable text representation of the task list for diffing."""
    lines = []
    for t in tasks:
        deps = ",".join(t.depends_on) if t.depends_on else ""
        lines.append(f"{t.id}: {t.summary} [{deps}]")
    return "\n".join(lines)


def _diff_tasks(old_tasks: list[Any], new_tasks: list[Any]) -> list[TaskChange]:
    old_by_id = {t.id: t for t in old_tasks}
    new_by_id = {t.id: t for t in new_tasks}
    changes: list[TaskChange] = []

    for tid in new_by_id:
        if tid not in old_by_id:
            changes.append(TaskChange(task_id=tid, change_type="added", summary_after=new_by_id[tid].summary))
        elif old_by_id[tid].summary != new_by_id[tid].summary or old_by_id[tid].depends_on != new_by_id[tid].depends_on:
            changes.append(
                TaskChange(
                    task_id=tid,
                    change_type="modified",
                    summary_before=old_by_id[tid].summary,
                    summary_after=new_by_id[tid].summary,
                )
            )

    for tid in old_by_id:
        if tid not in new_by_id:
            changes.append(TaskChange(task_id=tid, change_type="removed", summary_before=old_by_id[tid].summary))

    return changes
