"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata
from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    HierarchyChain,
    ProviderIssueRelationship,
    compute_divergence,
)


def _rel(
    key: str,
    parent: str | None = None,
    resolvable: bool = True,
    level: HierarchyLevel | None = None,
) -> ProviderIssueRelationship:
    return ProviderIssueRelationship(issue_key=key, parent_key=parent, resolvable=resolvable, level=level)


def test_compute_divergence_returns_empty_for_no_spec_dir() -> None:
    chain = HierarchyChain(subtask_key="1", feature_key=None, epic_key=None)
    assert compute_divergence(chain, None) == ()


def test_compute_divergence_notes_missing_hierarchy_yml(tmp_path: Path) -> None:
    chain = HierarchyChain(subtask_key="2", feature_key="1", epic_key=None)
    notes = compute_divergence(chain, tmp_path)
    assert notes and "missing" in notes[0]


def test_compute_divergence_notes_malformed_hierarchy_yml(tmp_path: Path) -> None:
    (tmp_path / "hierarchy.yml").write_text("not: [valid, yaml:", encoding="utf-8")
    chain = HierarchyChain(subtask_key="2", feature_key="1", epic_key=None)
    notes = compute_divergence(chain, tmp_path)
    assert notes and "could not be parsed" in notes[0]


def test_compute_divergence_detects_parent_mismatch(tmp_path: Path) -> None:
    write_hierarchy_yml(tmp_path / "hierarchy.yml", HierarchyMetadata(level=HierarchyLevel.TASK, parent=999))
    chain = HierarchyChain(subtask_key="2", feature_key="1", epic_key=None)
    notes = compute_divergence(chain, tmp_path)
    assert notes and "diverges" in notes[0]


def test_compute_divergence_no_notes_when_parent_matches(tmp_path: Path) -> None:
    write_hierarchy_yml(tmp_path / "hierarchy.yml", HierarchyMetadata(level=HierarchyLevel.TASK, parent=1))
    chain = HierarchyChain(subtask_key="2", feature_key="1", epic_key=None)
    assert compute_divergence(chain, tmp_path) == ()


def test_compute_divergence_no_notes_when_task_parent_matches_epic_chain(tmp_path: Path) -> None:
    write_hierarchy_yml(tmp_path / "hierarchy.yml", HierarchyMetadata(level=HierarchyLevel.TASK, parent=1))
    chain = HierarchyChain(subtask_key="2", feature_key=None, epic_key="1")
    assert compute_divergence(chain, tmp_path) == ()
