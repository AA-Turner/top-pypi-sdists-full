"""Tests for detect_existing_worktree."""

from types import SimpleNamespace

from agentic_devtools.cli.git import worktree


class TestDetectExistingWorktree:
    """Tests for detect_existing_worktree."""

    def test_returns_resume_for_porcelain_match(self, monkeypatch, tmp_path):
        """A porcelain branch match whose path is a valid worktree returns resume details."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        # Create the matched worktree path so it exists on disk.
        wt_path = tmp_path / "1900"
        wt_path.mkdir()
        porcelain = f"worktree {wt_path}\nbranch refs/heads/feature/1900/tests\n"

        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))

        # _is_valid_worktree_dir calls run_git_capture to verify the path.
        shared_git_dir = str(repo_root / ".git")

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                return SimpleNamespace(returncode=0, stdout=shared_git_dir)
            return SimpleNamespace(returncode=128, stdout="")

        (wt_path / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "resume"
        assert result.path == str(wt_path)
        assert result.branch == "feature/1900/tests"

    def test_returns_corrupt_for_stale_porcelain_match_missing_path(self, monkeypatch, tmp_path):
        """A porcelain branch match whose registered path no longer exists is corrupt."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        # Porcelain points to a path that does NOT exist on disk.
        porcelain = "worktree /nonexistent/path/1900\nbranch refs/heads/feature/1900/tests\n"

        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == "/nonexistent/path/1900"

    def test_returns_corrupt_for_invalid_porcelain_path(self, monkeypatch, tmp_path):
        """A porcelain branch match whose path exists but fails git validation is corrupt."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        wt_path = tmp_path / "1900"
        wt_path.mkdir()
        # No .git entry — _is_valid_worktree_dir will return False.
        porcelain = f"worktree {wt_path}\nbranch refs/heads/feature/1900/tests\n"

        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))
        monkeypatch.setattr(
            worktree, "run_git_capture", lambda args, cwd=None: SimpleNamespace(returncode=128, stdout="")
        )

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == str(wt_path)

    def test_returns_resume_for_valid_conventional_path_when_no_porcelain_match(self, monkeypatch, tmp_path):
        """A conventional directory with a .git entry that git validates resumes with branch None."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        conventional = tmp_path / "1900"
        conventional.mkdir()
        (conventional / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))

        # _is_valid_worktree_dir calls rev-parse --git-dir and rev-parse --git-common-dir.
        # Both paths must resolve to the same common dir (the main repo's .git).
        shared_git_dir = str(repo_root / ".git")

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                # Both the worktree and main repo return the same absolute common dir.
                return SimpleNamespace(returncode=0, stdout=shared_git_dir)
            return SimpleNamespace(returncode=128, stdout="")

        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "resume"
        assert result.path == str(conventional)
        assert result.branch is None

    def test_returns_corrupt_for_stale_gitdir_file(self, monkeypatch, tmp_path):
        """A conventional directory with a .git file that git rejects is reported as corrupt (FR-010)."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        conventional = tmp_path / "1900"
        conventional.mkdir()
        (conventional / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))
        # Simulate a stale/broken gitdir: rev-parse --git-dir fails.
        monkeypatch.setattr(
            worktree, "run_git_capture", lambda args, cwd=None: SimpleNamespace(returncode=128, stdout="")
        )

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == str(conventional)

    def test_returns_corrupt_for_conventional_path_without_git_entry(self, monkeypatch, tmp_path):
        """A conventional directory without .git is reported as corrupt."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        conventional = tmp_path / "PROJECT-1234"
        conventional.mkdir()
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))

        result = worktree.detect_existing_worktree("PROJECT-1234", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == str(conventional)
        assert result.branch is None

    def test_returns_not_found_when_neither_porcelain_nor_conventional_path_match(self, monkeypatch, tmp_path):
        """No porcelain match and no conventional directory returns not_found."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        porcelain = "worktree /repo/other\nbranch refs/heads/feature/9999/tests\n"
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "not_found"
        assert result.path is None
        assert result.branch is None

    def test_porcelain_match_wins_over_corrupt_conventional_path(self, monkeypatch, tmp_path):
        """A valid porcelain match takes precedence over a stale conventional directory."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        # A stale conventional path exists alongside a valid porcelain-registered path.
        (tmp_path / "1900").mkdir()
        elsewhere = tmp_path / "elsewhere-1900"
        elsewhere.mkdir()
        (elsewhere / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        porcelain = f"worktree {elsewhere}\nbranch refs/heads/feature/1900/tests\n"

        shared_git_dir = str(repo_root / ".git")

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                return SimpleNamespace(returncode=0, stdout=shared_git_dir)
            return SimpleNamespace(returncode=128, stdout="")

        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))
        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "resume"
        assert result.path == str(elsewhere)

    def test_primary_checkout_on_issue_branch_is_not_treated_as_worktree(self, monkeypatch, tmp_path):
        """The main checkout on a matching branch is excluded from the scan result."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        sibling = tmp_path / "sibling-1900"
        sibling.mkdir()
        (sibling / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        # Porcelain includes the primary checkout (repo_root) on the issue branch.
        porcelain = (
            f"worktree {repo_root}\nbranch refs/heads/feature/1900/impl\n\n"
            f"worktree {sibling}\nbranch refs/heads/feature/1900/impl\n"
        )

        shared_git_dir = str(repo_root / ".git")

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                return SimpleNamespace(returncode=0, stdout=shared_git_dir)
            return SimpleNamespace(returncode=128, stdout="")

        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=porcelain))
        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        # The primary checkout (repo_root) must be skipped; the sibling entry is matched.
        assert result.status == "resume"
        assert result.path == str(sibling)

    def test_conventional_path_matching_repo_root_is_ignored(self, monkeypatch, tmp_path):
        """Conventional fallback must not resume the primary checkout path."""
        repo_root = tmp_path / "1900"
        repo_root.mkdir()
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))
        monkeypatch.setattr(
            worktree, "run_git_capture", lambda args, cwd=None: SimpleNamespace(returncode=0, stdout=".git")
        )

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "not_found"
        assert result.path is None

    def test_conventional_path_from_unrelated_repo_is_corrupt(self, monkeypatch, tmp_path):
        """A conventional path that is a valid git repo but from a different origin is corrupt."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        conventional = tmp_path / "1900"
        conventional.mkdir()
        (conventional / ".git").write_text("gitdir: /other/repo/.git/worktrees/1900", encoding="utf-8")
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))

        shared_git_dir = str(repo_root / ".git")

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                # Candidate reports a DIFFERENT common dir — unrelated repo.
                if cwd == str(conventional):
                    return SimpleNamespace(returncode=0, stdout="/other/repo/.git")
                # Main repo reports its own .git.
                return SimpleNamespace(returncode=0, stdout=shared_git_dir)
            return SimpleNamespace(returncode=128, stdout="")

        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == str(conventional)

    def test_conventional_path_corrupt_when_git_common_dir_fails(self, monkeypatch, tmp_path):
        """A conventional path is corrupt when git-common-dir command fails for the candidate."""
        repo_root = tmp_path / "main"
        repo_root.mkdir()
        conventional = tmp_path / "1900"
        conventional.mkdir()
        (conventional / ".git").write_text("gitdir: ../.git/worktrees/1900", encoding="utf-8")
        monkeypatch.setattr(worktree, "run_git_safe", lambda args, cwd=None: SimpleNamespace(stdout=""))

        def fake_run_git_capture(args, cwd=None):
            if args == ["rev-parse", "--git-dir"]:
                return SimpleNamespace(returncode=0, stdout=".git")
            if args == ["rev-parse", "--git-common-dir"]:
                # Simulate the git-common-dir command failing (e.g. corrupt gitdir).
                return SimpleNamespace(returncode=128, stdout="")
            return SimpleNamespace(returncode=128, stdout="")

        monkeypatch.setattr(worktree, "run_git_capture", fake_run_git_capture)

        result = worktree.detect_existing_worktree("#1900", str(repo_root))

        assert result.status == "corrupt"
        assert result.path == str(conventional)
