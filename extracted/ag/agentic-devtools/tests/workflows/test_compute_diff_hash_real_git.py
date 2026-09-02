"""Real-repository tests for ``GitHubActionsProvider.compute_diff_hash``."""

import os
import stat
import subprocess
from collections.abc import Callable
from pathlib import Path

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _run_git(cwd: Path, *args: str) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _make_remote_with_worktree(tmp_path: Path) -> tuple[Path, Path]:
    """Create a bare remote plus a working clone with baseline files."""
    seed = tmp_path / "seed"
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"

    seed.mkdir()
    _run_git(seed, "init", "--initial-branch=main")
    _run_git(seed, "config", "user.name", "Test User")
    _run_git(seed, "config", "user.email", "test@example.com")
    (seed / "tracked.txt").write_text("line one\n", encoding="utf-8")
    (seed / "rename_me.txt").write_text("rename me\n", encoding="utf-8")
    (seed / "mode_a.sh").write_text("#!/bin/sh\necho a\n", encoding="utf-8")
    (seed / "mode_b.sh").write_text("#!/bin/sh\necho b\n", encoding="utf-8")
    (seed / "delete_me.txt").write_text("delete me\n", encoding="utf-8")
    (seed / "binary.bin").write_bytes(b"\x00\x01\x02")
    _run_git(seed, "add", "-A")
    _run_git(seed, "commit", "-m", "base")

    _run_git(tmp_path, "clone", "--bare", str(seed), str(remote))
    _run_git(tmp_path, "clone", str(remote), str(work))
    _run_git(work, "config", "user.name", "Test User")
    _run_git(work, "config", "user.email", "test@example.com")
    return remote, work


def _hash_for_branch_change(
    work: Path, provider: GitHubActionsProvider, branch: str, mutate: Callable[[Path], None]
) -> str:
    """Create one branch-specific change and return the diff fingerprint."""
    _run_git(work, "checkout", "-B", branch, "origin/main")
    mutate(work)
    _run_git(work, "add", "-A")
    _run_git(work, "commit", "-m", f"{branch} change")
    sha = _run_git(work, "rev-parse", "HEAD")
    result = provider.compute_diff_hash(base_branch="main", sha=sha)
    assert result is not None
    assert result.startswith("patch-id:")
    return result


class TestComputeDiffHashRealGit:
    """Real-git scenarios validating rebase invariance and patch distinctions."""

    def test_rebase_keeps_same_fingerprint_for_same_patch(self, tmp_path: Path, monkeypatch) -> None:
        remote, work = _make_remote_with_worktree(tmp_path)
        maint = tmp_path / "maint"
        _run_git(tmp_path, "clone", str(remote), str(maint))
        _run_git(maint, "config", "user.name", "Maintainer")
        _run_git(maint, "config", "user.email", "maintainer@example.com")

        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        base_lines = [f"line {index}" for index in range(1, 11)]
        (maint / "tracked.txt").write_text("\n".join(base_lines) + "\n", encoding="utf-8")
        _run_git(maint, "add", "tracked.txt")
        _run_git(maint, "commit", "-m", "expand tracked baseline")
        _run_git(maint, "push", "origin", "main")

        _run_git(work, "fetch", "origin", "main")
        _run_git(work, "checkout", "-B", "feature/rebase-test", "origin/main")
        feature_lines = base_lines.copy()
        feature_lines[7] = "feature line 8"
        (work / "tracked.txt").write_text("\n".join(feature_lines) + "\n", encoding="utf-8")
        _run_git(work, "add", "tracked.txt")
        _run_git(work, "commit", "-m", "feature change")
        before_sha = _run_git(work, "rev-parse", "HEAD")
        before_hash = provider.compute_diff_hash(base_branch="main", sha=before_sha)

        rebased_base_lines = [base_lines[0], "base inserted", *base_lines[1:]]
        (maint / "tracked.txt").write_text("\n".join(rebased_base_lines) + "\n", encoding="utf-8")
        _run_git(maint, "add", "tracked.txt")
        _run_git(maint, "commit", "-m", "advance main")
        _run_git(maint, "push", "origin", "main")

        _run_git(work, "fetch", "origin", "main")
        _run_git(work, "rebase", "origin/main")
        after_sha = _run_git(work, "rev-parse", "HEAD")
        after_hash = provider.compute_diff_hash(base_branch="main", sha=after_sha)

        assert before_hash is not None
        assert after_hash is not None
        assert before_hash == after_hash

    def test_adjacent_base_insert_keeps_same_fingerprint(self, tmp_path: Path, monkeypatch) -> None:
        """A conflict-free base edit near the PR hunk must not change the fingerprint.

        This validates the core rebase-invariance property: a base-only line
        insertion that does NOT conflict with the PR's change (i.e., is more than
        one line away from the PR hunk) does not change the fingerprint.

        The immediate-neighbor case (inserting the line directly before or after
        the changed line) IS within the 1-line context window and would change the
        fingerprint under ``-U1``, but such insertions cause a rebase conflict in
        practice because the base change falls inside git's 3-line rebase context.
        A conflict-free pure rebase therefore cannot produce a false
        ``REASON_CONTENT_CHANGED`` signal.
        """
        remote, work = _make_remote_with_worktree(tmp_path)
        maint = tmp_path / "maint"
        _run_git(tmp_path, "clone", str(remote), str(maint))
        _run_git(maint, "config", "user.name", "Maintainer")
        _run_git(maint, "config", "user.email", "maintainer@example.com")

        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        # A 7-line base so the PR hunk (line 5) has ≥3 context lines on each side.
        base_lines = ["a", "b", "c", "d", "e", "f", "g"]
        (maint / "tracked.txt").write_text("\n".join(base_lines) + "\n", encoding="utf-8")
        _run_git(maint, "add", "tracked.txt")
        _run_git(maint, "commit", "-m", "stable base")
        _run_git(maint, "push", "origin", "main")

        _run_git(work, "fetch", "origin", "main")
        _run_git(work, "checkout", "-B", "feature/context-sensitivity", "origin/main")
        # PR changes only line 5 ("e").
        pr_lines = base_lines.copy()
        pr_lines[4] = "E_CHANGED"
        (work / "tracked.txt").write_text("\n".join(pr_lines) + "\n", encoding="utf-8")
        _run_git(work, "add", "tracked.txt")
        _run_git(work, "commit", "-m", "feature: change e to E_CHANGED")
        before_sha = _run_git(work, "rev-parse", "HEAD")
        before_hash = provider.compute_diff_hash(base_branch="main", sha=before_sha)

        # Base inserts a line between "c" (line 3) and "d" (line 4).  This is
        # 2 lines before the PR's changed line ("e"), so "d" still appears
        # immediately before "e" after the insertion and the ``-U1`` context
        # (lines "d" and "f") is unchanged.  The rebase succeeds without conflict
        # because git locates the unchanged "d\ne\nf" region and applies the
        # ``e → E_CHANGED`` substitution cleanly.
        advanced_lines = base_lines[:3] + ["c_extra"] + base_lines[3:]
        (maint / "tracked.txt").write_text("\n".join(advanced_lines) + "\n", encoding="utf-8")
        _run_git(maint, "add", "tracked.txt")
        _run_git(maint, "commit", "-m", "advance: insert c_extra 2 lines before changed line")
        _run_git(maint, "push", "origin", "main")

        _run_git(work, "fetch", "origin", "main")
        _run_git(work, "rebase", "origin/main")
        after_sha = _run_git(work, "rev-parse", "HEAD")
        after_hash = provider.compute_diff_hash(base_branch="main", sha=after_sha)

        assert before_hash is not None
        assert after_hash is not None
        assert before_hash == after_hash

    def test_distinguishes_binary_content_changes(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        def _binary_a(repo: Path) -> None:
            (repo / "binary.bin").write_bytes(b"\x00\x01\x03")

        def _binary_b(repo: Path) -> None:
            (repo / "binary.bin").write_bytes(b"\x00\x01\x04")

        hash_a = _hash_for_branch_change(work, provider, "feature/binary-a", _binary_a)
        hash_b = _hash_for_branch_change(work, provider, "feature/binary-b", _binary_b)
        assert hash_a != hash_b

    def test_distinguishes_rename_targets(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        def _rename_a(repo: Path) -> None:
            (repo / "rename_me.txt").rename(repo / "renamed_a.txt")

        def _rename_b(repo: Path) -> None:
            (repo / "rename_me.txt").rename(repo / "renamed_b.txt")

        hash_a = _hash_for_branch_change(work, provider, "feature/rename-a", _rename_a)
        hash_b = _hash_for_branch_change(work, provider, "feature/rename-b", _rename_b)
        assert hash_a != hash_b

    def test_distinguishes_mode_changes(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        def _content_only(repo: Path) -> None:
            (repo / "mode_a.sh").write_text("#!/bin/sh\necho updated\n", encoding="utf-8")

        def _content_plus_mode(repo: Path) -> None:
            (repo / "mode_a.sh").write_text("#!/bin/sh\necho updated\n", encoding="utf-8")
            mode = (repo / "mode_a.sh").stat().st_mode
            os.chmod(repo / "mode_a.sh", mode | stat.S_IXUSR)

        hash_a = _hash_for_branch_change(work, provider, "feature/content-only", _content_only)
        hash_b = _hash_for_branch_change(work, provider, "feature/content-plus-mode", _content_plus_mode)
        assert hash_a != hash_b

    def test_distinguishes_identical_replacement_at_different_occurrences(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        (work / "tracked.txt").write_text("prefix\nold\nmiddle\nold\nsuffix\n", encoding="utf-8")
        _run_git(work, "add", "tracked.txt")
        _run_git(work, "commit", "-m", "prepare repeated content")
        _run_git(work, "push", "origin", "HEAD:main")

        def _change_first_occurrence(repo: Path) -> None:
            (repo / "tracked.txt").write_text("prefix\nnew\nmiddle\nold\nsuffix\n", encoding="utf-8")

        def _change_second_occurrence(repo: Path) -> None:
            (repo / "tracked.txt").write_text("prefix\nold\nmiddle\nnew\nsuffix\n", encoding="utf-8")

        first_hash = _hash_for_branch_change(work, provider, "feature/replace-first", _change_first_occurrence)
        second_hash = _hash_for_branch_change(work, provider, "feature/replace-second", _change_second_occurrence)
        assert first_hash != second_hash

    def test_distinguishes_delete_from_create(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        def _delete(repo: Path) -> None:
            (repo / "delete_me.txt").unlink()

        def _create(repo: Path) -> None:
            (repo / "created.txt").write_text("created\n", encoding="utf-8")

        delete_hash = _hash_for_branch_change(work, provider, "feature/delete", _delete)
        create_hash = _hash_for_branch_change(
            work,
            provider,
            "feature/create",
            _create,
        )
        assert delete_hash != create_hash

    def test_distinguishes_whitespace_only_changes(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        def _whitespace_a(repo: Path) -> None:
            (repo / "tracked.txt").write_text("line one \n", encoding="utf-8")

        def _whitespace_b(repo: Path) -> None:
            (repo / "tracked.txt").write_text("line one\t\n", encoding="utf-8")

        hash_a = _hash_for_branch_change(
            work,
            provider,
            "feature/whitespace-a",
            _whitespace_a,
        )
        hash_b = _hash_for_branch_change(
            work,
            provider,
            "feature/whitespace-b",
            _whitespace_b,
        )
        assert hash_a != hash_b

    def test_keeps_same_fingerprint_after_tree_preserving_squash(self, tmp_path: Path, monkeypatch) -> None:
        _, work = _make_remote_with_worktree(tmp_path)
        monkeypatch.chdir(work)
        provider = GitHubActionsProvider(repo="owner/repo")

        _run_git(work, "checkout", "-B", "feature/two-commit", "origin/main")
        (work / "tracked.txt").write_text("line one\nfeature line\n", encoding="utf-8")
        _run_git(work, "add", "tracked.txt")
        _run_git(work, "commit", "-m", "change tracked file")
        (work / "created.txt").write_text("created\n", encoding="utf-8")
        _run_git(work, "add", "created.txt")
        _run_git(work, "commit", "-m", "add created file")
        before_sha = _run_git(work, "rev-parse", "HEAD")
        before_hash = provider.compute_diff_hash(base_branch="main", sha=before_sha)
        tracked_text = (work / "tracked.txt").read_text(encoding="utf-8")
        created_text = (work / "created.txt").read_text(encoding="utf-8")

        _run_git(work, "checkout", "-B", "feature/squashed", "origin/main")
        (work / "tracked.txt").write_text(tracked_text, encoding="utf-8")
        (work / "created.txt").write_text(created_text, encoding="utf-8")
        _run_git(work, "add", "-A")
        _run_git(work, "commit", "-m", "squashed change")
        after_sha = _run_git(work, "rev-parse", "HEAD")
        after_hash = provider.compute_diff_hash(base_branch="main", sha=after_sha)

        assert before_hash is not None
        assert after_hash is not None
        assert before_hash == after_hash
