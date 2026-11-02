"""Unit tests for FR-018 conflict detection and resolution."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.conflicts import (
    ProposedEdit,
    UnresolvedConflictError,
    detect_boundary_overlaps,
    detect_proposed_edit_conflicts,
    resolve_conflict,
)
from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
    FileBoundary,
    make_review_only_scope,
    make_subtask_scope,
)


def _subtask(agent_id: str, paths: tuple[str, ...]):
    return make_subtask_scope(
        agent_id=agent_id, issue_key="1", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_resolve_conflict_raises_when_no_authority() -> None:
    detection = detect_boundary_overlaps([_subtask("a", ("x.py",)), _subtask("b", ("x.py",))])
    assert detection is not None
    with pytest.raises(UnresolvedConflictError):
        resolve_conflict(detection, authority=None, grants={}, resolution_decision="n/a")


def test_resolve_conflict_grants_each_contested_path_once() -> None:
    feature = make_review_only_scope(
        agent_id="feature-1", scope_level=AgentScopeLevel.FEATURE, issue_key="1", can_resolve_conflicts=True
    )
    detection = detect_boundary_overlaps([_subtask("a", ("x.py",)), _subtask("b", ("x.py",))])
    assert detection is not None
    resolution = resolve_conflict(
        detection, authority=feature, grants={"a": ("x.py",)}, resolution_decision="keep agent a's version"
    )
    assert resolution.granted_paths == {"a": ("x.py",)}
    assert resolution.resolution_authority == "feature-1"
    detail = resolution.to_event_detail()
    assert detail["resolution_authority"] == "feature-1"
    assert detail["granted_paths"] == {"a": ["x.py"]}


def test_resolve_conflict_rejects_unknown_grant_recipient() -> None:
    feature = make_review_only_scope(
        agent_id="feature-1", scope_level=AgentScopeLevel.FEATURE, issue_key="1", can_resolve_conflicts=True
    )
    detection = detect_boundary_overlaps([_subtask("a", ("x.py",)), _subtask("b", ("x.py",))])
    assert detection is not None
    with pytest.raises(ValueError, match="did not participate"):
        resolve_conflict(detection, authority=feature, grants={"other": ("x.py",)}, resolution_decision="bad")


def test_resolve_conflict_rejects_unauthorized_authority() -> None:
    """resolve_conflict must reject an authority with can_resolve_conflicts=False."""
    feature = make_review_only_scope(
        agent_id="feature-no-resolve",
        scope_level=AgentScopeLevel.FEATURE,
        issue_key="1",
        can_resolve_conflicts=False,  # explicitly unauthorized
    )
    detection = detect_boundary_overlaps([_subtask("a", ("x.py",)), _subtask("b", ("x.py",))])
    assert detection is not None
    with pytest.raises(ValueError, match="not authorized to resolve conflicts"):
        resolve_conflict(detection, authority=feature, grants={"a": ("x.py",)}, resolution_decision="keep a")


def test_resolve_conflict_rejects_cross_path_grant() -> None:
    """An agent that only contested path x.py must not be granted path y.py."""
    feature = make_review_only_scope(
        agent_id="feature-1", scope_level=AgentScopeLevel.FEATURE, issue_key="1", can_resolve_conflicts=True
    )
    # A/B on x.py and B/C on y.py — three-way conflict across two paths.
    edits = [
        ProposedEdit(agent_id="a", path="x.py", summary=None, content="print(1)"),
        ProposedEdit(agent_id="b", path="x.py", summary=None, content="print(2)"),
        ProposedEdit(agent_id="b", path="y.py", summary=None, content="print(3)"),
        ProposedEdit(agent_id="c", path="y.py", summary=None, content="print(4)"),
    ]
    detection = detect_proposed_edit_conflicts(edits)
    assert detection is not None
    # A did not contest y.py — granting y.py to A must be rejected.
    with pytest.raises(ValueError, match="was not a contestant for path 'y.py'"):
        resolve_conflict(
            detection,
            authority=feature,
            grants={"a": ("y.py",), "b": ("x.py",), "c": ()},
            resolution_decision="bad",
        )


def test_resolve_conflict_accepts_valid_per_path_grants() -> None:
    """Agents that contested a path may be granted that path."""
    feature = make_review_only_scope(
        agent_id="feature-1", scope_level=AgentScopeLevel.FEATURE, issue_key="1", can_resolve_conflicts=True
    )
    edits = [
        ProposedEdit(agent_id="a", path="x.py", summary=None, content="print(1)"),
        ProposedEdit(agent_id="b", path="x.py", summary=None, content="print(2)"),
        ProposedEdit(agent_id="b", path="y.py", summary=None, content="print(3)"),
        ProposedEdit(agent_id="c", path="y.py", summary=None, content="print(4)"),
    ]
    detection = detect_proposed_edit_conflicts(edits)
    assert detection is not None
    resolution = resolve_conflict(
        detection,
        authority=feature,
        grants={"a": ("x.py",), "c": ("y.py",)},
        resolution_decision="keep a for x, c for y",
    )
    assert set(resolution.contested_paths) == {"x.py", "y.py"}
