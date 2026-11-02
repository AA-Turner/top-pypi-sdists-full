"""Unit tests for the FR-017 exactly-one-lifetime-retry policy."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.retry import (
    is_isolable_subtask_failure,
)


def test_is_isolable_subtask_failure_detects_boundary_overlap() -> None:
    boundaries: dict[str, tuple[str, ...]] = {"a": ("shared.py",), "b": ("shared.py",)}
    assert not is_isolable_subtask_failure(
        failed_agent_id="a", active_subtask_boundaries=boundaries, downstream_dependents=frozenset()
    )


def test_is_isolable_subtask_failure_true_when_disjoint_and_no_dependents() -> None:
    boundaries: dict[str, tuple[str, ...]] = {"a": ("a.py",), "b": ("b.py",)}
    assert is_isolable_subtask_failure(
        failed_agent_id="a", active_subtask_boundaries=boundaries, downstream_dependents=frozenset()
    )


def test_is_isolable_subtask_failure_false_when_downstream_dependent() -> None:
    boundaries: dict[str, tuple[str, ...]] = {"a": ("a.py",), "b": ("b.py",)}
    assert not is_isolable_subtask_failure(
        failed_agent_id="a", active_subtask_boundaries=boundaries, downstream_dependents=frozenset({"b"})
    )


def test_is_isolable_subtask_failure_false_when_failed_boundary_missing() -> None:
    boundaries: dict[str, tuple[str, ...]] = {"b": ("b.py",)}
    assert not is_isolable_subtask_failure(
        failed_agent_id="a", active_subtask_boundaries=boundaries, downstream_dependents=frozenset()
    )
