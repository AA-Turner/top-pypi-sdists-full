"""Tests for orchestrate_finalize_cmd."""

from shutil import copytree as real_copytree
from shutil import rmtree as real_rmtree
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.orchestrator_commands import (
    _APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY,
    _compute_payload_digest,
    orchestrate_finalize_cmd,
)
from agentic_devtools.epic_tree import EpicTreeLoadError


def _make_run_result(returncode: int = 0, stdout: str = "", stderr: str = "") -> MagicMock:
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


_CLEAN_STATUS = _make_run_result(returncode=0, stdout="")
_GIT_SUCCESS = _make_run_result(returncode=0)
_DIRTY_STATUS = _make_run_result(returncode=0, stdout=" M somefile.py\n")
_NO_BRANCH = _make_run_result(returncode=0, stdout="")  # git branch --list → branch not found


def _prepare_scratch_dir(path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "epic-tree.json").write_text(
        '{"schemaVersion":"1.0","epic":{"ref":"epic-1","title":"Generated Epic","body":"","features":[]}}',
        encoding="utf-8",
    )


def _make_workflow_state(step: str, scratch_dir, status: str = "running") -> dict[str, object]:
    return {
        "step": step,
        "active": "orchestrate-feature",
        "status": status,
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: _compute_payload_digest(scratch_dir)},
    }


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_happy_path(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_value,
    mock_delete_pin_file,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        **_make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch),
        "started_at": "2026-08-21T00:00:00+00:00",
    }
    mock_copytree.side_effect = real_copytree
    # git status → clean; branch --list → no branch; worktree add → success; git -C add → success;
    # git -C commit → success; push → success; code → success
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _make_run_result(returncode=0),
    ]

    assert orchestrate_finalize_cmd() == 0
    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    mock_set_value.assert_called_once()
    assert mock_set_value.call_args[0][0] == "workflow"
    assert mock_set_value.call_args[0][1] == {
        "active": "",
        "status": "completed",
        "step": "completed",
        "context": mock_get.return_value["context"],
        "started_at": "2026-08-21T00:00:00+00:00",
    }
    mock_delete_pin_file.assert_called_once_with()
    assert mock_run_safe.call_count == 7
    assert mock_copytree.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_finalize_cmd_no_issue_key(
    mock_get_repo_root, mock_run_safe, mock_set, mock_get, mock_get_bootstrap_state, mock_get_value, tmp_path
):
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature", "context": {}}
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = None
    mock_get_bootstrap_state.return_value = {}

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
def test_orchestrate_finalize_cmd_wrong_step(mock_run_safe, mock_set, mock_get, mock_get_value):
    mock_get.return_value = {"step": "decomposition"}

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
def test_orchestrate_finalize_cmd_malformed_workflow_aborts(mock_run_safe, mock_set, mock_get, mock_get_value):
    mock_get.return_value = ["not", "a", "mapping"]

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
def test_orchestrate_finalize_cmd_malformed_context_aborts(mock_run_safe, mock_set, mock_get, mock_get_value):
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "context": [],
    }

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_finalize_cmd_dirty_tree(
    mock_get_repo_root, mock_run_safe, mock_set, mock_get, mock_get_value, tmp_path
):
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature", "context": {}}
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    mock_run_safe.return_value = _DIRTY_STATUS

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_worktree_failure(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _make_run_result(returncode=1, stderr="branch already exists"),
    ]

    assert orchestrate_finalize_cmd() == 1

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_source_digest_mismatch_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    approved_digest = _compute_payload_digest(scratch)
    (scratch / "epic-tree.json").write_text(
        '{"schemaVersion":"1.0","epic":{"ref":"epic-1","title":"Changed","body":"","features":[]}}',
        encoding="utf-8",
    )
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: approved_digest},
    }
    mock_run_safe.return_value = _CLEAN_STATUS

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands._compute_payload_digest")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_hash_failure_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    mock_digest,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "approved-digest"},
    }
    mock_digest.side_effect = ValueError("boom")
    mock_run_safe.return_value = _CLEAN_STATUS

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_push_failure(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _make_run_result(returncode=1, stderr="non-fast-forward"),
    ]

    assert orchestrate_finalize_cmd() == 1

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    mock_copytree.assert_called_once()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_retry_from_finalizing(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_value,
    mock_delete_pin_file,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """Retrying from finalizing state should complete without re-transitioning to finalizing."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)
    mock_copytree.side_effect = real_copytree
    mock_copytree.side_effect = real_copytree
    mock_copytree.side_effect = real_copytree
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        MagicMock(),
    ]

    assert orchestrate_finalize_cmd() == 0

    mock_set.assert_not_called()
    assert mock_set_value.call_args[0][1]["step"] == "completed"
    mock_delete_pin_file.assert_called_once_with()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_finalize_cmd_invalid_issue_key(
    mock_get_repo_root, mock_run_safe, mock_set, mock_get, mock_get_value, tmp_path
):
    """An issue_key that fails normalize_issue_key should abort without side effects."""
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature", "context": {}}
    mock_get_repo_root.return_value = tmp_path
    mock_get_value.return_value = "../../path-traversal"

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_finalize_cmd_git_status_failure(
    mock_get_repo_root, mock_run_safe, mock_set, mock_get, mock_get_value, tmp_path
):
    """A non-zero git status exit code should abort before any state mutation."""
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature", "context": {}}
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    mock_run_safe.return_value = _make_run_result(returncode=128, stdout="", stderr="not a git repo")

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_orchestrate_finalize_cmd_missing_approval_digest_aborts(
    mock_get_repo_root, mock_run_safe, mock_set, mock_get, mock_get_value, tmp_path
):
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "orchestrate-feature", "context": {}}
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    mock_run_safe.return_value = _CLEAN_STATUS

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_idempotent_worktree_reuse(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_value,
    mock_delete_pin_file,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """When the worktree directory already exists, worktree add is skipped and push still succeeds."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)
    mock_copytree.side_effect = real_copytree

    # Create the worktree path so worktree_path.exists() returns True.
    # With repo_root = tmp_path / "repo", worktree_path = tmp_path / "42-default-feature".
    slug = "default-feature"
    worktree_path = tmp_path / f"42-{slug}"
    worktree_path.mkdir(parents=True, exist_ok=True)

    # Only: status, branch check, worktree status, add, commit, push, code  (worktree add is skipped)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        MagicMock(),
    ]

    assert orchestrate_finalize_cmd() == 0

    mock_set.assert_not_called()
    assert mock_set_value.call_args[0][1]["step"] == "completed"
    mock_delete_pin_file.assert_called_once_with()
    # Verify worktree add was NOT called
    worktree_add_calls = [c for c in mock_run_safe.call_args_list if "worktree" in str(c)]
    assert not worktree_add_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_git_status_failure_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """A non-zero git status exit code inside the reused worktree should abort finalization."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(returncode=128, stderr="not a git repo"),  # wt_status fails
    ]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_unexpected_changes_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """Staged changes outside the expected retry path should abort finalization."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(returncode=0, stdout="\nM  unrelated_file.py\n"),  # wt_status: dirty
    ]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_rename_outside_payload_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A staged rename must be rejected when either source or destination escapes the retry payload."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(
            returncode=0,
            stdout="R  .agdt/scratch/default-feature/a -> secrets.txt\n",
        ),
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "outside the expected retry payload path" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_second_column_rename_outside_payload_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """An unstaged rename (second XY column) must be rejected when destination escapes the payload."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(
            returncode=0,
            # Second column rename: space in X, R in Y
            stdout=" R .agdt/scratch/default-feature/a -> secrets.txt\n",
        ),
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "outside the expected retry payload path" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_malformed_rename_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A rename/copy status entry without both parsed paths must fail closed."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(returncode=0, stdout="R  .agdt/scratch/default-feature/a\n"),
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "outside the expected retry payload path" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_reuse_worktree_short_status_line_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A malformed short porcelain line must fail closed instead of being indexed blindly."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(returncode=0, stdout="M\n"),
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "outside the expected retry payload path" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_git_add_failure(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """A non-zero git add exit code should abort before pushing."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # git status
        _NO_BRANCH,  # git branch --list (branch not found)
        _GIT_SUCCESS,  # git worktree add
        _make_run_result(returncode=128, stderr="not a git repository"),  # git -C add (fail)
    ]

    assert orchestrate_finalize_cmd() == 1

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    assert mock_run_safe.call_count == 4


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_git_commit_nothing_to_commit(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_value,
    mock_delete_pin_file,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """A non-zero git commit exit (e.g. 'nothing to commit') is non-fatal: push still proceeds."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # git status
        _NO_BRANCH,  # git branch --list (branch not found)
        _GIT_SUCCESS,  # git worktree add
        _GIT_SUCCESS,  # git -C add (success)
        _make_run_result(returncode=1, stderr="nothing to commit, working tree clean"),  # git commit (non-fatal)
        _make_run_result(returncode=0),  # git diff --cached --quiet
        _make_run_result(returncode=0, stdout=""),  # git status --porcelain
        _GIT_SUCCESS,  # git push
        MagicMock(),  # code
    ]

    assert orchestrate_finalize_cmd() == 0

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    assert mock_set_value.call_args[0][1]["step"] == "completed"
    mock_delete_pin_file.assert_called_once_with()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=False)
def test_orchestrate_finalize_cmd_invalid_worktree_reuse_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """If the worktree path exists but is not a valid repo worktree, finalization aborts."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)
    mock_run_safe.return_value = _CLEAN_STATUS

    slug = "default-feature"
    worktree_path = tmp_path / f"42-{slug}"
    worktree_path.mkdir(parents=True, exist_ok=True)

    assert orchestrate_finalize_cmd() == 1

    # Must not advance to completed
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    out = capsys.readouterr().out
    assert "Error" in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_existing_worktree_wrong_branch_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)
    mock_run_safe.side_effect = [_CLEAN_STATUS, _make_run_result(returncode=0, stdout="main\n")]

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    assert mock_run_safe.call_count == 2


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_scratch_payload(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    (repo_root / "outside.txt").write_text("outside", encoding="utf-8")
    (scratch / "linked.txt").symlink_to(repo_root / "outside.txt")
    mock_scratch_dir.return_value = scratch
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    mock_copytree.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands._compute_payload_digest")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_copied_digest_mismatch_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    mock_digest,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "approved-digest"},
    }
    mock_copytree.side_effect = real_copytree
    mock_digest.side_effect = ["approved-digest", "different-digest"]
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    assert mock_run_safe.call_count == 3


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands._compute_payload_digest")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_copied_digest_hash_failure_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    mock_digest,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "approved-digest"},
    }
    mock_copytree.side_effect = real_copytree

    def digest_side_effect(path):
        if path == scratch:
            return "approved-digest"
        raise ValueError("boom")

    mock_digest.side_effect = digest_side_effect
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    assert mock_set.call_count == 1
    assert mock_set.call_args[1]["step"] == "finalizing"
    assert mock_run_safe.call_count == 3


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_source_agdt_dir(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """A symlinked .agdt ancestor on the source side aborts finalization before copying."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    outside = tmp_path / "outside"
    outside.mkdir()
    source_store = tmp_path / "source-store"
    scratch = source_store / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    # .agdt on the source side is a symlink to an external directory
    (repo_root / ".agdt").symlink_to(outside, target_is_directory=True)
    scratch = repo_root / ".agdt" / "scratch" / "default-feature"
    mock_scratch_dir.return_value = scratch
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    mock_copytree.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_source_agdt_scratch_dir(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    """A symlinked .agdt/scratch ancestor on the source side aborts finalization before copying."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    agdt_dir = repo_root / ".agdt"
    agdt_dir.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    source_store = tmp_path / "source-store"
    scratch = source_store / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    # .agdt/scratch on the source side is a symlink to an external directory
    (agdt_dir / "scratch").symlink_to(outside, target_is_directory=True)
    scratch = agdt_dir / "scratch" / "default-feature"
    mock_scratch_dir.return_value = scratch
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    mock_copytree.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_source_scratch_dir(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    real_scratch = tmp_path / "real-scratch"
    _prepare_scratch_dir(real_scratch)
    symlink_scratch = tmp_path / "linked-scratch"
    symlink_scratch.symlink_to(real_scratch, target_is_directory=True)
    mock_scratch_dir.return_value = symlink_scratch
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "approved-digest"},
    }
    mock_run_safe.return_value = _CLEAN_STATUS

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_epic_tree_before_loading(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    mock_load_epic_tree,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    outside = repo_root / "outside-epic-tree.json"
    outside.write_text("{}", encoding="utf-8")
    (scratch / "epic-tree.json").unlink()
    (scratch / "epic-tree.json").symlink_to(outside)
    mock_scratch_dir.return_value = scratch
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    mock_load_epic_tree.assert_not_called()
    mock_copytree.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_missing_required_scratch_artifacts_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "precomputed-digest"},
    }
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    scratch.mkdir(parents=True, exist_ok=True)
    mock_scratch_dir.return_value = scratch
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
def test_orchestrate_finalize_cmd_existing_worktree_branch_query_failure_aborts(
    mock_valid_wt,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / "scratch"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)
    mock_run_safe.side_effect = [_CLEAN_STATUS, _make_run_result(returncode=1, stderr="git error")]

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    assert mock_run_safe.call_count == 2


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_missing_scratch_dir_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    mock_get.return_value = {
        "step": "AWAITING_HUMAN_APPROVAL",
        "active": "orchestrate-feature",
        "status": "running",
        "context": {_APPROVED_PAYLOAD_DIGEST_CONTEXT_KEY: "precomputed-digest"},
    }
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    mock_scratch_dir.return_value = tmp_path / "does-not-exist"
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    assert mock_run_safe.call_count == 1


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_commit_failure_with_staged_changes_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # git status
        _NO_BRANCH,  # git branch --list (branch not found)
        _GIT_SUCCESS,  # git worktree add
        _GIT_SUCCESS,  # git add
        _make_run_result(returncode=1, stderr="hook failed"),  # git commit
        _make_run_result(returncode=1),  # git diff --cached --quiet => staged changes remain
        _make_run_result(returncode=0, stdout=""),  # git status --porcelain
    ]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
    mock_copytree.assert_called_once()
    assert mock_run_safe.call_count == 7


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.propagate_agdt_cache")
def test_orchestrate_finalize_cmd_propagates_agdt_cache(
    mock_propagate,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        MagicMock(),
    ]

    assert orchestrate_finalize_cmd() == 0

    expected_worktree_path = str(repo_root.parent / "42-default-feature")
    mock_propagate.assert_called_once_with(expected_worktree_path, worktree_key="42")


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.rmtree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_replaces_existing_target_scratch_exactly(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_rmtree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_rmtree.side_effect = real_rmtree
    mock_copytree.side_effect = real_copytree
    (tmp_path / "42-default-feature" / ".agdt" / "scratch" / "default-feature").mkdir(parents=True, exist_ok=True)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _make_run_result(returncode=0),
    ]

    assert orchestrate_finalize_cmd() == 0

    mock_rmtree.assert_called_once()
    copied_source, copied_target = mock_copytree.call_args.args[:2]
    assert copied_source == scratch
    assert copied_target == tmp_path / "42-default-feature" / ".agdt" / "scratch" / "default-feature"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_source_target_scratch_collision(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
):
    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)
    mock_get_repo_root.return_value = worktree_path
    mock_get_value.return_value = "42"

    scratch = worktree_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    mock_copytree.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_non_directory_target_scratch(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    target_scratch = worktree_path / ".agdt" / "scratch" / "default-feature"
    target_scratch.parent.mkdir(parents=True, exist_ok=True)
    worktree_path.mkdir(parents=True, exist_ok=True)
    target_scratch.write_text("stale", encoding="utf-8")
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    mock_copytree.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.rmtree", side_effect=OSError("cannot remove"))
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rmtree_failure_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_rmtree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    target_scratch = tmp_path / "42-default-feature" / ".agdt" / "scratch" / "default-feature"
    target_scratch.mkdir(parents=True, exist_ok=True)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    mock_copytree.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.delete_pin_file")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_vscode_launch_failure_is_best_effort(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set_value,
    mock_delete_pin_file,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _make_run_result(returncode=127, stderr="code: command not found"),
    ]

    assert orchestrate_finalize_cmd() == 0

    assert mock_set.call_args_list[-1][1]["step"] == "finalizing"
    assert mock_set_value.call_args[0][1]["step"] == "completed"
    mock_delete_pin_file.assert_called_once_with()
    out = capsys.readouterr().out
    assert "best-effort" in out
    assert "No further agdt-orchestrate-step call is required." in out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch(
    "agentic_devtools.cli.workflows.orchestrator_commands.run_safe",
    side_effect=[
        _CLEAN_STATUS,
        _NO_BRANCH,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        _GIT_SUCCESS,
        OSError("missing code"),
    ],
)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_vscode_launch_oserror_is_best_effort(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree

    assert orchestrate_finalize_cmd() == 0

    assert "missing code" in capsys.readouterr().out


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlink_target_scratch(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    target_scratch = worktree_path / ".agdt" / "scratch" / "default-feature"
    target_scratch.parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "outside").mkdir()
    target_scratch.symlink_to(tmp_path / "outside", target_is_directory=True)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
def test_orchestrate_finalize_cmd_wrong_active_workflow_aborts(mock_run_safe, mock_set, mock_get, mock_get_value):
    mock_get.return_value = {"step": "AWAITING_HUMAN_APPROVAL", "active": "different-workflow", "context": {}}

    assert orchestrate_finalize_cmd() == 1

    mock_set.assert_not_called()
    mock_run_safe.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_existing_branch_without_matching_worktree(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A branch collision without a reusable worktree fails closed."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    branch_exists = _make_run_result(returncode=0, stdout="  feature/42/default-feature\n")
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # git status
        branch_exists,  # git branch --list (branch found)
    ]

    assert orchestrate_finalize_cmd() == 1

    captured = capsys.readouterr()
    assert "target branch already exists without a matching worktree path" in captured.out
    assert mock_run_safe.call_count == 2
    mock_copytree.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_branch_lookup_failure_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=1, stderr="lookup failed"),
    ]

    assert orchestrate_finalize_cmd() == 1

    captured = capsys.readouterr()
    assert "git branch lookup failed" in captured.out
    assert mock_run_safe.call_count == 2
    mock_copytree.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_creates_new_branch_from_origin_main(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_copytree.side_effect = real_copytree
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # git status
        _NO_BRANCH,  # git branch --list (branch not found)
        _GIT_SUCCESS,  # git worktree add -b <branch> <path> origin/main
        _GIT_SUCCESS,  # git -C add
        _GIT_SUCCESS,  # git -C commit
        _GIT_SUCCESS,  # git push
        _make_run_result(returncode=0),  # code
    ]

    assert orchestrate_finalize_cmd() == 0

    worktree_add_calls = [c for c in mock_run_safe.call_args_list if "worktree" in str(c)]
    assert len(worktree_add_calls) == 1
    wt_args = worktree_add_calls[0][0][0]
    assert "-b" in wt_args
    assert wt_args[-1] == "origin/main"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree")
def test_orchestrate_finalize_cmd_invalid_epic_tree_aborts(
    mock_load_epic_tree,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """An invalid epic-tree.json aborts finalization before any copy or push."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_load_epic_tree.side_effect = EpicTreeLoadError([])
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "schema validation" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.propagate_agdt_cache")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_agdt_dir(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_wt,
    mock_get_value,
    mock_propagate,
    tmp_path,
    capsys,
):
    """A symlinked .agdt directory inside the worktree aborts finalization."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (worktree_path / ".agdt").symlink_to(outside, target_is_directory=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "symlink" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.propagate_agdt_cache")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_agdt_scratch_dir(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_wt,
    mock_get_value,
    mock_propagate,
    tmp_path,
    capsys,
):
    """A symlinked .agdt/scratch directory inside the worktree aborts finalization."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    agdt_dir = worktree_path / ".agdt"
    agdt_dir.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (agdt_dir / "scratch").symlink_to(outside, target_is_directory=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "symlink" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree")
def test_orchestrate_finalize_cmd_load_epic_tree_generic_error_aborts(
    mock_load_epic_tree,
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A non-schema exception from load_epic_tree (e.g. JSONDecodeError) aborts finalization."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)
    mock_load_epic_tree.side_effect = ValueError("unexpected JSON structure")
    mock_run_safe.side_effect = [_CLEAN_STATUS, _NO_BRANCH, _GIT_SUCCESS]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "could not be loaded" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.load_epic_tree", new=MagicMock())
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_target_scratch_inside_worktree(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_worktree,
    mock_get_value,
    tmp_path,
    capsys,
):
    """target_scratch symlink pointing inside the worktree is rejected by the is_symlink() guard."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    target_scratch = worktree_path / ".agdt" / "scratch" / "default-feature"
    # Point target_scratch at a real dir inside the worktree so resolve() stays inside,
    # but is_symlink() must still reject the symlink.
    inside_dir = worktree_path / "safe-inside"
    inside_dir.mkdir(parents=True, exist_ok=True)
    target_scratch.parent.mkdir(parents=True, exist_ok=True)
    target_scratch.symlink_to(inside_dir, target_is_directory=True)
    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes in reused worktree
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "symlink" in out
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_reuse_path_boundary_rejects_prefixed_sibling(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_wt,
    mock_get_value,
    tmp_path,
    capsys,
):
    """A path sharing the expected prefix but not separated by '/' must be treated as unexpected.

    E.g. '.agdt/scratch/default-feature-private/secrets.txt' is NOT part of the
    'default-feature' retry payload and must abort finalization.
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    worktree_path.mkdir(parents=True, exist_ok=True)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),  # branch check
        _make_run_result(
            returncode=0, stdout="M  .agdt/scratch/default-feature-private/secrets.txt\n"
        ),  # wt_status: sibling path — must be unexpected
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "unexpected" in out.lower() or "outside" in out.lower()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.propagate_agdt_cache")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.git.worktree._is_valid_worktree_dir", return_value=True)
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_rejects_symlinked_identity_json(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_valid_wt,
    mock_get_value,
    mock_propagate,
    tmp_path,
    capsys,
):
    """A symlinked identity.json inside the worktree aborts finalization before propagating cache."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("finalizing", scratch)

    worktree_path = tmp_path / "42-default-feature"
    agdt_dir = worktree_path / ".agdt"
    agdt_dir.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (agdt_dir / "identity.json").symlink_to(outside / "identity.json")

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,
        _make_run_result(returncode=0, stdout="feature/42/default-feature\n"),
        _CLEAN_STATUS,  # wt_status: no unexpected changes
    ]

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "symlink" in out
    mock_propagate.assert_not_called()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls


@patch("agentic_devtools.cli.workflows.orchestrator_commands.propagate_agdt_cache")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.set_workflow_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_safe")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.shutil.copytree")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_scratch_dir")
def test_orchestrate_finalize_cmd_propagate_failure_aborts(
    mock_scratch_dir,
    mock_get_repo_root,
    mock_copytree,
    mock_run_safe,
    mock_set,
    mock_get,
    mock_get_value,
    mock_propagate,
    tmp_path,
    capsys,
):
    """An OSError from propagate_agdt_cache must abort finalization before publishing."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    mock_get_repo_root.return_value = repo_root
    mock_get_value.return_value = "42"
    scratch = tmp_path / ".agdt" / "scratch" / "default-feature"
    _prepare_scratch_dir(scratch)
    mock_scratch_dir.return_value = scratch
    mock_get.return_value = _make_workflow_state("AWAITING_HUMAN_APPROVAL", scratch)

    mock_run_safe.side_effect = [
        _CLEAN_STATUS,  # source git status (clean)
        _NO_BRANCH,  # git branch --list → branch not found
        _GIT_SUCCESS,  # git worktree add
    ]
    mock_propagate.side_effect = OSError("disk full")

    assert orchestrate_finalize_cmd() == 1

    out = capsys.readouterr().out
    assert "failed to propagate" in out.lower() or "agdt cache" in out.lower()
    completed_calls = [c for c in mock_set.call_args_list if c[1].get("step") == "completed"]
    assert not completed_calls
