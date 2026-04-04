from __future__ import annotations

import importlib.util
import io
import json
import subprocess
from pathlib import Path
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

        with (
            patch.object(helper, "issue_data", return_value=issue),
            patch.object(helper, "repo_name", return_value="owner/repo"),
            patch.object(helper, "git_dir", return_value=(root / ".git").resolve()),
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
