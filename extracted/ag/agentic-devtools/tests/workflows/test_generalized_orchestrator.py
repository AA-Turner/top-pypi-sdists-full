"""Integration tests for generalized orchestration workflow."""

from pathlib import Path
from shutil import copytree as real_copytree
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.orchestrator_commands import (
    _APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY,
    _compute_payload_digest,
    audit_trio_cmd,
    orchestrate_finalize_cmd,
    orchestrate_hierarchy_cmd,
    orchestrate_init_cmd,
    orchestrate_step_cmd,
)
from agentic_devtools.orchestration.hierarchy import ProtectedStorage, derive_caller_identity
from agentic_devtools.orchestration.hierarchy.trace import read_events


def _make_run_result(returncode: int = 0, stdout: str = "", stderr: str = "") -> MagicMock:
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


@patch("agentic_devtools.orchestration.hierarchy.resolve_master_key", return_value=b"x" * 32)
@patch(
    "agentic_devtools.orchestration.hierarchy.resolve_authorized_principals",
    return_value=frozenset({derive_caller_identity()}),
)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_required_issue_id")
def test_epic_tree_orchestration_runs_full_topology(
    mock_issue_id,
    mock_state_dir,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    _mock_authorized_principals,
    _mock_master_key,
    tmp_path: Path,
) -> None:
    """A validated epic tree stops before synthetic lifecycle events when dispatch is unavailable."""
    mock_issue_id.return_value = "subtask-author-schema"
    mock_state_dir.return_value = tmp_path / "state"
    mock_get_repo_root.return_value = tmp_path
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()
    mock_scratch_dir.return_value = scratch_dir

    def _run_safe_side_effect(args, **kwargs):  # type: ignore[no-untyped-def]
        if len(args) >= 3 and args[0] == "git" and args[-2:] == ["rev-parse", "HEAD"]:
            return _make_run_result(returncode=0, stdout="deadbeef\n")
        return _make_run_result(returncode=0, stdout="")

    mock_run_safe.side_effect = _run_safe_side_effect
    fixture = Path(__file__).parents[1] / "fixtures" / "epic-tree" / "valid-epic.json"
    (scratch_dir / "epic-tree.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    subtask_spec_dir = tmp_path / "specs" / "subtask-author-schema"
    subtask_spec_dir.mkdir(parents=True)
    (subtask_spec_dir / "tasks.md").write_text(
        "- [ ] T001 subtask-author-schema: `agentic_devtools/schema.py`\n",
        encoding="utf-8",
    )
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
    trace_path = next((mock_state_dir.return_value / "orchestration" / "hierarchy").rglob("trace.ndjson"))
    storage = ProtectedStorage(
        trace_path,
        master_key=b"x" * 32,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    events = read_events(trace_path, protected_storage=storage)
    event_types = [event["event_type"] for event in events]
    assert "agent_created" not in event_types
    assert "context_injected" not in event_types
    assert "handoff" not in event_types
    assert "review_decision" not in event_types
    assert event_types[-1] == "workflow_completed"
    assert events[-1]["event_detail"]["final_disposition"] == "hierarchy_dispatch_not_implemented"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_full_orchestration_lifecycle(
    mock_get,
    mock_set,
    mock_delete_pin_file,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_bootstrap,
    mock_set_value,
    mock_get_value,
    tmp_path,
):
    state = {}

    def mock_get_workflow_state():
        return state

    def mock_set_workflow_state(active, status, step=None, context=None):
        nonlocal state
        state["active"] = active
        state["status"] = status
        state["step"] = step
        state["context"] = context or {}

    def mock_set_value_side_effect(key, value):
        nonlocal state
        if key == "workflow":
            state.clear()
            state.update(value)

    mock_get.side_effect = mock_get_workflow_state
    mock_set.side_effect = mock_set_workflow_state
    mock_set_value.side_effect = mock_set_value_side_effect
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_copytree.side_effect = real_copytree

    mock_get_value.side_effect = lambda key, required=False: "42" if key == "issue_key" else None

    # git status (clean), branch --list (no branch), worktree add, git -C add, git -C commit, push, code
    mock_run_safe.side_effect = [
        _make_run_result(returncode=0, stdout=""),
        _make_run_result(returncode=0, stdout=""),
        _make_run_result(returncode=0),
        _make_run_result(returncode=0),
        _make_run_result(returncode=0),
        _make_run_result(returncode=0),
        MagicMock(),
    ]

    # create events.jsonl in the scratch dir resolved via mock get_repo_root
    events_dir = repo_root / ".agdt" / "scratch" / "default-feature"
    events_dir.mkdir(parents=True, exist_ok=True)
    (events_dir / "events.jsonl").write_text(
        '{"event":"decomposition"}\n'
        '{"event":"doer_execution"}\n'
        '{"event":"duck_reviews"}\n'
        '{"event":"adjudicator_decision"}\n'
        '{"event":"AWAITING_HUMAN_APPROVAL"}\n',
        encoding="utf-8",
    )

    # 1. Init
    assert orchestrate_init_cmd() == 0
    assert state["step"] == "decomposition"

    # 2. Steps
    assert orchestrate_step_cmd() == 0
    assert state["step"] == "doer_execution"

    assert orchestrate_step_cmd() == 0
    assert state["step"] == "duck_reviews"

    assert orchestrate_step_cmd() == 0
    assert state["step"] == "adjudicator_decision"

    assert orchestrate_step_cmd() == 0
    assert state["step"] == "AWAITING_HUMAN_APPROVAL"
    approved_digest = state["context"][_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY]

    (events_dir / "review-notes.txt").write_text("Updated after approval review.", encoding="utf-8")
    assert orchestrate_step_cmd() == 0
    assert state["step"] == "AWAITING_HUMAN_APPROVAL"
    assert state["context"][_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY] != approved_digest

    # 3. Audit
    audit_trio_cmd()

    # 4. Finalize — succeeds end-to-end, so workflow is marked completed and deactivated
    mock_delete_pin_file.reset_mock()
    assert orchestrate_finalize_cmd() == 0
    assert state["step"] == "completed"
    assert state["status"] == "completed"
    assert state["active"] == ""
    mock_delete_pin_file.assert_called_once_with()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_adjudicator_disagreement_handling(mock_get, mock_set, mock_get_repo_root, tmp_path):
    """Test adjudicator disagreement handling."""
    mock_get.return_value = {"step": "duck_reviews", "active": "orchestrate-feature"}
    mock_get_repo_root.return_value = tmp_path
    assert orchestrate_step_cmd() == 0
    assert mock_set.call_args[1]["step"] == "adjudicator_decision"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_partial_failure_recoveries(
    mock_get, mock_set, mock_get_repo_root, mock_copytree, mock_run_safe, mock_get_value, tmp_path
):
    """Test partial failure recoveries."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.side_effect = lambda key, required=False: "42" if key == "issue_key" else None
    scratch_dir = repo_root / ".agdt" / "scratch" / "default-feature"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    (scratch_dir / "epic-tree.json").write_text(
        '{"schemaVersion":"1.0","epic":{"ref":"epic-1","title":"Generated Epic","body":"","features":[]}}',
        encoding="utf-8",
    )

    # First finalize attempt: worktree add fails → stays at "finalizing"
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: _compute_payload_digest(scratch_dir)},
    }
    mock_run_safe.side_effect = [
        _make_run_result(returncode=0, stdout=""),  # git status (clean)
        _make_run_result(returncode=0, stdout=""),  # git branch --list (no branch)
        _make_run_result(returncode=1, stderr="worktree already exists"),  # git worktree add (fail)
    ]
    assert orchestrate_finalize_cmd() == 1
    assert mock_set.call_args[1]["step"] == "finalizing"

    # Should not finalize if step is not AWAITING_HUMAN_APPROVAL or finalizing
    mock_set.reset_mock()
    mock_run_safe.reset_mock()
    mock_get.return_value = {"step": "decomposition"}
    assert orchestrate_finalize_cmd() == 1
    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_orchestrate_step_refreshes_digest_at_human_approval_gate(mock_get, mock_set, mock_get_repo_root, tmp_path):
    """Test that rerunning the step command at approval refreshes the stored payload digest."""
    state = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {},
    }

    def mock_get_workflow_state():
        return state

    def mock_set_workflow_state(active, status, step=None, context=None):
        nonlocal state
        state["active"] = active
        state["status"] = status
        state["step"] = step
        state["context"] = context or {}

    mock_get.side_effect = mock_get_workflow_state
    mock_set.side_effect = mock_set_workflow_state
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    scratch_dir = repo_root / ".agdt" / "scratch" / "default-feature"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    payload_file = scratch_dir / "epic-tree.json"
    payload_file.write_text("first", encoding="utf-8")

    assert orchestrate_step_cmd() == 0
    first_digest = state["context"][_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY]

    payload_file.write_text("second", encoding="utf-8")
    assert orchestrate_step_cmd() == 0
    second_digest = state["context"][_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY]

    assert state["step"] == "AWAITING_HUMAN_APPROVAL"
    assert first_digest != second_digest
