"""Tests for orchestrate_step_cmd."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import (
    _APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY,
    _compute_payload_digest,
    orchestrate_step_cmd,
)


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd(mock_set, mock_scratch_dir, mock_get, tmp_path):
    mock_get.return_value = {"step": "decomposition", "active": "orchestrate-feature"}
    assert orchestrate_step_cmd() == 0
    assert mock_set.call_args[1]["step"] == "doer_execution"

    mock_get.return_value = {"step": "doer_execution", "active": "orchestrate-feature"}
    assert orchestrate_step_cmd() == 0
    assert mock_set.call_args[1]["step"] == "duck_reviews"

    mock_get.return_value = {"step": "duck_reviews", "active": "orchestrate-feature"}
    assert orchestrate_step_cmd() == 0
    assert mock_set.call_args[1]["step"] == "adjudicator_decision"

    mock_get.return_value = {"step": "adjudicator_decision", "active": "orchestrate-feature"}
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    scratch.mkdir(parents=True)
    (scratch / "epic-tree.json").write_text("{}", encoding="utf-8")
    mock_scratch_dir.return_value = scratch
    assert orchestrate_step_cmd() == 0
    assert mock_set.call_args[1]["step"] == "AWAITING_HUMAN_APPROVAL"
    assert mock_set.call_args[1]["context"][_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY] == _compute_payload_digest(scratch)


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_refreshes_digest_while_awaiting_human_approval(
    mock_set, mock_scratch_dir, mock_get, tmp_path
):
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    scratch.mkdir(parents=True)
    payload_file = scratch / "epic-tree.json"
    payload_file.write_text("first", encoding="utf-8")
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {},
    }

    assert orchestrate_step_cmd() == 0
    first_context = mock_set.call_args[1]["context"]
    first_digest = first_context[_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY]
    assert mock_set.call_args[1]["step"] == "AWAITING_HUMAN_APPROVAL"

    payload_file.write_text("second", encoding="utf-8")
    assert orchestrate_step_cmd() == 0
    second_context = mock_set.call_args[1]["context"]
    second_digest = second_context[_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY]

    assert mock_set.call_args[1]["step"] == "AWAITING_HUMAN_APPROVAL"
    assert first_digest != second_digest


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_invalid_step_aborts(mock_set, mock_get, capsys):
    """An invalid step must abort without calling set_workflow_state."""
    mock_get.return_value = {"step": "unknown", "active": "orchestrate-feature"}
    assert orchestrate_step_cmd() == 1
    mock_set.assert_not_called()
    out = capsys.readouterr().out
    assert "Error" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_wrong_workflow_aborts(mock_set, mock_get, capsys):
    """A non-orchestrate-feature active workflow must abort without calling set_workflow_state."""
    mock_get.return_value = {"step": "decomposition", "active": "other-workflow"}
    assert orchestrate_step_cmd() == 1
    mock_set.assert_not_called()
    out = capsys.readouterr().out
    assert "Error" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_no_active_workflow_aborts(mock_set, mock_get, capsys):
    """Empty/no workflow state must abort without calling set_workflow_state."""
    mock_get.return_value = {}
    assert orchestrate_step_cmd() == 1
    mock_set.assert_not_called()
    out = capsys.readouterr().out
    assert "Error" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_malformed_workflow_aborts(mock_set, mock_get, capsys):
    mock_get.return_value = ["not", "a", "mapping"]

    assert orchestrate_step_cmd() == 1

    mock_set.assert_not_called()
    assert "malformed" in capsys.readouterr().out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_malformed_context_aborts(mock_set, mock_get, capsys):
    mock_get.return_value = {"step": "decomposition", "active": "orchestrate-feature", "context": []}

    assert orchestrate_step_cmd() == 1

    mock_set.assert_not_called()
    assert "malformed" in capsys.readouterr().out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_step_cmd_digest_failure_aborts(mock_set, mock_scratch_dir, mock_get, tmp_path, capsys):
    mock_get.return_value = {"step": "adjudicator_decision", "active": "orchestrate-feature"}
    mock_scratch_dir.return_value = tmp_path / "missing"

    assert orchestrate_step_cmd() == 1

    mock_set.assert_not_called()
    assert "unable to record approval payload digest" in capsys.readouterr().out

    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature"}
    assert orchestrate_step_cmd() == 1
    mock_set.assert_not_called()
    assert "unable to record approval payload digest" in capsys.readouterr().out
