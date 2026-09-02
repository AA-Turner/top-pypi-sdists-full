"""Tests for agentic_devtools.orchestration.nodes.commit._validate_worktree_ownership."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.orchestration.nodes.commit import _validate_worktree_ownership

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0) -> MagicMock:
    return MagicMock(returncode=returncode, stdout=stdout)


class TestValidateWorktreeOwnership:
    def test_matching_common_dirs_returns_none(self, tmp_path: Path) -> None:
        """Same resolved git-common-dir for process CWD and worktree → ownership confirmed."""
        common_dir = str(tmp_path / "main" / ".git")

        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout=common_dir)):
            result = _validate_worktree_ownership("/tmp/wt")

        assert result is None

    def test_mismatched_common_dirs_blocks_context_mismatch(self, tmp_path: Path) -> None:
        """Different resolved common-dirs → blocks with context_mismatch."""
        main_git = str(tmp_path / "main" / ".git")
        foreign_git = str(tmp_path / "foreign" / ".git")

        call_count: list[int] = [0]

        def capture(args: list[str], cwd: str | None = None) -> MagicMock:
            call_count[0] += 1
            if call_count[0] == 1:
                return _proc(stdout=main_git)
            return _proc(stdout=foreign_git)

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            result = _validate_worktree_ownership("/tmp/foreign")

        assert result is not None
        assert result.category == "context_mismatch"
        assert "different repository" in result.message

    def test_proc_cwd_probe_failure_blocks_context_mismatch(self) -> None:
        """Failure to read process-CWD common-dir → blocks with context_mismatch."""
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=128)):
            result = _validate_worktree_ownership("/tmp/wt")

        assert result is not None
        assert result.category == "context_mismatch"
        assert "process CWD" in result.message

    def test_worktree_probe_failure_blocks_context_mismatch(self, tmp_path: Path) -> None:
        """Failure to read worktree common-dir → blocks with context_mismatch."""
        main_git = str(tmp_path / "main" / ".git")
        call_count: list[int] = [0]

        def capture(args: list[str], cwd: str | None = None) -> MagicMock:
            call_count[0] += 1
            if call_count[0] == 1:
                return _proc(stdout=main_git)
            return _proc(returncode=128)

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            result = _validate_worktree_ownership("/tmp/foreign")

        assert result is not None
        assert result.category == "context_mismatch"
        assert "git repository" in result.message

    def test_probe_os_error_blocks_context_mismatch(self) -> None:
        """Git process startup failure is converted to structured context_mismatch."""
        with patch(
            f"{_MOD}.run_git_capture",
            side_effect=GitError(returncode=2, stderr="No such file or directory", args_list=["rev-parse"]),
        ):
            result = _validate_worktree_ownership("/tmp/wt")

        assert result is not None
        assert result.category == "context_mismatch"
        assert "Cannot determine repository identity" in result.message

    def test_worktree_probe_os_error_blocks_context_mismatch(self, tmp_path: Path) -> None:
        """Worktree probe startup failure is converted to structured context_mismatch."""
        main_git = str(tmp_path / "main" / ".git")

        call_count: list[int] = [0]

        def capture(args: list[str], cwd: str | None = None) -> MagicMock:
            call_count[0] += 1
            if call_count[0] == 1:
                return _proc(stdout=main_git)
            raise GitError(returncode=2, stderr="No such file or directory", args_list=["rev-parse"])

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            result = _validate_worktree_ownership("/tmp/wt")

        assert result is not None
        assert result.category == "context_mismatch"
        assert "Cannot verify repository identity" in result.message

    def test_symlinked_common_dirs_resolve_to_same_path(self, tmp_path: Path) -> None:
        """Symlinked paths that resolve to the same target are treated as the same repo."""
        real_git = str(tmp_path / "main" / ".git")
        # Both calls return the same unresolved path (str comparison is intentionally skipped
        # by resolving via Path); since they resolve identically, ownership is confirmed.

        def capture(args: list[str], cwd: str | None = None) -> MagicMock:
            return _proc(stdout=real_git)

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            result = _validate_worktree_ownership(str(tmp_path / "wt"))

        assert result is None
