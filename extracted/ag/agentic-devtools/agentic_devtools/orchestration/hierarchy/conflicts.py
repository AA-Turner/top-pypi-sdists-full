"""Conflict detection and resolution between Subtask Agents (FR-018).

Detects two conflict modes:

1. **Pre-edit boundary overlap** — two or more Subtask Agents declare
   overlapping file-responsibility boundaries before any edit is proposed.
2. **Proposed-edit path overlap** — two or more Subtask Agents propose
   edits to the same file path.

On detection, the workflow must stop before any conflicting edit is
applied. Resolution authority is the Feature Agent when present and not
failed, otherwise the Epic Agent when Epic-level review may continue
independently (FR-017); if neither is eligible, the workflow terminates
with an unresolved-conflict disposition.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field

from .scopes import ScopeAgent


@dataclass(frozen=True)
class ProposedEdit:
    """A Subtask Agent's proposed edit to a single file path."""

    agent_id: str
    path: str
    summary: str | None
    content: str

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()

    @property
    def summary_sha256(self) -> str:
        summary = self.summary or ""
        return hashlib.sha256(summary.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ConflictDetection:
    """A detected conflict awaiting resolution."""

    conflicting_agent_ids: tuple[str, ...]
    contested_paths: tuple[str, ...]
    proposed_edit_summaries: dict[str, dict[str, dict[str, str | None]]]
    participants_per_contested_path: dict[str, frozenset[str]] = field(default_factory=dict)

    @property
    def has_proposed_edits(self) -> bool:
        return bool(self.proposed_edit_summaries)

    def to_event_detail(self) -> dict[str, object]:
        return {
            "conflicting_agent_ids": list(self.conflicting_agent_ids),
            "contested_paths": list(self.contested_paths),
            "proposed_edit_summaries": self.proposed_edit_summaries,
        }


class UnresolvedConflictError(RuntimeError):
    """Raised when no eligible resolution authority exists for a detected conflict."""


def detect_boundary_overlaps(agents: list[ScopeAgent]) -> ConflictDetection | None:
    """Detect overlapping declared file boundaries among Subtask Agents.

    This is the pre-edit conflict mode: no proposed edits are involved yet,
    so ``proposed_edit_summaries`` is always ``{}``.
    """
    conflicting_ids: set[str] = set()
    contested: set[str] = set()
    participants_by_path: dict[str, set[str]] = {}
    for i, agent_a in enumerate(agents):
        for agent_b in agents[i + 1 :]:
            overlap = agent_a.file_boundary.overlaps(agent_b.file_boundary)
            if overlap:
                conflicting_ids.update({agent_a.agent_id, agent_b.agent_id})
                contested.update(overlap)
                for path in overlap:
                    participants_by_path.setdefault(path, set()).update({agent_a.agent_id, agent_b.agent_id})
    if not contested:
        return None
    return ConflictDetection(
        conflicting_agent_ids=tuple(sorted(conflicting_ids)),
        contested_paths=tuple(sorted(contested)),
        proposed_edit_summaries={},
        participants_per_contested_path={path: frozenset(ids) for path, ids in participants_by_path.items()},
    )


def detect_proposed_edit_conflicts(proposed_edits: list[ProposedEdit]) -> ConflictDetection | None:
    """Detect two or more agents proposing edits to the same file path.

    This is the proposed-edit conflict mode: the returned
    ``proposed_edit_summaries`` includes non-sensitive edit metadata
    (summary hash + content hash) for every contested path.
    """
    by_path: dict[str, list[ProposedEdit]] = {}
    for edit in proposed_edits:
        by_path.setdefault(edit.path, []).append(edit)

    contested_paths = sorted(path for path, edits in by_path.items() if len({e.agent_id for e in edits}) > 1)
    if not contested_paths:
        return None

    conflicting_ids: set[str] = set()
    summaries: dict[str, dict[str, dict[str, str | None]]] = {}
    for path in contested_paths:
        path_summaries: dict[str, dict[str, str | None]] = {}
        for edit in by_path[path]:
            conflicting_ids.add(edit.agent_id)
            path_summaries[edit.agent_id] = {
                "summary": None,
                "summary_sha256": edit.summary_sha256,
                "content_sha256": edit.content_sha256,
                "snapshot_ref": None,
            }
        summaries[path] = path_summaries
    return ConflictDetection(
        conflicting_agent_ids=tuple(sorted(conflicting_ids)),
        contested_paths=tuple(contested_paths),
        proposed_edit_summaries=summaries,
        participants_per_contested_path={
            path: frozenset(edit.agent_id for edit in by_path[path]) for path in contested_paths
        },
    )


def eligible_resolution_authority(
    *,
    feature_agent: ScopeAgent | None,
    feature_failed: bool,
    epic_agent: ScopeAgent | None,
    epic_review_independent: bool,
) -> ScopeAgent | None:
    """Return the eligible FR-018 conflict resolution authority, or ``None``.

    The Feature Agent is authoritative when present and not failed.
    Otherwise the Epic Agent is eligible only when epic-level review may
    continue independently of the Feature Agent (FR-017). If neither
    applies, there is no eligible authority.
    """
    if feature_agent is not None and not feature_failed and feature_agent.review_authority.can_resolve_conflicts:
        return feature_agent
    if epic_agent is not None and epic_review_independent and epic_agent.review_authority.can_resolve_conflicts:
        return epic_agent
    return None


@dataclass(frozen=True)
class ConflictResolution:
    """A recorded resolution decision for a detected conflict."""

    resolution_authority: str
    contested_paths: tuple[str, ...]
    granted_paths: dict[str, tuple[str, ...]]
    resolution_decision: str

    def __post_init__(self) -> None:
        contested = set(self.contested_paths)
        seen: set[str] = set()
        for _agent_id, paths in self.granted_paths.items():
            for path in paths:
                if path in seen:
                    msg = f"Path '{path}' granted to more than one agent"
                    raise ValueError(msg)
                seen.add(path)
        if contested and contested != seen:
            msg = "Every contested path must be granted to exactly one agent"
            raise ValueError(msg)

    def to_event_detail(self) -> dict[str, object]:
        return {
            "resolution_authority": self.resolution_authority,
            "contested_paths": list(self.contested_paths),
            "granted_paths": {agent_id: list(paths) for agent_id, paths in self.granted_paths.items()},
            "resolution_decision": self.resolution_decision,
        }


def resolve_conflict(
    detection: ConflictDetection,
    *,
    authority: ScopeAgent | None,
    grants: Mapping[str, tuple[str, ...]],
    resolution_decision: str,
) -> ConflictResolution:
    """Record a resolution for a detected conflict.

    Raises:
        UnresolvedConflictError: If ``authority`` is ``None`` — no eligible
            resolution authority exists and the workflow must terminate
            with an unresolved-conflict disposition instead of calling this
            function.
    """
    if authority is None:
        msg = "No eligible resolution authority exists for this conflict"
        raise UnresolvedConflictError(msg)
    if not authority.review_authority.can_resolve_conflicts:
        msg = f"Agent '{authority.agent_id}' is not authorized to resolve conflicts (can_resolve_conflicts=False)"
        raise ValueError(msg)
    unknown_recipients = set(grants) - set(detection.conflicting_agent_ids)
    if unknown_recipients:
        raise ValueError(f"Grant recipients did not participate in conflict: {sorted(unknown_recipients)}")
    for agent_id, paths in grants.items():
        for path in paths:
            path_participants = detection.participants_per_contested_path.get(path)
            if path_participants is not None and agent_id not in path_participants:
                raise ValueError(f"Agent '{agent_id}' was not a contestant for path '{path}' and cannot be granted it")
    return ConflictResolution(
        resolution_authority=authority.agent_id,
        contested_paths=detection.contested_paths,
        granted_paths={agent_id: tuple(paths) for agent_id, paths in grants.items()},
        resolution_decision=resolution_decision,
    )
