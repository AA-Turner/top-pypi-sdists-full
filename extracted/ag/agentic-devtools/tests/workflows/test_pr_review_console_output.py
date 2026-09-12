"""Regression tests for console output across PR-review setup calls."""

import io
import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.azure_devops import review_commands
from agentic_devtools.cli.git import operations
from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult
from agentic_devtools.cli.workflows import commands
from agentic_devtools.cli.workflows.preflight import PreflightResult


@pytest.mark.parametrize("encoding", ["cp1252", "utf-8"])
@pytest.mark.parametrize("setup_fails", [False, True])
def test_initiation_runs_real_auto_setup_output(temp_state_dir, encoding, setup_fails):
    """Console encoding must not turn a started task into a setup failure."""
    preflight = PreflightResult(False, False, "wrong", "main", "PROJECT-1234")
    with (
        patch.dict("os.environ"),
        io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stdout,
        io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stderr,
        patch("sys.stdout", stdout),
        patch("sys.stderr", stderr),
        patch.object(commands, "_ensure_bootstrap_identity_and_scope"),
        patch.object(commands, "check_worktree_and_branch", return_value=preflight),
        patch(
            "agentic_devtools.cli.azure_devops.helpers.get_pull_request_source_branch",
            return_value="feature/test",
        ),
        patch(
            "agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background",
            return_value="task-123",
            side_effect=RuntimeError("Connection failed 漢") if setup_fails else None,
        ) as start_task,
    ):
        argv = ["--pull-request-id", "123", "--issue-key", "PROJECT-1234", "--skip-copilot-session"]
        if setup_fails:
            with pytest.raises(SystemExit) as exc:
                commands.initiate_pull_request_review_workflow(_argv=argv)
            assert exc.value.code == 1
        else:
            commands.initiate_pull_request_review_workflow(_argv=argv)
            assert state.get_value("background.task_id") == "task-123"

        start_task.assert_called_once()
        stdout.flush()
        output = stdout.buffer.getvalue().decode(encoding)
        if setup_fails:
            marker = "[ERROR]" if encoding == "cp1252" else "❌"
            detail = "?" if encoding == "cp1252" else "漢"
            assert f"{marker} Failed to start background task: Connection failed {detail}" in output
        else:
            marker = "[OK]" if encoding == "cp1252" else "✅"
            assert f"{marker} Background task started: task-123" in output
            assert "NEXT STEPS" in output
            assert "Worktree setup started" in output


@pytest.mark.parametrize("encoding", ["cp1252", "utf-8"])
@pytest.mark.parametrize("checkout_fails", [False, True])
def test_review_setup_runs_real_branch_and_instruction_output(temp_state_dir, encoding, checkout_fails, monkeypatch):
    """Conflict warnings, paths and errors retain setup state and exit semantics."""
    monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(temp_state_dir))
    state.set_value("pull_request_id", "123")
    state.set_value("dry_run", True)
    artifact_dir = temp_state_dir / "artifacts-漢"
    artifact_dir.mkdir()
    details = {
        "pullRequest": {
            "sourceRefName": "refs/heads/feature/漢",
            "targetRefName": "refs/heads/main",
            "title": "Review 漢",
        },
        "files": [{"path": "/merged-漢.py"}],
    }
    (artifact_dir / "temp-get-pull-request-details-response.json").write_text(json.dumps(details), encoding="utf-8")
    checkout = CheckoutResult(
        CheckoutResult.UNCOMMITTED_CHANGES if checkout_fails else CheckoutResult.SUCCESS,
        "Local changes 漢",
    )

    with (
        io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stdout,
        io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stderr,
        patch("sys.stdout", stdout),
        patch("sys.stderr", stderr),
        patch.object(review_commands, "get_state_dir", return_value=artifact_dir),
        patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details"),
        patch("agentic_devtools.cli.git.operations.checkout_branch", return_value=checkout),
        patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True),
        patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True),
        patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True),
        patch(
            "agentic_devtools.cli.git.operations.rebase_onto_main",
            return_value=RebaseResult(RebaseResult.CONFLICT, "Conflicts 漢"),
        ),
        patch(
            "agentic_devtools.cli.git.operations.get_branch_change_inventory",
            return_value=([], {}, {}, None, True),
        ),
        patch(
            "agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts",
            side_effect=RuntimeError("Artifact failed 漢"),
        ),
        patch.object(review_commands, "run_safe", return_value=Mock(returncode=0, stdout=str(temp_state_dir))),
        patch("agentic_devtools.config.load_review_focus_areas", return_value=None),
        patch("agentic_devtools.prompts.loader.load_and_render_prompt") as render_prompt,
    ):
        if checkout_fails:
            with pytest.raises(SystemExit) as exc:
                review_commands.setup_pull_request_review()
            assert exc.value.code == 1
            render_prompt.assert_not_called()
        else:
            review_commands.setup_pull_request_review()
            assert state.get_value("review.rebase_conflicts_detected") == "true"
            assert state.get_workflow_state()["active"] == "pull-request-review"
            render_prompt.assert_called_once()

        stdout.flush()
        stderr.flush()
        output = stdout.buffer.getvalue().decode(encoding)
        errors = stderr.buffer.getvalue().decode(encoding)
        detail = "?" if encoding == "cp1252" else "漢"
        assert f"feature/{detail}" in output
        if checkout_fails:
            assert "BRANCH CHECKOUT/SYNC ISSUE" in errors
            assert f"Local changes {detail}" in errors
            assert "Please resolve this issue and re-run the workflow." in errors
        else:
            marker = "[WARN]" if encoding == "cp1252" else "⚠️"
            assert f"{marker}  REBASE CONFLICTS DETECTED" in output
            assert f"artifacts-{detail}" in output
            assert f"Skipping file not on branch (likely from merged PR): /merged-{detail}.py" in output
            assert "WARNING: No prompts were generated." in output
            assert f"Artifact failed {detail}" in errors
            assert "WORKFLOW INITIALIZED" in output


@pytest.mark.parametrize("encoding", ["cp1252", "utf-8"])
@pytest.mark.parametrize("fetch_fails", [False, True])
def test_review_sync_runs_real_git_status_output(encoding, fetch_fails):
    """Nested Git status/error output preserves Unicode arguments and sync results."""
    branch = "feature/漢"

    def run_git(*args, **kwargs):
        if args == ("rev-parse", "--abbrev-ref", "HEAD"):
            return Mock(returncode=0, stdout=branch, stderr="")
        if fetch_fails and args == ("fetch", "origin", branch):
            return Mock(returncode=1, stdout="", stderr="Fetch failed 漢")
        return Mock(returncode=0, stdout="0", stderr="")

    with (
        io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stdout,
        patch("sys.stdout", stdout),
        patch.object(operations, "run_git", side_effect=run_git) as git,
        patch.object(operations, "has_local_changes", return_value=False),
        patch("agentic_devtools.cli.git.core.get_current_branch", return_value="main"),
        patch.object(operations, "get_files_changed_on_branch", return_value=["changed.py"]),
    ):
        success, error, files, conflicts, pushed = review_commands.checkout_and_sync_branch(branch)
        stdout.flush()
        output = stdout.buffer.getvalue().decode(encoding)

    git.assert_any_call("checkout", branch, check=False)
    git.assert_any_call("fetch", "origin", branch, check=False)
    assert success is not fetch_fails
    assert conflicts is False
    assert pushed is None
    detail = "?" if encoding == "cp1252" else "漢"
    assert f"feature/{detail}" in output
    if fetch_fails:
        assert branch in error
        assert files == set()
        assert f"Fetch failed {detail}" in output
    else:
        assert error is None
        assert files == {"changed.py"}
