"""Tests for setup_node (worktree creation/resume — issue #1900)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.cli.git.worktree import DetectionResult
from agentic_devtools.models.git_results import BlockedState, SetupResult
from agentic_devtools.orchestration.nodes.setup import setup_node

_MOD = "agentic_devtools.orchestration.nodes.setup"


def _proc(stdout: str = "", returncode: int = 0):
    return MagicMock(returncode=returncode, stdout=stdout, stderr="")


@pytest.fixture
def base_patches():
    """Patch the external helpers used by setup_node with safe defaults.

    Defaults simulate: main repo root context (not in a worktree), branch/folder
    that do NOT reference the issue (so pre-flight passes at repo root), a
    successful fetch, and a ``not_found`` detection.
    """
    with (
        patch(f"{_MOD}.get_current_git_branch", return_value="main") as branch,
        patch(f"{_MOD}.get_git_repo_root", return_value="/repos/agentic-devtools") as repo_root,
        patch(f"{_MOD}.get_main_repo_root", return_value="/repos/agentic-devtools") as main_root,
        patch(f"{_MOD}.is_in_worktree", return_value=False) as in_wt,
        patch(f"{_MOD}.run_git_safe", return_value=_proc()) as run_safe,
        patch(f"{_MOD}.detect_existing_worktree") as detect,
        patch(f"{_MOD}.create_worktree") as create,
        patch(f"{_MOD}._find_remote_branch", return_value=None) as find_remote,
    ):
        detect.return_value = DetectionResult(status="not_found")
        create.return_value = SetupResult(worktree_path="/repos/42", branch_name="feature/42/impl", mode="created")
        yield {
            "branch": branch,
            "repo_root": repo_root,
            "main_root": main_root,
            "in_wt": in_wt,
            "run_safe": run_safe,
            "detect": detect,
            "create": create,
            "find_remote": find_remote,
        }


# --- issue key validation ------------------------------------------------------


class TestSetupNodeValidation:
    def test_empty_issue_key_blocks(self):
        result = setup_node({"issue_key": ""})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"
        assert result["events"][0]["event"] == "setup_failed"

    def test_missing_issue_key_blocks(self):
        result = setup_node({})
        assert result["setup_complete"] is False
        assert "issue_key" in result["error"]

    @pytest.mark.parametrize("bad", [42, None, [], {}])
    def test_non_string_issue_key_blocks(self, bad):
        result = setup_node({"issue_key": bad})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_invalid_issue_key_blocks(self):
        # "#" normalizes to empty -> ValueError inside normalize_issue_key
        result = setup_node({"issue_key": "#"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"


# --- pre-flight context --------------------------------------------------------


class TestSetupNodePreflight:
    def test_context_mismatch_when_in_different_worktree(self, base_patches):
        base_patches["branch"].return_value = "feature/99/other"
        base_patches["repo_root"].return_value = "/repos/99"
        base_patches["in_wt"].return_value = True
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_branch_match_allows_proceed(self, base_patches):
        base_patches["branch"].return_value = "feature/42/impl"
        base_patches["detect"].return_value = DetectionResult(
            status="resume", path="/repos/42", branch="feature/42/impl"
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is True
        assert result["setup_result"].mode == "resumed"

    def test_folder_match_allows_proceed(self, base_patches):
        base_patches["branch"].return_value = "main"
        base_patches["repo_root"].return_value = "/repos/42"
        base_patches["detect"].return_value = DetectionResult(
            status="resume", path="/repos/42", branch="feature/42/impl"
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is True

    def test_folder_match_only_inside_worktree_blocks(self, base_patches):
        """Inside a linked worktree, folder match alone is not enough — branch must also match."""
        base_patches["branch"].return_value = "main"  # branch does NOT match
        base_patches["repo_root"].return_value = "/repos/42"  # folder matches
        base_patches["in_wt"].return_value = True
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_branch_match_only_inside_worktree_blocks(self, base_patches):
        """Inside a linked worktree, branch match alone is not enough — folder must also match."""
        base_patches["branch"].return_value = "feature/42/impl"  # branch matches
        base_patches["repo_root"].return_value = "/repos/agentic-devtools"  # folder does NOT match
        base_patches["in_wt"].return_value = True
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_both_branch_and_folder_match_inside_worktree_allows_proceed(self, base_patches):
        """Inside a linked worktree, both folder AND branch must match to proceed."""
        base_patches["branch"].return_value = "feature/42/impl"  # branch matches
        base_patches["repo_root"].return_value = "/repos/42"  # folder matches
        base_patches["in_wt"].return_value = True
        base_patches["detect"].return_value = DetectionResult(
            status="resume", path="/repos/42", branch="feature/42/impl"
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is True
        assert result["setup_result"].mode == "resumed"


# --- repo root resolution / fetch ---------------------------------------------


class TestSetupNodeInfra:
    def test_missing_repo_root_blocks(self, base_patches):
        base_patches["main_root"].return_value = None
        base_patches["repo_root"].return_value = None
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_dry_run_returns_simulated_result_without_git_mutations(self, base_patches):
        """dry_run=True returns a simulated SetupResult without fetch/create/ls-remote."""
        result = setup_node({"issue_key": "42", "dry_run": True})
        assert result["setup_complete"] is True
        assert result["setup_result"].error is None
        assert result["setup_result"].mode == "created"
        assert result["setup_result"].branch_name is not None
        assert result["setup_result"].worktree_path is not None
        # No git mutations should have been triggered.
        base_patches["run_safe"].assert_not_called()
        base_patches["create"].assert_not_called()

    def test_fetch_failure_is_transient_block(self, base_patches):
        base_patches["run_safe"].side_effect = GitError(1, "network down", ["fetch", "origin"])
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "transient"

    def test_fetch_uses_main_root_when_main_root_none(self, base_patches):
        # main_root None -> falls back to repo_root (non-empty), still proceeds.
        base_patches["main_root"].return_value = None
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is True

    def test_detection_git_error_is_transient_block(self, base_patches):
        base_patches["detect"].side_effect = GitError(1, "boom", ["worktree", "list"])
        result = setup_node({"issue_key": "42"})
        assert result["setup_result"].error.category == "transient"


# --- detection outcomes --------------------------------------------------------


class TestSetupNodeDetection:
    def test_corrupt_detection_blocks(self, base_patches):
        base_patches["detect"].return_value = DetectionResult(status="corrupt", path="/repos/42")
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "corruption"

    def test_resume_with_known_branch(self, base_patches):
        base_patches["detect"].return_value = DetectionResult(
            status="resume", path="/repos/42", branch="feature/42/impl"
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_result"].mode == "resumed"
        assert result["source_branch"] == "feature/42/impl"

    def test_resume_looks_up_branch_when_missing(self, base_patches):
        base_patches["detect"].return_value = DetectionResult(status="resume", path="/repos/42", branch=None)
        base_patches["run_safe"].side_effect = [_proc(), _proc(stdout="feature/42/found")]
        result = setup_node({"issue_key": "42"})
        assert result["setup_result"].branch_name == "feature/42/found"

    def test_resume_branch_lookup_failure_blocks(self, base_patches):
        """A GitError during branch lookup blocks setup as context_mismatch."""
        base_patches["detect"].return_value = DetectionResult(status="resume", path="/repos/42", branch=None)
        base_patches["run_safe"].side_effect = [_proc(), GitError(1, "x", ["rev-parse"])]
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"
        assert "detached" in result["error"] or "named branch" in result["error"]

    def test_resume_branch_lookup_empty_blocks(self, base_patches):
        """An empty/whitespace branch from lookup blocks setup as context_mismatch."""
        base_patches["detect"].return_value = DetectionResult(status="resume", path="/repos/42", branch=None)
        base_patches["run_safe"].side_effect = [_proc(), _proc(stdout="   ")]
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"

    def test_resume_detached_head_blocks(self, base_patches):
        """A detached HEAD worktree (branch='HEAD') blocks setup as context_mismatch."""
        base_patches["detect"].return_value = DetectionResult(status="resume", path="/repos/42", branch=None)
        base_patches["run_safe"].side_effect = [_proc(), _proc(stdout="HEAD")]
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"
        assert "detached" in result["error"]

    def test_resume_branch_unrelated_to_issue_key_blocks(self, base_patches):
        """A resumed worktree whose branch does not contain the issue key is blocked."""
        base_patches["detect"].return_value = DetectionResult(status="resume", path="/repos/42", branch="main")
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "context_mismatch"
        assert "main" in result["error"]


# --- create / remote tracking --------------------------------------------------


class TestSetupNodeCreate:
    def test_fresh_create_uses_origin_main_start_point(self, base_patches):
        result = setup_node({"issue_key": "42", "issue_data": {"summary": "Add webhook support"}})
        assert result["setup_complete"] is True
        assert result["setup_result"].mode == "created"
        _, kwargs = base_patches["create"].call_args
        assert kwargs["start_point"] == "origin/main"

    def test_fresh_create_failure_blocks(self, base_patches):
        base_patches["create"].return_value = SetupResult(
            error=BlockedState(category="corruption", message="add failed")
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "corruption"

    def test_fresh_create_sets_branch_name_when_missing(self, base_patches):
        base_patches["create"].return_value = SetupResult(worktree_path="/repos/42", branch_name=None, mode="created")
        result = setup_node({"issue_key": "42", "issue_data": {"summary": "cool feature title"}})
        assert result["setup_result"].branch_name == "feature/42/cool-feature-title"

    def test_remote_branch_tracking_resumes(self, base_patches):
        base_patches["find_remote"].return_value = "feature/42/remote"
        base_patches["create"].return_value = SetupResult(
            worktree_path="/repos/42", branch_name="feature/42/remote", mode="created"
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_result"].mode == "resumed"
        _, kwargs = base_patches["create"].call_args
        assert kwargs["use_existing_branch"] is True
        assert kwargs["branch_name"] == "feature/42/remote"

    def test_remote_branch_tracking_failure_blocks(self, base_patches):
        base_patches["find_remote"].return_value = "feature/42/remote"
        base_patches["create"].return_value = SetupResult(
            error=BlockedState(category="transient", message="track failed")
        )
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False

    def test_ls_remote_git_error_blocks_transient(self, base_patches):
        """A GitError from ls-remote (transient network/auth) is classified as transient."""
        # Replace the patched _find_remote_branch with the real function path so
        # the GitError propagates through the real call site in setup_node.
        base_patches["find_remote"].side_effect = GitError(128, "could not connect", ["ls-remote"])
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "transient"
        assert "ls-remote" in result["error"] or "transient" in result["setup_result"].error.category

    def test_ls_remote_auth_failure_blocks_auth(self, base_patches):
        """A GitError from ls-remote with auth stderr is classified as auth."""
        base_patches["find_remote"].side_effect = GitError(128, "Authentication failed for origin", ["ls-remote"])
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is False
        assert result["setup_result"].error.category == "auth"

    def test_description_defaults_to_implementation(self, base_patches):
        result = setup_node({"issue_key": "42"})
        assert result["setup_complete"] is True
        args, _ = base_patches["create"].call_args
        assert args[1] == "implementation"

    def test_non_dict_issue_data_defaults_description(self, base_patches):
        setup_node({"issue_key": "42", "issue_data": "not-a-dict"})
        args, _ = base_patches["create"].call_args
        assert args[1] == "implementation"

    def test_blank_summary_defaults_description(self, base_patches):
        setup_node({"issue_key": "42", "issue_data": {"summary": "   "}})
        args, _ = base_patches["create"].call_args
        assert args[1] == "implementation"
