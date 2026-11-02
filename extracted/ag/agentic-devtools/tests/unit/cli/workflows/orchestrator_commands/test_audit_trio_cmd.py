"""Tests for audit_trio_cmd."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.orchestrator_commands import audit_trio_cmd


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path

        # Test without events.jsonl
        with pytest.raises(FileNotFoundError):
            audit_trio_cmd()

        # Test with events.jsonl (valid JSON with empty lines)
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n'
            '{"event":"finalizing"}\n'
            '{"event":"completed"}\n',
            encoding="utf-8",
        )
        audit_trio_cmd()

        # Test with invalid events.jsonl
        (scratch_dir / "events.jsonl").write_text("{invalid json", encoding="utf-8")
        with pytest.raises(ValueError, match="Malformed JSON"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_non_object_event_row(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('"scalar"\n', encoding="utf-8")

        with pytest.raises(ValueError, match="must be a JSON object"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_unknown_event(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"event":"unexpected"}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="unsupported type"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_completed_without_finalizing(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n'
            '{"event":"completed"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="requires a prior finalizing event"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_reversed_finalization_order(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"completed"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n'
            '{"event":"finalizing"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="require an AWAITING_HUMAN_APPROVAL gate event"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_requires_gate_before_finalizing(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"finalizing"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="require an AWAITING_HUMAN_APPROVAL gate event"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_missing_event_field(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"type":"decomposition"}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="missing string field 'event'"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_empty_events_file(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text("\n   \n", encoding="utf-8")

        with pytest.raises(ValueError, match="must contain at least one non-empty event object"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_out_of_order_lifecycle(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"duck_reviews"}\n{"event":"decomposition"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="appears out of lifecycle order"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_lifecycle_regression_after_retry(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n{"event":"doer_execution"}\n{"event":"decomposition"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="appears out of lifecycle order"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_post_completion_regression(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n'
            '{"event":"finalizing"}\n'
            '{"event":"completed"}\n'
            '{"event":"finalizing"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="appears out of lifecycle order"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_requires_gate_for_finalization_events(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"finalizing"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="require an AWAITING_HUMAN_APPROVAL gate event"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_allows_partial_lifecycle_without_finalization_events(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n{"event":"doer_execution"}\n',
            encoding="utf-8",
        )

        audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_skipped_lifecycle_stages_before_gate(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n{"event":"AWAITING_HUMAN_APPROVAL"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="appears out of lifecycle order"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_accepts_artifact_event_types(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        # Verify that all declared artifact event types are accepted by the validator.
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"review","review":{"result":"pass"}}\n'
            '{"event":"response","response":{"accepted":true}}\n'
            '{"event":"adjudication","adjudication":{"decision":"accept"}}\n'
            '{"event":"promotion","promotion":{"target":"next"}}\n'
            '{"event":"audit","audit":{"status":"ok"}}\n'
            '{"event":"state_verify","state_verify":{"ok":true}}\n'
            '{"event":"invocation_failure","invocation_failure":{"reason":"timeout"}}\n'
            '{"event":"issue_reconciled","issue_reconciled":{"issue":"42"}}\n'
            '{"event":"state_transition","state_transition":{"from":"a","to":"b"}}\n'
            '{"event":"assignment","assignment":{"assignee":"duck-1"}}\n',
            encoding="utf-8",
        )

        audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_falls_back_to_cwd_when_repo_root_is_none(mock_get, tmp_path):
    """_get_scratch_dir falls back to cwd when get_repo_root() returns None."""
    mock_get.return_value = {}
    with (
        patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_repo_root,
        patch("pathlib.Path.cwd", return_value=tmp_path),
    ):
        mock_repo_root.return_value = None

        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n',
            encoding="utf-8",
        )

        audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_artifact_event_without_payload(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"event":"review"}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="must include exactly one payload field"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_artifact_event_with_extra_payload_fields(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"event":"review","review":{},"x":1}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="must include exactly one payload field"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_non_object_artifact_payload(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"event":"review","review":1}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="must use an object payload"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_extra_lifecycle_events_after_completion(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text(
            '{"event":"decomposition"}\n'
            '{"event":"doer_execution"}\n'
            '{"event":"duck_reviews"}\n'
            '{"event":"adjudicator_decision"}\n'
            '{"event":"AWAITING_HUMAN_APPROVAL"}\n'
            '{"event":"finalizing"}\n'
            '{"event":"completed"}\n'
            '{"event":"completed"}\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="contains extra events after completion"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_symlinked_events_path(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        outside = tmp_path / "outside"
        outside.mkdir()
        (scratch_dir / "events.jsonl").symlink_to(outside / "events.jsonl")

        with pytest.raises(ValueError, match="events path is a symlink"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_requires_regular_events_file(mock_get, tmp_path):
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").mkdir()

        with pytest.raises(ValueError, match="Events file must be a regular file"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_nan_in_event_payload(mock_get, tmp_path):
    """json.loads accepts NaN silently; audit must reject it as non-standard JSON."""
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        # NaN is not valid JSON but Python's json.loads accepts it as a float
        (scratch_dir / "events.jsonl").write_text('{"event":"review","review":{"score":NaN}}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="Non-standard JSON constant"):
            audit_trio_cmd()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_audit_trio_cmd_rejects_infinity_in_event_payload(mock_get, tmp_path):
    """json.loads accepts Infinity silently; audit must reject it as non-standard JSON."""
    mock_get.return_value = {}
    with patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root") as mock_get_repo_root:
        mock_get_repo_root.return_value = tmp_path
        scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        (scratch_dir / "events.jsonl").write_text('{"event":"review","review":{"val":Infinity}}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="Non-standard JSON constant"):
            audit_trio_cmd()
