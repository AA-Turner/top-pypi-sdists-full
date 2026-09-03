"""Unit tests for ScopeAgent, FileBoundary immutability and enforcement (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)


def test_subtask_can_modify_files_within_boundary() -> None:
    agent = make_subtask_scope(
        agent_id="subtask-1-py",
        issue_key="1",
        file_boundary=FileBoundary(paths=("a.py", "b.py")),
        specialization=None,
    )
    assert agent.can_modify_files
    assert agent.may_write("a.py")
    assert not agent.may_write("c.py")


@pytest.mark.parametrize("bad_path", ["", "../secret.py", "a\\b.py"])
def test_file_boundary_rejects_invalid_paths(bad_path: str) -> None:
    with pytest.raises(ValueError):
        FileBoundary(paths=(bad_path,))


def test_file_boundary_is_within_rejects_backslash_candidate() -> None:
    """is_within must reject Windows-style paths even when not stored in the boundary."""
    boundary = FileBoundary(paths=("src/main.py",))
    assert not boundary.is_within("src\\main.py")
    assert not boundary.is_within("..\\secret.py")


def test_file_boundary_union_and_overlap() -> None:
    a = FileBoundary(paths=("a.py", "b.py"))
    b = FileBoundary(paths=("b.py", "c.py"))
    assert set(a.union(b).paths) == {"a.py", "b.py", "c.py"}
    assert a.overlaps(b) == ("b.py",)


def test_file_boundary_rejects_non_canonical_paths() -> None:
    """Paths that are syntactically valid but not in canonical POSIX form must be rejected."""
    with pytest.raises(ValueError, match="Non-canonical"):
        FileBoundary(paths=("src/./item.py",))
    with pytest.raises(ValueError, match="Non-canonical"):
        FileBoundary(paths=("src//item.py",))


def test_discovery_only_subtask_rejects_non_empty_boundary() -> None:
    """A discovery_only Subtask agent must have an empty file boundary."""
    with pytest.raises(ValueError, match="discovery_only"):
        make_subtask_scope(
            agent_id="sub-1",
            issue_key="T-1",
            file_boundary=FileBoundary(paths=("src/a.py",)),
            specialization=None,
            discovery_only=True,
        )


def test_discovery_only_subtask_with_empty_boundary_and_no_specialization_is_valid() -> None:
    """A discovery_only Subtask agent with empty boundary and no specialization must succeed."""
    agent = make_subtask_scope(
        agent_id="disc-1",
        issue_key="T-1",
        file_boundary=FileBoundary(),
        specialization=None,
        discovery_only=True,
    )
    assert agent.discovery_only is True
    assert agent.file_boundary.is_empty
