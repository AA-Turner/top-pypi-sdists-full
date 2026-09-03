"""Tests for orchestrate_hierarchy_cmd."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.orchestrator_commands import orchestrate_hierarchy_cmd
from agentic_devtools.orchestration.hierarchy import MasterKeyUnavailableError
from agentic_devtools.orchestration.hierarchy.protected_storage import ProtectedStorage, derive_caller_identity
from agentic_devtools.orchestration.hierarchy.trace import read_events


@pytest.fixture(autouse=True)
def configured_hierarchy_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_HIERARCHY_AUTHORIZED_PRINCIPALS", "runner")
    monkeypatch.setattr(
        "agentic_devtools.orchestration.hierarchy.protected_storage.derive_caller_identity",
        lambda: "runner",
    )


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch(
    "agentic_devtools.orchestration.hierarchy.resolve_authorized_principals",
    side_effect=ValueError("missing allowlist"),
)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id", return_value="42")
def test_orchestrate_hierarchy_cmd_rejects_missing_authorization(
    _mock_issue_id, _mock_principals, _mock_master_key
) -> None:
    assert orchestrate_hierarchy_cmd() == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_returns_error_when_issue_id_missing(mock_issue_id) -> None:
    mock_issue_id.return_value = None
    assert orchestrate_hierarchy_cmd() == 1


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_fails_with_hierarchy_unavailable_without_artifact(
    mock_issue_id,
    mock_state_dir,
    mock_scratch_dir,
    _mock_master_key,
    tmp_path: Path,
) -> None:
    """Without epic-tree.json the command cannot verify standalone status; it must fail."""
    mock_issue_id.return_value = "42"
    mock_state_dir.return_value = tmp_path
    mock_scratch_dir.return_value = tmp_path / "scratch"

    result = orchestrate_hierarchy_cmd()

    assert result == 1

    trace_files = list((tmp_path / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    assert events[-1]["event_type"] == "workflow_completed"
    assert events[-1]["event_detail"]["final_disposition"] == "hierarchy_unavailable"
    assert (tmp_path / "orchestration" / "hierarchy" / "trace-history.ndjson").exists()
    assert (tmp_path / "orchestration" / "hierarchy" / "retention-registry.ndjson").exists()


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_dispatch_not_implemented_for_complete_tree(
    mock_issue_id,
    mock_state_dir,
    mock_repo_root,
    mock_scratch_dir,
    _mock_master_key,
    tmp_path: Path,
    capsys,
) -> None:
    """A non-standalone hierarchy fails until runtime agent dispatch is implemented."""
    mock_issue_id.return_value = "subtask-author-schema"
    mock_state_dir.return_value = tmp_path / "state"
    mock_repo_root.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir
    fixture = Path(__file__).parents[4] / "fixtures" / "epic-tree" / "valid-epic.json"
    (scratch_dir / "epic-tree.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    spec_dir = tmp_path / "specs" / "subtask-author-schema"
    spec_dir.mkdir(parents=True)
    (spec_dir / "tasks.md").write_text(
        "- [ ] T001 subtask-author-schema: `agentic_devtools/schema.py`\n",
        encoding="utf-8",
    )
    (spec_dir / "spec.md").write_text("# Specification\n", encoding="utf-8")
    (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
    feature_spec_dir = tmp_path / "specs" / "feature-schema-validation"
    feature_spec_dir.mkdir(parents=True)
    (feature_spec_dir / "spec.md").write_text("# Feature Spec\n", encoding="utf-8")
    (feature_spec_dir / "plan.md").write_text("# Feature Plan\n", encoding="utf-8")
    (feature_spec_dir / "tasks.md").write_text("# Feature Tasks\n", encoding="utf-8")
    (feature_spec_dir / "research.md").write_text("# Feature Research\n", encoding="utf-8")
    (feature_spec_dir / "generated").mkdir()
    (feature_spec_dir / "generated" / "analysis-report.md").write_text("# Analysis\n", encoding="utf-8")
    epic_spec_dir = tmp_path / "specs" / "epic-standardize-creation"
    epic_spec_dir.mkdir(parents=True)
    (epic_spec_dir / "spec.md").write_text("# Epic Spec\n", encoding="utf-8")
    (epic_spec_dir / "plan.md").write_text("# Epic Plan\n", encoding="utf-8")

    assert orchestrate_hierarchy_cmd() == 1
    assert "dispatch and review are not yet implemented" in capsys.readouterr().out

    trace_files = list((mock_state_dir.return_value / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    event_types = [event["event_type"] for event in events]
    assert "agent_created" not in event_types
    assert "handoff" not in event_types
    assert "review_decision" not in event_types
    assert events[-1]["event_type"] == "workflow_completed"
    assert events[-1]["event_detail"]["final_disposition"] == "hierarchy_dispatch_not_implemented"


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_fails_with_hierarchy_unavailable_when_artifact_absent(
    mock_issue_id,
    mock_state_dir,
    mock_scratch_dir,
    _mock_master_key,
    tmp_path: Path,
    capsys,
) -> None:
    """Absence of epic-tree.json is a discovery failure, not a standalone indicator."""
    mock_issue_id.return_value = "42"
    mock_state_dir.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir

    result = orchestrate_hierarchy_cmd()

    assert result == 1
    assert "hierarchy relationship data is unavailable" in capsys.readouterr().out


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_fails_when_issue_absent_from_hierarchy_artifact(
    mock_issue_id,
    mock_state_dir,
    mock_repo_root,
    mock_scratch_dir,
    _mock_master_key,
    tmp_path: Path,
) -> None:
    """Issue absent from provider-verified epic-tree must fail, not synthesize standalone."""
    mock_issue_id.return_value = "standalone-task"
    mock_state_dir.return_value = tmp_path / "state"
    mock_repo_root.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir
    fixture = Path(__file__).parents[4] / "fixtures" / "epic-tree" / "valid-epic.json"
    (scratch_dir / "epic-tree.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    subtask_spec_dir = tmp_path / "specs" / "standalone-task"
    subtask_spec_dir.mkdir(parents=True)
    (subtask_spec_dir / "tasks.md").write_text(
        "- [ ] T001 standalone-task: `agentic_devtools/schema.py`\n",
        encoding="utf-8",
    )

    result = orchestrate_hierarchy_cmd()

    assert result == 1

    trace_files = list((mock_state_dir.return_value / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    assert events[-1]["event_type"] == "workflow_completed"
    assert events[-1]["event_detail"]["final_disposition"] == "hierarchy_unavailable"


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_invalid_tree(
    mock_issue_id, mock_state_dir, mock_scratch_dir, _mock_master_key, tmp_path: Path, capsys
) -> None:
    mock_issue_id.return_value = "42"
    mock_state_dir.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir
    (scratch_dir / "epic-tree.json").write_text("{not-json", encoding="utf-8")

    assert orchestrate_hierarchy_cmd() == 1
    assert "hierarchy input could not be loaded" in capsys.readouterr().out


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.orchestration.hierarchy.run_discovery")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_discovery_failure(
    mock_issue_id, mock_state_dir, mock_run_discovery, mock_scratch_dir, _mock_master_key, tmp_path: Path, capsys
) -> None:
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import DiscoveryResult

    mock_issue_id.return_value = "42"
    mock_state_dir.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    mock_scratch_dir.return_value = scratch_dir
    artifact = scratch_dir / "epic-tree.json"
    artifact.write_text(
        '{"schemaVersion":"1.0","epic":{"ref":"42","title":"Issue","body":"","features":[]}}',
        encoding="utf-8",
    )
    mock_run_discovery.return_value = DiscoveryResult(outcome="failed", chain=None, error="cycle_detected: boom")

    result = orchestrate_hierarchy_cmd()

    assert result == 1
    assert "hierarchy discovery failed" in capsys.readouterr().out
    trace_files = list((tmp_path / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    assert events[-1]["event_type"] == "workflow_completed"
    assert events[-1]["event_detail"]["final_disposition"] == "hierarchy_discovery_failed"


@patch(
    "agentic_devtools.orchestration.hierarchy.resolve_master_key",
    side_effect=MasterKeyUnavailableError("missing key"),
)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_missing_master_key(mock_issue_id, _mock_resolve_master_key, capsys) -> None:
    mock_issue_id.return_value = "42"

    result = orchestrate_hierarchy_cmd()

    assert result == 1
    assert "AGDT_HIERARCHY_MASTER_KEY" in capsys.readouterr().out


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"short")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_invalid_master_key(mock_issue_id, _mock_resolve_master_key, capsys) -> None:
    mock_issue_id.return_value = "42"

    result = orchestrate_hierarchy_cmd()

    assert result == 1
    assert "hierarchy master key is invalid" in capsys.readouterr().out


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.orchestration.hierarchy.compose_assignment")
@patch("agentic_devtools.orchestration.hierarchy.run_discovery")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_partial_outcome_records_degradation(
    mock_issue_id,
    mock_state_dir,
    mock_run_discovery,
    mock_compose_assignment,
    mock_scratch_dir,
    _mock_master_key,
    tmp_path: Path,
    capsys,
) -> None:
    from agentic_devtools.orchestration.hierarchy.assignment import (
        AssignmentOutcome,
        DegradationRecord,
        HierarchyAssignment,
    )
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import DiscoveryResult

    mock_issue_id.return_value = "42"
    mock_state_dir.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    mock_scratch_dir.return_value = scratch_dir
    (scratch_dir / "epic-tree.json").write_text(
        '{"schemaVersion":"1.0","epic":{"ref":"42","title":"Issue","body":"","features":[]}}',
        encoding="utf-8",
    )

    # Simulate a partial discovery result with a chain present
    from unittest.mock import MagicMock

    chain_mock = MagicMock()
    chain_mock.is_standalone = False
    chain_mock.levels_found = ["subtask"]
    mock_run_discovery.return_value = DiscoveryResult(outcome="partial", chain=chain_mock, error=None)

    degradation = DegradationRecord(
        reason="feature_agent_unavailable",
        missing_level="feature",
        resulting_topology=("subtask",),
    )
    mock_compose_assignment.return_value = HierarchyAssignment(
        outcome=AssignmentOutcome.EPIC_SUBTASK,
        chain=chain_mock,
        degradation=degradation,
    )

    result = orchestrate_hierarchy_cmd()

    assert result == 1

    trace_files = list((tmp_path / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    event_types = [e["event_type"] for e in events]
    assert "degradation" in event_types
    completed = next(e for e in events if e["event_type"] == "workflow_completed")
    assert completed["event_detail"]["outcome"] == "failed"
    assert completed["event_detail"]["final_disposition"] == "hierarchy_dispatch_not_implemented"


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch("agentic_devtools.orchestration.hierarchy.compose_assignment")
@patch("agentic_devtools.orchestration.hierarchy.run_discovery")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_orchestrate_hierarchy_cmd_reports_reduced_scope_without_candidates(
    mock_issue_id,
    mock_state_dir,
    mock_repo_root,
    mock_scratch_dir,
    mock_run_discovery,
    mock_compose_assignment,
    _mock_master_key,
    tmp_path: Path,
) -> None:
    """A hierarchy with no candidate files completes as a reduced-scope run."""
    from agentic_devtools.orchestration.hierarchy.assignment import AssignmentOutcome, HierarchyAssignment
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import DiscoveryResult, HierarchyChain

    mock_issue_id.return_value = "epic-standardize-creation"
    mock_state_dir.return_value = tmp_path
    mock_repo_root.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir
    fixture = Path(__file__).parents[4] / "fixtures" / "epic-tree" / "valid-epic.json"
    (scratch_dir / "epic-tree.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    chain = HierarchyChain(subtask_key="epic-standardize-creation")
    mock_run_discovery.return_value = DiscoveryResult(outcome="success", chain=chain, error=None)
    mock_compose_assignment.return_value = HierarchyAssignment(
        outcome=AssignmentOutcome.STANDALONE,
        chain=chain,
    )

    result = orchestrate_hierarchy_cmd()

    assert result == 0
    trace_files = list((tmp_path / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    assert len(trace_files) == 1
    storage = ProtectedStorage(
        trace_files[0],
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_files[0], protected_storage=storage)
    assert events[-1]["event_type"] == "workflow_completed"
    assert events[-1]["event_detail"]["outcome"] == "partial"
    assert events[-1]["event_detail"]["final_disposition"] == "reduced_scope_success"
    assert (tmp_path / "orchestration" / "hierarchy" / "retention-registry.ndjson").exists()
