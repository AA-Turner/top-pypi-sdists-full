"""Tests for _check_git_hooks_config."""

from __future__ import annotations

import io
import json
import subprocess
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.dependency_checker import _check_git_hooks_config, print_dependency_report


def _make_run_result(returncode: int = 0, stdout: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


class TestCheckGitHooksConfigured:
    """_check_git_hooks_config returns found=True when configured."""

    def test_hooks_configured_and_dir_exists(self, tmp_path: Path) -> None:
        """hooksPath=.githooks and .githooks dir exists → found=True."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(0, "true\n")
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(0, ".githooks\n")
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is True
        assert status.name == "git-hooks"
        assert status.required is True


class TestCheckGitHooksNotInRepo:
    """_check_git_hooks_config returns required=False outside git repo."""

    def test_not_in_git_repo(self) -> None:
        """Not in a git repo → found=False, required=False."""

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(128, "")
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


class TestCheckGitHooksGitMissing:
    """_check_git_hooks_config returns required=False when git unavailable."""

    def test_git_not_found(self) -> None:
        """git binary not found → found=False, required=False."""
        with patch("subprocess.run", side_effect=FileNotFoundError("git")):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


class TestCheckGitHooksNotConfigured:
    """_check_git_hooks_config returns found=False when not configured."""

    def test_in_repo_but_hooks_not_set(self, tmp_path: Path) -> None:
        """In git repo but hooksPath not set → found=False, required=True."""

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(0, "true\n")
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(1, "")  # Not configured
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is True

    def test_hooks_set_but_dir_missing(self, tmp_path: Path) -> None:
        """hooksPath=.githooks but .githooks dir doesn't exist → found=False."""

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(0, "true\n")
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(0, ".githooks\n")
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is True


class TestCheckGitHooksToplevelNonZero:
    """_check_git_hooks_config handles non-zero exit from show-toplevel."""

    def test_toplevel_nonzero_is_non_blocking(self) -> None:
        """Non-zero exit from --show-toplevel → found=False, required=False (non-blocking)."""

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(0, "true\n")
            if "--show-toplevel" in args:
                return _make_run_result(128, "")  # e.g. bare repo / detached HEAD
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


class TestCheckGitHooksTimeout:
    """_check_git_hooks_config handles subprocess timeout."""

    def test_timeout_returns_not_required(self) -> None:
        """Timeout → found=False, required=False."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="git", timeout=10)):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


class TestCheckGitHooksToplevelFailure:
    """_check_git_hooks_config handles failure on show-toplevel call."""

    def test_toplevel_file_not_found(self) -> None:
        """FileNotFoundError on --show-toplevel → found=False, required=False (non-blocking)."""
        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call: --is-inside-work-tree succeeds
                return _make_run_result(0, "true\n")
            # Second call: --show-toplevel fails
            raise FileNotFoundError("git")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"

    def test_toplevel_timeout(self) -> None:
        """TimeoutExpired on --show-toplevel → found=False, required=False (non-blocking)."""
        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return _make_run_result(0, "true\n")
            raise subprocess.TimeoutExpired(cmd="git", timeout=10)

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


class TestCheckGitHooksConfigGetFailure:
    """_check_git_hooks_config handles failure on config --get call."""

    def test_config_get_file_not_found(self, tmp_path: Path) -> None:
        """FileNotFoundError on config --get → found=False, required=False (non-blocking)."""
        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return _make_run_result(0, "true\n")
            if call_count == 2:
                return _make_run_result(0, str(tmp_path) + "\n")
            raise FileNotFoundError("git")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"

    def test_config_get_timeout(self, tmp_path: Path) -> None:
        """TimeoutExpired on config --get → found=False, required=False (non-blocking)."""
        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return _make_run_result(0, "true\n")
            if call_count == 2:
                return _make_run_result(0, str(tmp_path) + "\n")
            raise subprocess.TimeoutExpired(cmd="git", timeout=10)

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is False
        assert status.category == "Optional — only inside a git repository"


def _write_project_config(git_root: Path, payload: dict[str, object]) -> None:
    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload), encoding="utf-8")


def _mock_run_factory(git_root: Path, hooks_path: str):
    def mock_run(args, **kwargs):
        if "--is-inside-work-tree" in args:
            return _make_run_result(0, "true\n")
        if "--show-toplevel" in args:
            return _make_run_result(0, str(git_root) + "\n")
        if "core.hooksPath" in args:
            if hooks_path:
                return _make_run_result(0, hooks_path + "\n")
            return _make_run_result(1, "")
        return _make_run_result(0, "")

    return mock_run


class TestCheckGitHooksEmptyConfiguredValue:
    """An explicitly-configured empty core.hooksPath is treated as externally managed."""

    def test_empty_value_is_non_blocking(self, tmp_path: Path) -> None:
        """returncode=0 + empty stdout is a set key, not an absent key."""

        def mock_run(args, **kwargs):
            if "--is-inside-work-tree" in args:
                return _make_run_result(0, "true\n")
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(0, "")  # explicitly configured as empty
            return _make_run_result(0, "")

        with patch("subprocess.run", side_effect=mock_run):
            status = _check_git_hooks_config()

        assert status.found is True
        assert status.required is False
        assert status.path == "(empty)"
        assert status.install_hint == ""
        assert status.category == "Optional — core.hooksPath is managed outside agentic-devtools"


class TestCheckGitHooksForeignPath:
    """A hooks path owned by another tool is preserved and non-blocking."""

    def test_foreign_path_is_non_blocking(self, tmp_path: Path) -> None:
        """hooksPath=.husky/_ → found=True, required=False, no install hint."""
        with patch("subprocess.run", side_effect=_mock_run_factory(tmp_path, ".husky/_")):
            status = _check_git_hooks_config()

        assert status.found is True
        assert status.required is False
        assert status.path == ".husky/_"
        assert status.install_hint == ""
        assert status.category == "Optional — core.hooksPath is managed outside agentic-devtools"

    def test_report_line_is_not_misleading(self, tmp_path: Path) -> None:
        """The rendered line must not claim the dependency is missing."""
        with patch("subprocess.run", side_effect=_mock_run_factory(tmp_path, ".husky/_")):
            status = _check_git_hooks_config()

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_dependency_report([status])
        rendered = buffer.getvalue()

        assert "Install: run: agdt-setup-check --fix" not in rendered
        assert "❌ git-hooks" not in rendered
        assert "✅ git-hooks" in rendered
        assert "Optional — core.hooksPath is managed outside agentic-devtools" in rendered


class TestCheckGitHooksDisabledByConfig:
    """manage_git_hooks=false makes the check non-blocking."""

    def test_disabled_with_existing_value(self, tmp_path: Path) -> None:
        """Reports the current value and never blocks."""
        _write_project_config(tmp_path, {"manage_git_hooks": False})

        with patch("subprocess.run", side_effect=_mock_run_factory(tmp_path, ".husky/_")):
            status = _check_git_hooks_config()

        assert status.found is True
        assert status.required is False
        assert status.path == ".husky/_"
        assert status.install_hint == ""
        assert status.category == "Optional — hooks management disabled by manage_git_hooks"

    def test_disabled_with_unset_value(self, tmp_path: Path) -> None:
        """An unset hooksPath renders a placeholder location instead of blocking."""
        _write_project_config(tmp_path, {"manage_git_hooks": False})

        with patch("subprocess.run", side_effect=_mock_run_factory(tmp_path, "")):
            status = _check_git_hooks_config()

        assert status.found is True
        assert status.required is False
        assert status.path == "(not configured)"
        assert status.category == "Optional — hooks management disabled by manage_git_hooks"

    def test_enabled_toggle_keeps_legacy_behaviour(self, tmp_path: Path) -> None:
        """manage_git_hooks=true with an unset hooksPath still blocks (R8)."""
        _write_project_config(tmp_path, {"manage_git_hooks": True})

        with patch("subprocess.run", side_effect=_mock_run_factory(tmp_path, "")):
            status = _check_git_hooks_config()

        assert status.found is False
        assert status.required is True
        assert status.install_hint == "run: agdt-setup-check --fix"
        assert status.category == "Required"
