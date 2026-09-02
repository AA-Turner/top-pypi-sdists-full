"""Tests for the commit node (stage/rebase/amend/push — issue #1900)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.models.git_results import BlockedState, CommitResult, SetupResult
from agentic_devtools.orchestration.nodes.commit import commit_node

_MOD = "agentic_devtools.orchestration.nodes.commit"
_OPS_MOD = "agentic_devtools.cli.git.operations"

_DEFAULT_SETUP = SetupResult(worktree_path="/tmp/wt-42", branch_name="feature/42/x", mode="created")
"""Minimal SetupResult used across orchestration flow tests.

The commit node now requires a non-blank worktree_path; without it, a
context_mismatch BlockedState is returned before any git command runs.
"""


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


# --- issue key validation (preserved from the legacy node) ---------------------


class TestCommitNodeValidation:
    def test_fails_fast_when_issue_key_is_missing(self):
        result = commit_node({})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["commit_result"].error.category == "context_mismatch"
        assert result["events"][0]["event"] == "commit_failed"

    def test_fails_fast_when_issue_key_is_blank(self):
        result = commit_node({"issue_key": "   "})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["commit_result"].error.category == "context_mismatch"

    @pytest.mark.parametrize("bad", [None, 42, True, []])
    def test_fails_fast_when_issue_key_is_non_string(self, bad):
        result = commit_node({"issue_key": bad})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["commit_result"].error.category == "context_mismatch"

    def test_fails_fast_when_issue_key_normalizes_to_empty(self):
        result = commit_node({"issue_key": "#"})
        assert result["error"] == "issue_key must normalize to a non-empty issue identifier"
        assert result["commit_result"].error.category == "context_mismatch"

    def test_fails_fast_when_worktree_path_is_missing(self):
        """No setup_result → context_mismatch before any git command."""
        result = commit_node({"issue_key": "42"})
        assert result["commit_result"].error.category == "context_mismatch"
        assert "worktree_path" in result["error"]

    def test_fails_fast_when_worktree_path_is_blank(self):
        """Blank worktree_path is treated the same as missing."""
        setup = SetupResult(worktree_path="   ", branch_name=None, mode="created")
        result = commit_node({"issue_key": "42", "setup_result": setup})
        assert result["commit_result"].error.category == "context_mismatch"


# --- commit_node orchestration -------------------------------------------------


@pytest.fixture
def flow_patches():
    """Patch the commit node's internal helpers for orchestration tests."""

    def _branch_aware_capture(args, cwd=None):
        # Branch-check calls (rev-parse --abbrev-ref HEAD) must return the expected
        # branch so they don't trigger a context_mismatch before staging.
        if args[:2] == ["rev-parse", "--abbrev-ref"]:
            return _proc(stdout=_DEFAULT_SETUP.branch_name)
        # Ownership check (rev-parse --git-common-dir) must return the same path
        # for both the process CWD (cwd=None) and the worktree CWD so the check passes.
        if args == ["rev-parse", "--git-common-dir"]:
            return _proc(stdout="/tmp/main-repo/.git")
        return _proc(stdout="deadbeef")

    with (
        patch(f"{_MOD}.stage_changes") as stage,
        patch(f"{_MOD}._has_staged_changes", return_value=True) as has_staged,
        patch(f"{_MOD}._fetch_and_rebase", return_value=(True, None)) as rebase,
        patch(f"{_MOD}.should_amend_instead_of_commit", return_value=False) as ahead,
        patch(f"{_MOD}.run_git_safe", return_value=_proc()) as run_safe,
        patch(f"{_MOD}.run_git_capture", side_effect=_branch_aware_capture) as capture,
        patch(f"{_MOD}._push", return_value=None) as push,
    ):
        yield {
            "stage": stage,
            "has_staged": has_staged,
            "rebase": rebase,
            "ahead": ahead,
            "run_safe": run_safe,
            "capture": capture,
            "push": push,
            "setup": _DEFAULT_SETUP,
        }


class TestCommitNodeFlow:
    def test_dry_run_is_noop(self, flow_patches):
        result = commit_node({"issue_key": "42", "dry_run": True, "setup_result": flow_patches["setup"]})
        assert result["commit_result"].no_op is True
        assert result["error"] is None
        flow_patches["run_safe"].assert_not_called()

    def test_staging_failure_blocks(self, flow_patches):
        flow_patches["stage"].side_effect = GitError(1, "locked", ["add", "."])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "transient"
        assert "Staging failed" in result["error"]

    def test_wrong_branch_blocks_before_staging(self, flow_patches):
        """If the worktree has been checked out on a different branch, staging is refused."""

        def switched_branch(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="main")  # switched away from the expected branch
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = switched_branch
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "context_mismatch"
        assert "main" in result["error"]
        assert result["events"][0]["event"] == "commit_blocked_wrong_branch"
        # staging must not have been called
        flow_patches["stage"].assert_not_called()

    def test_branch_check_blocks_when_branch_name_not_set(self, flow_patches):
        """When setup_result.branch_name is None/blank, context_mismatch is returned."""
        setup_no_branch = SetupResult(worktree_path="/tmp/wt-42", branch_name=None, mode="created")
        result = commit_node({"issue_key": "42", "setup_result": setup_no_branch})
        assert result["commit_result"].error.category == "context_mismatch"
        assert "branch_name is not set" in result["error"]
        flow_patches["stage"].assert_not_called()

    def test_branch_probe_git_error_returns_transient_block(self, flow_patches):
        """GitError raised by the branch probe becomes a structured transient CommitResult."""

        def probe_fails(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                raise GitError(128, "not a git repo", args)
            # Ownership check (--git-common-dir) must succeed so the branch probe is reached.
            if args == ["rev-parse", "--git-common-dir"]:
                return _proc(stdout="/tmp/main/.git")
            return _proc()

        flow_patches["capture"].side_effect = probe_fails
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "Branch probe failed" in result["error"]
        assert result["commit_created"] is False
        assert result["events"][0]["event"] == "commit_blocked_worktree_disappeared"
        # staging must not have been called
        flow_patches["stage"].assert_not_called()

    def test_ownership_check_failure_blocks_before_staging(self, flow_patches):
        """A foreign-repo worktree directory blocks commit_node with context_mismatch."""

        def foreign_repo(args, cwd=None):
            if args == ["rev-parse", "--git-common-dir"]:
                # Process CWD returns one common-dir; worktree returns a different one.
                if cwd is None:
                    return _proc(stdout="/tmp/main/.git")
                return _proc(stdout="/tmp/other/.git")
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = foreign_repo
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "context_mismatch"
        assert "different repository" in result["error"]
        assert result["events"][0]["event"] == "commit_blocked_wrong_repo"
        flow_patches["stage"].assert_not_called()

    def test_ownership_check_proc_probe_failure_blocks(self, flow_patches):
        """Failure in the process-CWD common-dir probe blocks with context_mismatch."""

        def proc_probe_fails(args, cwd=None):
            if args == ["rev-parse", "--git-common-dir"] and cwd is None:
                return _proc(returncode=128)
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = proc_probe_fails
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "context_mismatch"
        assert "process CWD" in result["error"]
        assert result["events"][0]["event"] == "commit_blocked_wrong_repo"
        flow_patches["stage"].assert_not_called()

    def test_no_staged_changes_is_noop(self, flow_patches):
        flow_patches["has_staged"].return_value = False
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].no_op is True
        assert result["error"] is None
        assert result["commit_created"] is False

    def test_index_check_error_returns_blocked_transient(self, flow_patches):
        """A corrupt index (exit code > 1) produces a transient BlockedState."""
        flow_patches["has_staged"].side_effect = GitError(128, "corrupt index", ["diff", "--cached", "--quiet"])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "transient"
        assert "Index check failed" in result["error"]
        assert result["commit_created"] is False

    def test_no_staged_changes_retries_previous_failed_push(self, flow_patches):
        flow_patches["has_staged"].return_value = False
        prior_result = CommitResult(
            commit_sha="deadbeef",
            commit_message_title="feat(#42): add workflow",
            is_amend=True,
            push_succeeded=False,
            error=BlockedState(category="transient", message="push timed out"),
        )

        def unpublished_head(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="deadbeef")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout="")
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = unpublished_head
        result = commit_node(
            {
                "issue_key": "42",
                "setup_result": flow_patches["setup"],
                "commit_result": prior_result,
            }
        )
        assert result["error"] is None
        assert result["commit_result"].push_succeeded is True
        assert result["commit_result"].commit_sha == "deadbeef"
        assert result["commit_result"].is_amend is True
        assert result["commit_created"] is False
        flow_patches["push"].assert_called_once_with("/tmp/wt-42", is_amend=True)

    def test_no_staged_changes_retry_push_failure_returns_error(self, flow_patches):
        flow_patches["has_staged"].return_value = False
        flow_patches["push"].return_value = BlockedState(category="transient", message="push still failing")
        prior_result = CommitResult(
            commit_sha="deadbeef",
            commit_message_title="feat(#42): add workflow",
            is_amend=False,
            push_succeeded=False,
            error=BlockedState(category="transient", message="push timed out"),
        )

        def unpublished_head(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="deadbeef")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout="")
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = unpublished_head
        result = commit_node(
            {
                "issue_key": "42",
                "setup_result": flow_patches["setup"],
                "commit_result": prior_result,
            }
        )
        assert result["commit_result"].error.category == "transient"
        assert result["error"] == "push still failing"
        assert result["commit_created"] is False

    def test_rebase_block_propagates(self, flow_patches):
        flow_patches["rebase"].return_value = (True, BlockedState(category="conflict", message="conflict"))
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "conflict"

    def test_fetch_and_rebase_git_error_returns_transient_block(self, flow_patches):
        """GitError raised by _fetch_and_rebase becomes a structured transient CommitResult."""
        flow_patches["rebase"].side_effect = GitError(128, "worktree disappeared", ["fetch"])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "Fetch/rebase failed" in result["error"]
        assert result["commit_created"] is False
        assert result["events"][0]["event"] == "commit_failed"

    def test_amend_detection_git_error_returns_transient_block(self, flow_patches):
        """GitError raised by should_amend_instead_of_commit becomes a structured transient CommitResult."""
        flow_patches["ahead"].side_effect = GitError(128, "worktree gone", ["rev-parse"])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "Amend-detection probe failed" in result["error"]
        assert result["commit_created"] is False

    def test_sha_readback_git_error_returns_transient_block_with_commit_created(self, flow_patches):
        """GitError raised by the SHA read-back becomes a transient block with commit_created=True."""

        def sha_raises(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            if args == ["rev-parse", "--short", "HEAD"]:
                raise GitError(128, "worktree gone during sha read", args)
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = sha_raises
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "SHA read-back raised GitError" in result["commit_result"].error.message
        assert result["commit_created"] is True

    def test_push_git_error_returns_transient_block_with_commit_created(self, flow_patches):
        """GitError raised by _push becomes a transient block with commit_created=True."""
        flow_patches["push"].side_effect = GitError(128, "worktree gone during push", ["push"])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "Push failed" in result["error"]
        assert result["commit_created"] is True

    def test_new_commit_success(self, flow_patches):
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["error"] is None
        assert result["commit_result"].is_amend is False
        assert result["commit_result"].push_succeeded is True
        assert result["commit_result"].commit_sha == "deadbeef"
        # New commit path uses "commit -m", not "--amend"
        commit_call = flow_patches["run_safe"].call_args_list[0][0][0]
        assert commit_call[0] == "commit" and "--amend" not in commit_call

    def test_amend_commit_success(self, flow_patches):
        flow_patches["ahead"].return_value = True
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].is_amend is True
        commit_call = flow_patches["run_safe"].call_args_list[0][0][0]
        assert commit_call[:2] == ["commit", "--amend"]

    def test_commit_failure_blocks(self, flow_patches):
        flow_patches["run_safe"].side_effect = GitError(1, "nothing to commit", ["commit"])
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "transient"
        assert "Commit failed" in result["error"]

    def test_push_failure_blocks(self, flow_patches):
        flow_patches["push"].return_value = BlockedState(category="protection", message="protected")
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error.category == "protection"
        assert result["commit_result"].push_succeeded is False

    def test_commit_sha_read_back_failure_returns_blocked(self, flow_patches):
        """When rev-parse HEAD returns empty output after commit, a transient block is produced.

        The commit was created locally but we cannot confirm its identity; continuing
        with commit_sha=None violates FR-011 and leaves retry logic without a commit identity.
        """

        def _empty_sha(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            return _proc(returncode=0, stdout="   ")

        flow_patches["capture"].side_effect = _empty_sha
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"]})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert result["commit_created"] is True

    def test_cwd_propagated_from_setup_result(self, flow_patches):
        setup = SetupResult(worktree_path="/repos/42", branch_name="feature/42/x", mode="created")
        commit_node({"issue_key": "42", "setup_result": setup})
        # stage_changes receives cwd; commit run_git_safe receives cwd kwarg.
        assert flow_patches["stage"].call_args.kwargs["cwd"] == "/repos/42"
        assert flow_patches["run_safe"].call_args_list[0].kwargs["cwd"] == "/repos/42"
        flow_patches["rebase"].assert_called_once_with("/repos/42", False, issue_key="42")

    def test_supplied_commit_message_used_verbatim(self, flow_patches):
        """When state carries commit_message it is used as-is, not generated."""
        explicit_msg = "fix(#42): correct off-by-one in scheduler\n\n#42"
        result = commit_node(
            {
                "issue_key": "42",
                "setup_result": flow_patches["setup"],
                "commit_message": explicit_msg,
            }
        )
        assert result["error"] is None
        # The message passed to git commit must be the exact supplied string.
        commit_call_msg = flow_patches["run_safe"].call_args_list[0][0][0]
        assert commit_call_msg[-1] == explicit_msg

    def test_generated_message_used_when_commit_message_absent(self, flow_patches):
        """When commit_message is not in state, message is auto-generated."""
        result = commit_node(
            {
                "issue_key": "42",
                "setup_result": flow_patches["setup"],
                "issue_data": {"summary": "Add webhook support"},
            }
        )
        assert result["error"] is None
        commit_call_msg = flow_patches["run_safe"].call_args_list[0][0][0]
        assert "feat(#42):" in commit_call_msg[-1]

    def test_generated_message_used_when_commit_message_is_blank(self, flow_patches):
        """A blank commit_message in state triggers auto-generation."""
        result = commit_node(
            {
                "issue_key": "42",
                "setup_result": flow_patches["setup"],
                "commit_message": "   ",
                "issue_data": {"summary": "Add webhook support"},
            }
        )
        assert result["error"] is None
        commit_call_msg = flow_patches["run_safe"].call_args_list[0][0][0]
        assert "feat(#42):" in commit_call_msg[-1]

    def test_no_staged_retry_push_git_error_returns_transient_block(self, flow_patches):
        """GitError raised by _retry_unpublished_push probe is caught and returned as transient."""
        flow_patches["has_staged"].return_value = False
        prior = CommitResult(
            commit_sha="deadbeef",
            push_succeeded=False,
            error=BlockedState(category="transient", message="push timed out"),
        )

        def raise_on_head_probe(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout=_DEFAULT_SETUP.branch_name)
            if args == ["rev-parse", "--short", "HEAD"]:
                raise GitError(128, "fatal: not a git repository", ["rev-parse"])
            return _proc(stdout="deadbeef")

        flow_patches["capture"].side_effect = raise_on_head_probe
        result = commit_node({"issue_key": "42", "setup_result": flow_patches["setup"], "commit_result": prior})
        assert result["commit_result"].error is not None
        assert result["commit_result"].error.category == "transient"
        assert "Push retry probe failed" in result["error"]
        assert result["commit_created"] is False
