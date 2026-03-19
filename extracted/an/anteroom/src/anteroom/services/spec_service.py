"""Spec artifact lifecycle — create, read, update, approve phases, traceability.

All functions operate on the DB via ``artifact_storage`` — no direct SQL.
Phase approval state lives in artifact ``metadata``, not in authored content.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from . import artifact_storage
from .artifacts import ArtifactSource, ArtifactType, build_fqn
from .spec_schema import (
    SpecContent,
    SpecPhaseStatus,
    SpecTask,
    SpecValidationError,
    default_phase_metadata,
    get_phase_status,
    parse_spec_content,
    set_phase_status,
)

logger = logging.getLogger(__name__)


def create_spec(
    db: ThreadSafeConnection,
    namespace: str,
    name: str,
    content_yaml: str,
    source: str | ArtifactSource = ArtifactSource.LOCAL,
    *,
    user_id: str | None = None,
    user_display_name: str | None = None,
) -> dict[str, Any]:
    """Create a new spec artifact after validating YAML content.

    Raises ``SpecValidationError`` if the YAML is invalid.
    """
    parse_spec_content(content_yaml)
    fqn = build_fqn(namespace, ArtifactType.SPEC.value, name)
    metadata = default_phase_metadata()

    return artifact_storage.create_artifact(
        db,
        fqn,
        ArtifactType.SPEC,
        namespace,
        name,
        content_yaml,
        source,
        metadata,
        user_id,
        user_display_name,
    )


def get_spec(db: ThreadSafeConnection, fqn: str) -> tuple[dict[str, Any], SpecContent] | None:
    """Fetch a spec artifact and parse its content.

    Returns ``(artifact_dict, SpecContent)`` or ``None`` if not found.
    Raises ``SpecValidationError`` if the stored content is malformed.
    """
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return None
    if art["type"] != ArtifactType.SPEC.value:
        raise SpecValidationError(f"Artifact {fqn!r} is type '{art['type']}', not 'spec'")
    content = parse_spec_content(art["content"])
    return art, content


def update_spec_content(
    db: ThreadSafeConnection,
    fqn: str,
    content_yaml: str,
) -> dict[str, Any] | None:
    """Update a spec artifact's authored content.

    Validates the new YAML. Triggers auto-versioning when content hash changes.
    Evaluates invalidation rules and applies stale status in a single write.

    Returns the updated artifact dict, or ``None`` if not found.
    Raises ``SpecValidationError`` for invalid YAML.
    """
    new_spec = parse_spec_content(content_yaml)

    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return None
    if art["type"] != ArtifactType.SPEC.value:
        raise SpecValidationError(f"Artifact {fqn!r} is type '{art['type']}', not 'spec'")

    if artifact_storage.is_pack_owned(db, art["id"]):
        raise ValueError(
            f"Spec {fqn!r} is owned by a pack and cannot be edited directly. "
            "Update the spec in the pack source and refresh the pack instead."
        )

    # Evaluate invalidation rules before persisting (single-write)
    from .spec_diff import apply_invalidations, evaluate_invalidation_rules

    old_spec = parse_spec_content(art["content"])
    invalidations = evaluate_invalidation_rules(old_spec, new_spec, art["metadata"])
    updated_metadata = apply_invalidations(art["metadata"], invalidations) if invalidations else None

    return artifact_storage.update_artifact(
        db,
        art["id"],
        content=content_yaml,
        metadata=updated_metadata,
    )


def approve_phase(
    db: ThreadSafeConnection,
    fqn: str,
    phase: str,
    approved_by: str | None = None,
) -> dict[str, Any] | None:
    """Approve a spec phase — metadata-only update, no new content version.

    Records ``approved_at_version`` so stale reasons can be derived later.

    Returns the updated artifact dict, or ``None`` if not found.
    Raises ``ValueError`` for invalid phase names.
    """
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return None
    if art["type"] != ArtifactType.SPEC.value:
        raise SpecValidationError(f"Artifact {fqn!r} is type '{art['type']}', not 'spec'")

    # Get current version number for approved_at_version
    versions = artifact_storage.list_artifact_versions(db, art["id"])
    current_version = versions[0]["version"] if versions else 1

    new_meta = set_phase_status(
        art["metadata"],
        phase,
        SpecPhaseStatus.APPROVED,
        approved_by=approved_by,
        approved_at_version=current_version,
    )
    return artifact_storage.update_artifact(db, art["id"], metadata=new_meta)


def unapprove_phase(
    db: ThreadSafeConnection,
    fqn: str,
    phase: str,
) -> dict[str, Any] | None:
    """Reset a spec phase to draft — metadata-only update.

    Returns the updated artifact dict, or ``None`` if not found.
    Raises ``ValueError`` for invalid phase names.
    """
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return None
    if art["type"] != ArtifactType.SPEC.value:
        raise SpecValidationError(f"Artifact {fqn!r} is type '{art['type']}', not 'spec'")

    new_meta = set_phase_status(art["metadata"], phase, SpecPhaseStatus.DRAFT)
    return artifact_storage.update_artifact(db, art["id"], metadata=new_meta)


def get_phase_statuses(
    db: ThreadSafeConnection,
    fqn: str,
) -> dict[str, SpecPhaseStatus] | None:
    """Return the status of all three phases, or ``None`` if not found."""
    art = artifact_storage.get_artifact_by_fqn(db, fqn)
    if art is None:
        return None
    return {
        "requirements": get_phase_status(art["metadata"], "requirements"),
        "design": get_phase_status(art["metadata"], "design"),
        "tasks": get_phase_status(art["metadata"], "tasks"),
    }


def get_traceability(
    db: ThreadSafeConnection,
    fqn: str,
) -> dict[str, list[dict[str, Any]]] | None:
    """Return traceability from spec tasks to workflow runs.

    Returns ``{task_id: [run_summary, ...]}`` or ``None`` if spec not found.
    """
    result = get_spec(db, fqn)
    if result is None:
        return None
    _art, spec = result

    from .workflow_storage import list_runs_by_spec

    runs = list_runs_by_spec(db, fqn)

    by_task: dict[str, list[dict[str, Any]]] = {t.id: [] for t in spec.tasks}
    for run in runs:
        task_id = run.get("task_id")
        if task_id and task_id in by_task:
            by_task[task_id].append(run)

    return by_task


def get_task(
    db: "ThreadSafeConnection",
    fqn: str,
    task_id: str,
) -> tuple[dict[str, Any], SpecTask] | None:
    """Look up a specific task within a spec.

    Returns ``(artifact_dict, SpecTask)`` or ``None`` if the spec is not found
    or the task ID does not exist in the spec.
    """
    result = get_spec(db, fqn)
    if result is None:
        return None
    art, spec = result
    for task in spec.tasks:
        if task.id == task_id:
            return art, task
    return None


def launch_from_task(
    db: "ThreadSafeConnection",
    fqn: str,
    task_id: str,
    workflow_id: str,
    *,
    extra_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve a spec task and build workflow inputs for launch.

    Raises ``ValueError`` if the spec is not found, the task ID is invalid,
    or the tasks phase is not approved.
    """
    result = get_spec(db, fqn)
    if result is None:
        raise ValueError(f"Spec not found: {fqn!r}")
    art, spec = result

    task: SpecTask | None = None
    for t in spec.tasks:
        if t.id == task_id:
            task = t
            break
    if task is None:
        raise ValueError(f"Task {task_id!r} not found in spec {fqn!r}")

    tasks_status = get_phase_status(art["metadata"], "tasks")
    if tasks_status != SpecPhaseStatus.APPROVED:
        raise ValueError(f"Tasks phase is {tasks_status.value!r}, must be approved before launch")

    inputs: dict[str, Any] = {
        "spec_fqn": fqn,
        "task_id": task_id,
        "task_summary": task.summary,
    }
    if extra_inputs:
        inputs.update(extra_inputs)

    return inputs
