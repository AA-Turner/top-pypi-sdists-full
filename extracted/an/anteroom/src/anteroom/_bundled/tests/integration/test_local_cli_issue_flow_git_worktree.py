from __future__ import annotations

import importlib.util
import io
import json
import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "workflows" / "local_cli_issue_flow.py"
_SPEC = importlib.util.spec_from_file_location("local_cli_issue_flow", _SCRIPT)
helper = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(helper)


def _git(*args: str, cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}"
        raise AssertionError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout.strip()


def _create_repo(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    remote.mkdir()
    _git("init", "--bare", cwd=remote)
    root.mkdir()
    _git("init", "-b", "main", cwd=root)
    _git("config", "user.name", "Test User", cwd=root)
    _git("config", "user.email", "test@example.com", cwd=root)
    _git("remote", "add", "origin", str(remote), cwd=root)
    (root / "README.md").write_text("seed\n")
    _git("add", "README.md", cwd=root)
    _git("commit", "-m", "seed", cwd=root)
    _git("update-ref", "refs/remotes/origin/main", "HEAD", cwd=root)
    return remote, root


def _issue(number: int, title: str) -> dict[str, str]:
    return {
        "state": "open",
        "title": title,
        "url": f"https://example.com/issues/{number}",
    }


class TestLocalCliIssueFlowGitWorktree:
    def test_ensure_worktree_creates_real_worktree_and_state(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Real worktree integration")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = Path(state["worktree_path"])
        expected = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])
        state_file = root / ".git" / helper.STATE_DIRNAME / f"issue-{issue_number}" / "state.json"
        saved = json.loads(state_file.read_text())

        assert worktree == expected
        assert worktree.exists()
        assert _git("branch", "--show-current", cwd=worktree) == branch
        assert saved["branch"] == branch
        assert saved["worktree_path"] == str(worktree)
        assert state_file.parent.parent == (root / ".git" / helper.STATE_DIRNAME)
        entries = helper.list_worktrees(root)
        assert any(entry.get("worktree") == str(root) for entry in entries)
        assert any(
            entry.get("worktree") == str(worktree) and entry.get("branch") == f"refs/heads/{branch}"
            for entry in entries
        )

    def test_state_dir_uses_shared_git_common_dir_from_linked_worktree(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Shared state dir")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
        ):
            state = helper.ensure_worktree(root, issue_number)

        worktree = Path(state["worktree_path"])
        root_state = helper.state_path(root, issue_number)
        worktree_state = helper.state_path(worktree, issue_number)

        assert root_state == worktree_state
        assert root_state.exists()

    def test_ensure_worktree_reuses_branch_checked_out_in_attached_worktree(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Reuse attached worktree")
        branch = helper.issue_branch(issue_number, issue["title"])
        attached = tmp_path / "attached-worktree"

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(attached), branch, cwd=root)

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        entries = helper.list_worktrees(root)
        assert Path(state["worktree_path"]) == attached.resolve()
        assert not helper.issue_worktree(root, "owner/repo", issue_number, issue["title"]).exists()
        assert sum(1 for entry in entries if entry.get("branch") == f"refs/heads/{branch}") == 1

    def test_ensure_worktree_prunes_stale_meta_before_fast_forwarding_stale_branch(self, tmp_path: Path) -> None:
        """Regression for PR #1198 senior review blocker.

        When a linked worktree directory is deleted WITHOUT running
        ``git worktree prune`` AND the issue branch is also stale (at a prior
        base_ref), a naive ``git branch -f`` fails with:

            fatal: cannot force update the branch 'issue-...'
                   checked out at '<missing path>'

        ``ensure_worktree`` must prune the stale registration before the
        fast-forward so the recovery path actually recovers. This test
        exercises the real Git error path and would have caught the bug
        before the earlier PR head that only ran mocked unit coverage.
        """
        import shutil

        _, root = _create_repo(tmp_path)
        issue_number = 1197
        issue = _issue(issue_number, "Prune stale meta then refresh stale branch")
        branch = helper.issue_branch(issue_number, issue["title"])
        expected = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        # 1. Create a branch at main and attach a worktree to it.
        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(expected), branch, cwd=root)

        # 2. Delete the worktree directory directly. Do NOT run
        #    `git worktree remove` -- that would also unregister the worktree
        #    cleanly. We want the stale-metadata condition where git still
        #    thinks the branch is "checked out" at a missing path.
        shutil.rmtree(expected)
        entries = helper.list_worktrees(root)
        assert any(entry.get("branch") == f"refs/heads/{branch}" for entry in entries), (
            "precondition: stale worktree registration should still exist after rmtree"
        )

        # 3. Move main forward so the branch is both stale and behind the
        #    current base_ref. This makes ensure_worktree take the
        #    branch-refresh (fast-forward) path.
        (root / "README.md").write_text("seed\nmain moved forward\n")
        _git("add", "README.md", cwd=root)
        _git("commit", "-m", "main update after stale worktree", cwd=root)
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)
        main_head = _git("rev-parse", "main", cwd=root)

        # 4. ensure_worktree should succeed: prune stale meta, force-update
        #    the branch, recreate the worktree.
        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        # 5. Assertions:
        assert Path(state["worktree_path"]) == expected
        assert expected.exists()
        # Branch is now at the new main HEAD (fast-forwarded).
        assert _git("rev-parse", branch, cwd=root) == main_head
        # Exactly one worktree entry for this branch -- stale meta was pruned.
        final_entries = helper.list_worktrees(root)
        branch_entries = [e for e in final_entries if e.get("branch") == f"refs/heads/{branch}"]
        assert len(branch_entries) == 1
        assert branch_entries[0].get("worktree") == str(expected)

    def test_ensure_worktree_recovers_when_expected_path_is_missing(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Recover missing worktree path")
        branch = helper.issue_branch(issue_number, issue["title"])
        expected = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(expected), branch, cwd=root)
        _git("worktree", "remove", "--force", str(expected), cwd=root)
        expected.parent.mkdir(parents=True, exist_ok=True)

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        entries = helper.list_worktrees(root)
        assert Path(state["worktree_path"]) == expected
        assert expected.exists()
        assert _git("branch", "--show-current", cwd=expected) == branch
        assert sum(1 for entry in entries if entry.get("branch") == f"refs/heads/{branch}") == 1

    def test_branch_status_reports_ahead_and_behind_counts(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        _git("branch", "issue-1206-branch", "main", cwd=root)
        _git("checkout", "issue-1206-branch", cwd=root)
        (root / "feature.txt").write_text("feature\n")
        _git("add", "feature.txt", cwd=root)
        _git("commit", "-m", "feature", cwd=root)
        _git("checkout", "main", cwd=root)
        (root / "README.md").write_text("seed\nmain update\n")
        _git("add", "README.md", cwd=root)
        _git("commit", "-m", "main update", cwd=root)
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        status = helper.branch_status(root, "issue-1206-branch", "main")

        assert status["ahead_of_base"] == 1
        assert status["behind_base"] == 1
        assert status["diverged"] is True
        assert status["needs_refresh"] is True

    def test_branch_status_uses_fetched_remote_base_when_local_main_is_stale(self, tmp_path: Path) -> None:
        remote, root = _create_repo(tmp_path)
        upstream = tmp_path / "upstream"
        upstream.mkdir()
        _git("init", "-b", "main", cwd=upstream)
        _git("config", "user.name", "Test User", cwd=upstream)
        _git("config", "user.email", "test@example.com", cwd=upstream)
        root_main = _git("rev-parse", "main", cwd=root)
        _git("fetch", str(root), root_main, cwd=upstream)
        _git("checkout", root_main, cwd=upstream)
        _git("switch", "-c", "main", cwd=upstream)
        (upstream / "README.md").write_text("seed\nremote update\n")
        _git("add", "README.md", cwd=upstream)
        _git("commit", "-m", "remote main update", cwd=upstream)
        _git("fetch", str(upstream), "main:refs/heads/main", cwd=remote)

        _git("branch", "issue-1206-branch", "main", cwd=root)
        _git("checkout", "issue-1206-branch", cwd=root)
        (root / "feature.txt").write_text("feature\n")
        _git("add", "feature.txt", cwd=root)
        _git("commit", "-m", "feature", cwd=root)

        status = helper.branch_status(root, "issue-1206-branch", "main")

        assert status["ahead_of_base"] == 1
        assert status["behind_base"] == 1
        assert status["diverged"] is True
        assert status["needs_refresh"] is True

    def test_inspect_pr_state_reports_refresh_needed_for_behind_issue_branch(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1205
        issue = _issue(issue_number, "Route PR refresh coverage")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        (root / "README.md").write_text("seed\nmain update\n")
        _git("add", "README.md", cwd=root)
        _git("commit", "-m", "main update", cwd=root)
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        # Stub ensure_worktree so #1197's stale-branch fast-forward does not
        # clobber the test fixture. This test exercises inspect_pr_state +
        # branch_status, not ensure_worktree.
        fake_state = {
            "branch": branch,
            "worktree_path": str(worktree),
            "repo_name": "owner/repo",
            "issue_number": issue_number,
            "issue_title": issue["title"],
            "issue_url": issue["url"],
        }

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch.object(helper, "ensure_worktree", return_value=fake_state),
            patch.object(helper, "current_pr_number", return_value=77),
            patch.object(
                helper,
                "run_json",
                return_value={
                    "number": 77,
                    "url": "https://example.com/pr/77",
                    "state": "OPEN",
                    "isDraft": False,
                    "reviewDecision": "APPROVED",
                    "labels": [{"name": "needs-senior-review"}],
                    "mergeable": "MERGEABLE",
                    "headRefName": branch,
                    "baseRefName": "main",
                    "headRefOid": _git("rev-parse", branch, cwd=root),
                    "baseRefOid": _git("rev-parse", "main", cwd=root),
                    "statusCheckRollup": [{"conclusion": "SUCCESS", "status": "COMPLETED"}],
                },
            ),
        ):
            state = helper.inspect_pr_state(root, issue_number)

        assert state["exists"] is True
        assert state["pr_number"] == 77
        assert state["branch_status"]["head_ref"] == branch
        assert state["branch_status"]["behind_base"] == 1
        assert state["branch_status"]["needs_refresh"] is True
        assert state["lifecycle"] == "refresh_needed"

    def test_ensure_worktree_reused_junk_only_succeeds_and_records_prepare_state(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1223
        issue = _issue(issue_number, "Clean reusable worktree")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        junk = worktree / "<MagicMock name='mock.app.data_dir.__truediv__()' id='123'>"
        junk.write_text("junk")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        assert not junk.exists()
        assert state["prepare_worktree_status"] == "reused_junk_cleaned"
        assert state["prepare_removed_junk"] == [junk.name]
        assert state["prepare_tracked_dirty_paths"] == []
        assert state["prepare_unexpected_untracked_paths"] == []
        assert _git("status", "--porcelain", cwd=worktree) == ""

    def test_ensure_worktree_reused_tracked_dirty_blocks_after_junk_cleanup(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1223
        issue = _issue(issue_number, "Dirty reusable worktree")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        (worktree / "README.md").write_text("seed\ndirty\n")
        junk = worktree / "<MagicMock name='mock.app.data_dir.__truediv__()' id='123'>"
        junk.write_text("junk")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            with pytest.raises(SystemExit) as exc_info:
                helper.ensure_worktree(root, issue_number)

        assert exc_info.value.code == 1
        assert not junk.exists()
        assert "Refusing to reuse dirty issue worktree with tracked changes: README.md" in stderr.getvalue()
        status_lines = _git("status", "--porcelain", cwd=worktree).splitlines()
        assert status_lines == ["M README.md"]

    def test_ensure_worktree_reused_untracked_non_junk_blocks_without_deleting_file(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1223
        issue = _issue(issue_number, "Unexpected untracked reusable worktree")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        stray = worktree / "notes.txt"
        stray.write_text("keep me\n")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            with pytest.raises(SystemExit) as exc_info:
                helper.ensure_worktree(root, issue_number)

        assert exc_info.value.code == 1
        assert stray.exists()
        assert "Refusing to reuse issue worktree with unexpected untracked files: notes.txt" in stderr.getvalue()
        assert _git("status", "--porcelain", cwd=worktree) == "?? notes.txt"

    def test_ensure_worktree_reused_cleans_tmp_issue_body_files(self, tmp_path: Path) -> None:
        _, root = _create_repo(tmp_path)
        issue_number = 1227
        issue = _issue(issue_number, "Temp issue body cleanup")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        tmp_body = worktree / ".tmp_issue_1227_body.md"
        tmp_body.write_text("temp body\n")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            state = helper.ensure_worktree(root, issue_number)

        assert not tmp_body.exists()
        assert state["prepare_worktree_status"] == "reused_junk_cleaned"
        assert _git("status", "--porcelain", cwd=worktree) == ""

    # ------------------------------------------------------------------
    # branch_status fast-path coverage (#1199)
    # ------------------------------------------------------------------

    def test_branch_status_clean_when_head_matches_base(self, tmp_path: Path) -> None:
        """Branch at main with no divergence: ahead=0, behind=0, no refresh."""
        _, root = _create_repo(tmp_path)
        _git("branch", "issue-1199-clean", "main", cwd=root)

        status = helper.branch_status(root, "issue-1199-clean", "main")

        assert status["ahead_of_base"] == 0
        assert status["behind_base"] == 0
        assert status["diverged"] is False
        assert status["needs_refresh"] is False

    def test_branch_status_ahead_only_does_not_require_refresh(self, tmp_path: Path) -> None:
        """Branch with its own commits but main unchanged: ahead only, no refresh."""
        _, root = _create_repo(tmp_path)
        _git("branch", "issue-1199-ahead", "main", cwd=root)
        _git("checkout", "issue-1199-ahead", cwd=root)
        (root / "feature.txt").write_text("feature\n")
        _git("add", "feature.txt", cwd=root)
        _git("commit", "-m", "feature", cwd=root)
        # Keep origin/main pointing at the current main (unchanged).
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        status = helper.branch_status(root, "issue-1199-ahead", "main")

        assert status["ahead_of_base"] == 1
        assert status["behind_base"] == 0
        assert status["diverged"] is False
        assert status["needs_refresh"] is False

    # ------------------------------------------------------------------
    # inspect_pr_state lifecycle coverage (#1199)
    # ------------------------------------------------------------------

    def test_inspect_pr_state_no_pr_when_branch_has_no_open_pr(self, tmp_path: Path) -> None:
        """current_pr_number() returns None → early-return path with lifecycle=no_pr."""
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Inspect no-PR path")

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            # No PR → early return; run_json MUST NOT be called because
            # current_pr_number short-circuits the whole path.
            patch.object(helper, "current_pr_number", return_value=None),
        ):
            state = helper.inspect_pr_state(root, issue_number)

        assert state["exists"] is False
        assert state["pr_number"] is None
        assert state["lifecycle"] == "no_pr"
        assert state["ready_for_senior_review"] is False

    def test_inspect_pr_state_review_only_when_branch_up_to_date_and_checks_pass(self, tmp_path: Path) -> None:
        """Up-to-date non-draft MERGEABLE PR with passing checks → review_only."""
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Inspect review-only path")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        # Keep branch at main and origin/main in sync -- no refresh needed.
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        # Stub ensure_worktree so #1197's stale-branch fast-forward path is
        # not exercised here (this test is about classify_pr_lifecycle, not
        # ensure_worktree). Matches the pattern used by the behind_base test
        # above.
        fake_state = {
            "branch": branch,
            "worktree_path": str(worktree),
            "repo_name": "owner/repo",
            "issue_number": issue_number,
            "issue_title": issue["title"],
            "issue_url": issue["url"],
        }

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch.object(helper, "ensure_worktree", return_value=fake_state),
            patch.object(helper, "current_pr_number", return_value=88),
            patch.object(
                helper,
                "run_json",
                return_value={
                    "number": 88,
                    "url": "https://example.com/pr/88",
                    "state": "OPEN",
                    "isDraft": False,
                    "reviewDecision": "APPROVED",
                    "labels": [{"name": "senior-approved"}],
                    "mergeable": "MERGEABLE",
                    "headRefName": branch,
                    "baseRefName": "main",
                    "headRefOid": _git("rev-parse", branch, cwd=root),
                    "baseRefOid": _git("rev-parse", "main", cwd=root),
                    "statusCheckRollup": [{"conclusion": "SUCCESS", "status": "COMPLETED"}],
                },
            ),
        ):
            state = helper.inspect_pr_state(root, issue_number)

        assert state["exists"] is True
        assert state["pr_number"] == 88
        assert state["branch_status"]["behind_base"] == 0
        assert state["branch_status"]["ahead_of_base"] == 0
        assert state["branch_status"]["needs_refresh"] is False
        assert state["lifecycle"] == "review_only"
        assert state["ready_for_senior_review"] is True

    def test_inspect_pr_state_review_repair_when_draft_or_checks_failing(self, tmp_path: Path) -> None:
        """Draft PR OR failing checks → review_repair (not senior-review-ready)."""
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Inspect review-repair path")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        fake_state = {
            "branch": branch,
            "worktree_path": str(worktree),
            "repo_name": "owner/repo",
            "issue_number": issue_number,
            "issue_title": issue["title"],
            "issue_url": issue["url"],
        }

        head_oid = _git("rev-parse", branch, cwd=root)
        base_oid = _git("rev-parse", "main", cwd=root)

        def _make_pr_data(*, is_draft: bool, check_conclusion: str) -> dict[str, Any]:
            return {
                "number": 89,
                "url": "https://example.com/pr/89",
                "state": "OPEN",
                "isDraft": is_draft,
                "reviewDecision": "",
                "labels": [],
                "mergeable": "MERGEABLE",
                "headRefName": branch,
                "baseRefName": "main",
                "headRefOid": head_oid,
                "baseRefOid": base_oid,
                "statusCheckRollup": [{"conclusion": check_conclusion, "status": "COMPLETED"}],
            }

        # Case A: draft PR, checks passing -> review_repair (is_draft branch)
        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch.object(helper, "ensure_worktree", return_value=fake_state),
            patch.object(helper, "current_pr_number", return_value=89),
            patch.object(
                helper,
                "run_json",
                return_value=_make_pr_data(is_draft=True, check_conclusion="SUCCESS"),
            ),
        ):
            state = helper.inspect_pr_state(root, issue_number)
        assert state["lifecycle"] == "review_repair", "draft PR must be review_repair"
        assert state["ready_for_senior_review"] is False

        # Case B: non-draft PR but checks failing -> review_repair (has_required_failures branch)
        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
            patch.object(helper, "ensure_worktree", return_value=fake_state),
            patch.object(helper, "current_pr_number", return_value=89),
            patch.object(
                helper,
                "run_json",
                return_value=_make_pr_data(is_draft=False, check_conclusion="FAILURE"),
            ),
        ):
            state = helper.inspect_pr_state(root, issue_number)
        assert state["lifecycle"] == "review_repair", "failing checks must be review_repair"
        assert state["ready_for_senior_review"] is False

    # ------------------------------------------------------------------
    # ensure_worktree diverged-branch fail-path (#1199)
    # ------------------------------------------------------------------

    def test_ensure_worktree_diverged_branch_rejects_prepare(self, tmp_path: Path) -> None:
        """A branch with real divergent work from origin/main must fail prepare
        rather than silently rewriting state."""
        _, root = _create_repo(tmp_path)
        issue_number = 1199
        issue = _issue(issue_number, "Diverged branch")
        branch = helper.issue_branch(issue_number, issue["title"])
        worktree = helper.issue_worktree(root, "owner/repo", issue_number, issue["title"])

        # Create branch at main and check it out in its own worktree; commit
        # on the branch so it's ahead of main.
        _git("branch", branch, "main", cwd=root)
        _git("worktree", "add", str(worktree), branch, cwd=root)
        (worktree / "feature.txt").write_text("feature work\n")
        _git("add", "feature.txt", cwd=worktree)
        _git("commit", "-m", "feature work on issue branch", cwd=worktree)
        branch_tip_before = _git("rev-parse", branch, cwd=root)

        # Move main forward on a different line so branch is now BOTH ahead
        # and behind main (diverged).
        (root / "README.md").write_text("seed\nmain moved\n")
        _git("add", "README.md", cwd=root)
        _git("commit", "-m", "main update", cwd=root)
        _git("update-ref", "refs/remotes/origin/main", "main", cwd=root)

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
        ):
            with pytest.raises(SystemExit) as exc_info:
                helper.ensure_worktree(root, issue_number)

        assert exc_info.value.code == 1
        # Branch and worktree are untouched: the feature commit is still
        # there and the worktree file is intact.
        assert _git("rev-parse", branch, cwd=root) == branch_tip_before
        assert (worktree / "feature.txt").exists()
