"""Tests for orchestrate_init_cmd."""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.cli.workflows.orchestrator_commands import orchestrate_init_cmd


@pytest.fixture(autouse=True)
def mock_pin_file_functions(monkeypatch):
    """Isolate every test from real pin-file / state-dir I/O and env-var leaks.

    The pin functions write files and mutate os.environ["AGENTIC_DEVTOOLS_STATE_DIR"].
    Without isolation, a successful init test would set the env var and cause all
    subsequent tests to skip the pin-write path, leaving lines 281-282 uncovered.
    """
    fake_state_dir = Path("/tmp/fake-state-dir")
    mock_delete = MagicMock(return_value=None)
    mock_get_state = MagicMock(return_value=fake_state_dir)
    mock_write = MagicMock(return_value=None)

    with (
        patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file", mock_delete),
        patch("agentic_devtools.cli.workflows.orchestrator_commands.get_state_dir", mock_get_state),
        patch("agentic_devtools.cli.workflows.orchestrator_commands.write_pin_file", mock_write),
    ):
        # Ensure AGENTIC_DEVTOOLS_STATE_DIR is unset for each test so that the
        # pin-writing branch is always entered (unless a test sets it explicitly).
        monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
        yield {"delete": mock_delete, "get_state": mock_get_state, "write": mock_write}
    # Any env-var written by orchestrate_init_cmd during the test is also cleaned up here
    # because monkeypatch restores the environment after each test.


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd(
    mock_get_repo_root, mock_set, mock_get, mock_get_value, mock_set_bootstrap, mock_set_value, tmp_path
):
    mock_get.return_value = {}
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 0

    mock_set.assert_called_once()
    assert mock_set.call_args[0][0] == "orchestrate-feature"
    assert mock_set.call_args[0][1] == "running"
    assert mock_set.call_args[1]["step"] == "decomposition"
    mock_set_bootstrap.assert_called()
    mock_set_value.assert_called_once_with("issue_key", "42")

    scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
    assert (scratch_dir / "epic-tree.json").exists()
    epic_tree = json.loads((scratch_dir / "epic-tree.json").read_text())
    assert "body" in epic_tree["epic"], "epic.body is required by the epic-tree schema"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_falls_back_to_cwd_when_repo_root_is_none(
    mock_get_repo_root, mock_set, mock_get, mock_get_value, mock_set_bootstrap, mock_set_value, tmp_path
):
    mock_get.return_value = {}
    mock_get_repo_root.return_value = None
    mock_get_value.return_value = "42"

    with patch("pathlib.Path.cwd", return_value=tmp_path):
        assert orchestrate_init_cmd() == 0

    mock_set.assert_called_once()
    assert mock_set.call_args[1]["step"] == "decomposition"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_handles_null_context(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap,
    mock_set_value,
    tmp_path,
):
    mock_get_workflow_state.return_value = {"context": None}
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 0

    mock_set_workflow_state.assert_called_once()
    assert mock_set_workflow_state.call_args[1]["context"]["trio_state"] == "primed"
    scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
    assert (scratch_dir / "epic-tree.json").exists()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_handles_non_mapping_workflow_state(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap,
    mock_set_value,
    tmp_path,
):
    mock_get_workflow_state.return_value = ["invalid-workflow-shape"]
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 0

    mock_set_workflow_state.assert_called_once()
    assert mock_set_workflow_state.call_args[1]["context"]["trio_state"] == "primed"
    scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
    assert (scratch_dir / "epic-tree.json").exists()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_uses_bootstrap_issue_key_when_state_is_unscoped(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_get_bootstrap_state,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
):
    mock_get_workflow_state.return_value = {}
    mock_get_value.return_value = None
    mock_get_bootstrap_state.return_value = {"worktree_key": "42"}
    mock_get_repo_root.return_value = tmp_path

    assert orchestrate_init_cmd() == 0

    mock_set_bootstrap_state.assert_called_once_with(worktree_key="42")
    mock_set_value.assert_called_once_with("issue_key", "42")
    mock_set_workflow_state.assert_called_once()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
def test_orchestrate_init_cmd_requires_issue_key(
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_get_bootstrap_state,
    mock_set_bootstrap_state,
    mock_set_value,
    capsys,
):
    mock_get_workflow_state.return_value = {}
    mock_get_value.return_value = None
    mock_get_bootstrap_state.return_value = {}

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_bootstrap_state.assert_not_called()
    mock_set_value.assert_not_called()
    assert "issue_key must be set and valid before initializing" in capsys.readouterr().out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_fails_if_workflow_already_active_past_decomposition(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap_state,
    mock_set_value,
    capsys,
):
    """Fail closed when the orchestrate-feature workflow has progressed past decomposition."""
    mock_get_workflow_state.return_value = {
        "active": "orchestrate-feature",
        "step": "doer_execution",
        "status": "running",
    }
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    out = capsys.readouterr().out
    assert "already active" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_fails_if_any_other_workflow_is_active(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap_state,
    mock_set_value,
    capsys,
):
    """Fail closed when another workflow is active to avoid overwriting the shared _workflow record."""
    mock_get_workflow_state.return_value = {
        "active": "work-on-jira-issue",
        "step": "implementation",
        "status": "running",
    }
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_bootstrap_state.assert_not_called()
    mock_set_value.assert_not_called()
    out = capsys.readouterr().out
    assert "already active" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_uses_slug_from_prior_scope_before_bootstrap_switch(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
):
    """The scratch dir is named from the workflow context slug captured before set_bootstrap_state
    changes the state scope; a later get_workflow_state() would read the new scope and lose a
    custom slug recorded under the prior scope (e.g. '#42' → '42').
    """
    mock_get_workflow_state.return_value = {
        "context": {"feature_slug": "my-custom-feature"},
    }
    # issue_key normalizes '#42' → '42', changing the state scope after set_bootstrap_state
    mock_get_value.return_value = "#42"
    mock_get_repo_root.return_value = tmp_path

    assert orchestrate_init_cmd() == 0

    # epic-tree.json must be in the slug directory captured from the prior-scope context,
    # not the post-scope-switch default ("default-feature").
    # sanitize_branch_description("my-custom-feature") → "custom-feature"
    expected_scratch = tmp_path / ".agdt" / "scratch" / "custom-feature"
    assert (expected_scratch / "epic-tree.json").exists()
    unexpected_scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    assert not unexpected_scratch.exists()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_fails_if_epic_tree_already_exists(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
    capsys,
):
    """Fail closed when epic-tree.json already exists to avoid overwriting reviewed artifacts."""
    mock_get_workflow_state.return_value = {}
    mock_get_value.return_value = "42"
    mock_get_repo_root.return_value = tmp_path

    scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    (scratch_dir / "epic-tree.json").write_text('{"existing": true}', encoding="utf-8")

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_bootstrap_state.assert_not_called()
    mock_set_value.assert_not_called()
    out = capsys.readouterr().out
    assert "already exists" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._read_workflow_state_for_scope")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_fails_if_destination_scope_has_active_workflow(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_read_workflow_state_for_scope,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
    capsys,
):
    """Fail closed when the destination (post-normalization) scope already has an active workflow.

    The pre-switch guard reads the '#42' scope which has no active workflow; after
    set_bootstrap_state() switches to the '42' scope a second guard must detect the
    active workflow already recorded there and abort before overwriting it.
    """
    mock_get_workflow_state.return_value = {}
    mock_read_workflow_state_for_scope.return_value = {
        "active": "some-other-workflow",
        "step": "step-x",
        "status": "running",
    }
    mock_get_value.return_value = "#42"
    mock_get_repo_root.return_value = tmp_path

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_bootstrap_state.assert_not_called()
    mock_set_value.assert_not_called()
    out = capsys.readouterr().out
    assert "already active" in out
    assert "some-other-workflow" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_rejects_symlinked_epic_tree_path(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap,
    mock_set_value,
    tmp_path,
    capsys,
):
    mock_get_workflow_state.return_value = {}
    mock_get_value.return_value = "42"
    mock_get_repo_root.return_value = tmp_path

    scratch_dir = tmp_path / ".agdt" / "scratch" / "default-feature"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (scratch_dir / "epic-tree.json").symlink_to(outside / "epic-tree.json")

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_bootstrap.assert_not_called()
    mock_set_value.assert_not_called()
    out = capsys.readouterr().out
    assert "destination path is a symlink" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._read_workflow_state_for_scope")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_restores_bootstrap_if_destination_scope_activates_after_switch(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_read_workflow_state_for_scope,
    mock_get_workflow_state,
    mock_get_value,
    mock_get_bootstrap_state,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
    capsys,
):
    mock_get_workflow_state.side_effect = [
        {},
        {"active": "some-other-workflow", "step": "step-x", "status": "running"},
    ]
    mock_read_workflow_state_for_scope.return_value = {}
    mock_get_value.return_value = "#42"
    mock_get_repo_root.return_value = tmp_path
    mock_get_bootstrap_state.return_value = {"worktree_key": "#42"}

    assert orchestrate_init_cmd() == 1

    mock_set_workflow_state.assert_not_called()
    mock_set_value.assert_not_called()
    assert mock_set_bootstrap_state.call_args_list == [
        call(worktree_key="42"),
        call(worktree_key="#42"),
    ]
    out = capsys.readouterr().out
    assert "already active" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_writes_pin_file_on_success(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_get_workflow_state,
    mock_get_value,
    mock_set_bootstrap,
    mock_set_value,
    tmp_path,
    mock_pin_file_functions,
):
    """Pin file is written with workflow='orchestrate-feature' after the scope switch."""
    mock_get_workflow_state.return_value = {}
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = "42"

    assert orchestrate_init_cmd() == 0

    mock_pin_file_functions["delete"].assert_called()
    mock_pin_file_functions["get_state"].assert_called()
    mock_pin_file_functions["write"].assert_called_once()
    assert mock_pin_file_functions["write"].call_args.kwargs["workflow"] == "orchestrate-feature"
    assert os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR") == str(mock_pin_file_functions["get_state"].return_value)


@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._read_workflow_state_for_scope")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_init_cmd_skips_pin_on_error_when_env_override_already_set(
    mock_get_repo_root,
    mock_set_workflow_state,
    mock_read_workflow_state_for_scope,
    mock_get_workflow_state,
    mock_get_value,
    mock_get_bootstrap_state,
    mock_set_bootstrap_state,
    mock_set_value,
    tmp_path,
    mock_pin_file_functions,
    monkeypatch,
    capsys,
):
    """When AGENTIC_DEVTOOLS_STATE_DIR is already set, the pin is never written and the
    cleanup inside the error path is skipped (_pin_was_written=False branch).
    """
    monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", "/external/state-dir")
    mock_get_workflow_state.side_effect = [
        {},
        {"active": "some-other-workflow", "step": "step-x", "status": "running"},
    ]
    mock_read_workflow_state_for_scope.return_value = {}
    mock_get_value.return_value = "#42"
    mock_get_repo_root.return_value = tmp_path
    mock_get_bootstrap_state.return_value = {"worktree_key": "#42"}

    assert orchestrate_init_cmd() == 1

    # Pin was NOT written because an env override was already present.
    mock_pin_file_functions["delete"].assert_not_called()
    mock_pin_file_functions["write"].assert_not_called()
    out = capsys.readouterr().out
    assert "already active" in out
