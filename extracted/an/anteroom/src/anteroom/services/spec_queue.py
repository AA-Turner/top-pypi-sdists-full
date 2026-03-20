"""Spec review queue -- aggregation queries for the review inbox (#1015)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection


@dataclass(frozen=True)
class ReviewQueueItem:
    fqn: str
    category: str  # "needs_review", "stale", "blocked"
    phases: dict[str, str]  # phase -> status
    stale_reasons: dict[str, str]  # phase -> reason (for stale items only)
    blocked_runs: list[dict[str, Any]]  # spec-gate-blocked workflow runs
    updated_at: str


@dataclass(frozen=True)
class ReviewQueue:
    needs_review: list[ReviewQueueItem]
    stale: list[ReviewQueueItem]
    blocked: list[ReviewQueueItem]
    total: int


def get_review_queue(
    db: "ThreadSafeConnection",
    *,
    space_id: str | None = None,
    project_path: str | None = None,
) -> ReviewQueue:
    """Build the review queue by scanning attached spec artifacts."""
    from . import artifact_storage
    from .artifacts import ArtifactType
    from .spec_diff import derive_stale_reason
    from .spec_schema import VALID_PHASE_NAMES, SpecPhaseStatus, get_phase_status
    from .workflow_storage import list_spec_blocked_runs

    # Use attached_only=True when context is available to prevent
    # detached pack specs from leaking into the review surface.
    _attached = space_id is not None or project_path is not None
    all_artifacts = artifact_storage.list_artifacts(
        db,
        artifact_type=ArtifactType.SPEC.value,
        attached_only=_attached,
        space_id=space_id,
        project_path=project_path,
    )

    needs_review: list[ReviewQueueItem] = []
    stale: list[ReviewQueueItem] = []
    blocked: list[ReviewQueueItem] = []

    for art in all_artifacts:
        metadata = art.get("metadata", {})
        phases: dict[str, str] = {}
        stale_reasons: dict[str, str] = {}
        has_draft = False
        has_stale = False

        for phase_name in VALID_PHASE_NAMES:
            status = get_phase_status(metadata, phase_name)
            phases[phase_name] = status.value
            if status == SpecPhaseStatus.DRAFT:
                has_draft = True
            elif status == SpecPhaseStatus.STALE:
                has_stale = True
                reason = derive_stale_reason(db, art["id"], phase_name, metadata)
                if reason:
                    stale_reasons[phase_name] = reason

        blocked_runs = list_spec_blocked_runs(db, art["fqn"])

        if has_draft or has_stale:
            item = ReviewQueueItem(
                fqn=art["fqn"],
                category="needs_review",
                phases=phases,
                stale_reasons=stale_reasons,
                blocked_runs=blocked_runs,
                updated_at=art.get("updated_at", art.get("created_at", "")),
            )
            needs_review.append(item)

        if has_stale:
            stale_item = ReviewQueueItem(
                fqn=art["fqn"],
                category="stale",
                phases=phases,
                stale_reasons=stale_reasons,
                blocked_runs=blocked_runs,
                updated_at=art.get("updated_at", art.get("created_at", "")),
            )
            stale.append(stale_item)

        if blocked_runs:
            blocked_item = ReviewQueueItem(
                fqn=art["fqn"],
                category="blocked",
                phases=phases,
                stale_reasons=stale_reasons,
                blocked_runs=blocked_runs,
                updated_at=art.get("updated_at", art.get("created_at", "")),
            )
            blocked.append(blocked_item)

    needs_review.sort(key=lambda x: x.updated_at, reverse=True)
    stale.sort(key=lambda x: x.updated_at, reverse=True)
    blocked.sort(key=lambda x: x.updated_at, reverse=True)

    return ReviewQueue(
        needs_review=needs_review,
        stale=stale,
        blocked=blocked,
        total=len(needs_review),
    )
