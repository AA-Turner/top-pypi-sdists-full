"""Unit tests for FR-018 conflict detection and resolution."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.conflicts import (
    detect_boundary_overlaps,
)
from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)


def _subtask(agent_id: str, paths: tuple[str, ...]):
    return make_subtask_scope(
        agent_id=agent_id, issue_key="1", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_detect_boundary_overlaps_finds_shared_path() -> None:
    a = _subtask("subtask-py", ("shared.py", "a.py"))
    b = _subtask("subtask-md", ("shared.py", "b.md"))
    detection = detect_boundary_overlaps([a, b])
    assert detection is not None
    assert detection.contested_paths == ("shared.py",)
    assert set(detection.conflicting_agent_ids) == {"subtask-py", "subtask-md"}
    assert detection.proposed_edit_summaries == {}
    assert not detection.has_proposed_edits
    detail = detection.to_event_detail()
    assert detail["contested_paths"] == ["shared.py"]
    assert detail["proposed_edit_summaries"] == {}


def test_detect_boundary_overlaps_none_when_disjoint() -> None:
    a = _subtask("subtask-py", ("a.py",))
    b = _subtask("subtask-md", ("b.md",))
    assert detect_boundary_overlaps([a, b]) is None


def test_conflict_detection_populates_participants_per_contested_path() -> None:
    """Boundary-overlap detection must track which agents contested each path."""
    a = _subtask("agent-a", ("shared.py", "only-a.py"))
    b = _subtask("agent-b", ("shared.py", "only-b.py"))
    detection = detect_boundary_overlaps([a, b])
    assert detection is not None
    assert detection.participants_per_contested_path == {"shared.py": frozenset({"agent-a", "agent-b"})}
