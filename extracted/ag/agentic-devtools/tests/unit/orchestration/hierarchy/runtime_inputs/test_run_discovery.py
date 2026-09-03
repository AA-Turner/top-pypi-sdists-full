"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata
from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    ProviderIssueRelationship,
    read_runtime_hierarchy_input,
    run_discovery,
)


def _rel(
    key: str,
    parent: str | None = None,
    resolvable: bool = True,
    level: HierarchyLevel | None = None,
) -> ProviderIssueRelationship:
    return ProviderIssueRelationship(issue_key=key, parent_key=parent, resolvable=resolvable, level=level)


def test_run_discovery_success_for_complete_chain(tmp_path: Path) -> None:
    relationships = {"3": _rel("3", "2"), "2": _rel("2", "1"), "1": _rel("1", None)}
    result = run_discovery("3", relationships, state_dir=tmp_path, run_id="run-1")
    assert result.outcome == "success"
    assert result.chain is not None
    assert result.input_path is not None
    assert result.input_path.exists()


def test_run_discovery_success_for_standalone(tmp_path: Path) -> None:
    relationships = {"1": _rel("1", None)}
    result = run_discovery("1", relationships, state_dir=tmp_path, run_id="run-1")
    assert result.outcome == "success"
    assert result.chain is not None
    assert result.chain.is_standalone


def test_run_discovery_partial_for_feature_only(tmp_path: Path) -> None:
    relationships = {"2": _rel("2", "1"), "1": _rel("1", None)}
    result = run_discovery("2", relationships, state_dir=tmp_path, run_id="run-1")
    assert result.outcome == "partial"


def test_run_discovery_failed_for_cycle(tmp_path: Path) -> None:
    relationships = {"1": _rel("1", "2"), "2": _rel("2", "1")}
    result = run_discovery("1", relationships, state_dir=tmp_path, run_id="run-1")
    assert result.outcome == "failed"
    assert result.chain is None
    assert result.error is not None
    assert "cycle_detected" in result.error


def test_run_discovery_failed_for_duplicate_parent_claim(tmp_path: Path) -> None:
    # Two distinct dict entries both self-report issue_key "X" with conflicting
    # parents; the subtask_key argument matches the *reported* issue_key, not
    # the dict key, exercising the duplicate-parent short-circuit in run_discovery.
    relationships = {
        "a": ProviderIssueRelationship(issue_key="X", parent_key="P1"),
        "b": ProviderIssueRelationship(issue_key="X", parent_key="P2"),
    }
    result = run_discovery("X", relationships, state_dir=tmp_path, run_id="run-1")
    assert result.outcome == "failed"
    assert result.chain is None
    assert result.error is not None
    assert "duplicate_parent" in result.error


def test_run_discovery_records_divergence_notes_in_written_chain(tmp_path: Path) -> None:
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir()
    write_hierarchy_yml(spec_dir / "hierarchy.yml", HierarchyMetadata(level=HierarchyLevel.TASK, parent=999))
    relationships = {"2": _rel("2", "1"), "1": _rel("1", None)}
    result = run_discovery("2", relationships, state_dir=tmp_path, run_id="run-1", spec_dir=spec_dir)
    assert result.outcome == "partial"
    assert result.chain is not None
    assert result.input_path is not None
    assert result.chain.divergence_notes
    loaded = read_runtime_hierarchy_input(result.input_path)
    assert loaded.divergence_notes == result.chain.divergence_notes
