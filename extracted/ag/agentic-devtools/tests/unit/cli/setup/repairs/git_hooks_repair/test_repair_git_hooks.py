"""Tests for repair_git_hooks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    PRESERVED_MESSAGE_PREFIX,
    PRESERVED_MESSAGE_SUFFIX,
)
from agentic_devtools.cli.setup.repairs.git_hooks_repair import repair_git_hooks


def _make_run_result(returncode: int = 0, stdout: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


class TestRepairGitHooksApplied:
    """repair_git_hooks configures hooks when not set."""

    def test_configures_hooks_and_returns_true(self, tmp_path: Path) -> None:
        """When hooks not configured, calls setup_git_hooks and returns True."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_call_count = 0

        def mock_run(args, **kwargs):
            nonlocal config_call_count
            if "show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                config_call_count += 1
                if config_call_count == 1:
                    return _make_run_result(1, "")  # not configured (pre-repair)
                return _make_run_result(0, ".githooks\n")  # verified (post-repair)
            return _make_run_result(0, "")

        with (
            patch("agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run", side_effect=mock_run),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  ✓ core.hooksPath set to '.githooks'",
            ),
        ):
            result = repair_git_hooks(dep)

        assert result is True
        assert dep.found is True


class TestRepairGitHooksNoop:
    """repair_git_hooks returns False when already configured."""

    def test_returns_false_when_already_configured(self, tmp_path: Path) -> None:
        """When hooks configured to .githooks with dir present, returns False."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_result = _make_run_result(0, ".githooks\n")

        def mock_run(args, **kwargs):
            if "show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                return config_result
            return _make_run_result(0, "")

        with patch("agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run", side_effect=mock_run):
            result = repair_git_hooks(dep)

        assert result is False
        assert dep.found is True


class TestRepairGitHooksGitMissing:
    """repair_git_hooks raises when git is not found."""

    def test_raises_on_git_not_found(self) -> None:
        """When git binary is not available, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=FileNotFoundError("git not found"),
        ):
            with pytest.raises(RuntimeError, match="git binary not found"):
                repair_git_hooks(dep)

    def test_raises_on_git_toplevel_timeout(self) -> None:
        """When git rev-parse times out, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="git", timeout=10),
        ):
            with pytest.raises(RuntimeError, match="timed out"):
                repair_git_hooks(dep)


class TestRepairGitHooksNotInRepo:
    """repair_git_hooks raises when not in a git repo."""

    def test_raises_not_in_repo(self) -> None:
        """When not inside a git repository, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            return_value=_make_run_result(128, ""),
        ):
            with pytest.raises(RuntimeError, match="Not inside a git repository"):
                repair_git_hooks(dep)


class TestRepairGitHooksSetupFails:
    """repair_git_hooks raises when setup_git_hooks returns failure."""

    def test_raises_on_setup_failure(self, tmp_path: Path) -> None:
        """When setup_git_hooks returns a failure message, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_result = _make_run_result(1, "")

        def mock_run(args, **kwargs):
            if "show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                return config_result
            return _make_run_result(0, "")

        with (
            patch("agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run", side_effect=mock_run),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  ⚠ Failed to set core.hooksPath: error",
            ),
        ):
            with pytest.raises(RuntimeError, match="Failed to set core.hooksPath"):
                repair_git_hooks(dep)


class TestRepairGitHooksSetupReturnsNone:
    """repair_git_hooks raises when setup_git_hooks returns None."""

    def test_raises_on_none_return(self, tmp_path: Path) -> None:
        """When setup_git_hooks returns None (no git context), raises."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_result = _make_run_result(1, "")

        def mock_run(args, **kwargs):
            if "show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                return config_result
            return _make_run_result(0, "")

        with (
            patch("agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run", side_effect=mock_run),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value=None,
            ),
        ):
            with pytest.raises(RuntimeError, match="No git context"):
                repair_git_hooks(dep)


class TestRepairGitHooksPostCheckFails:
    """repair_git_hooks raises when .githooks dir missing after success."""

    def test_raises_on_post_check_failure(self, tmp_path: Path) -> None:
        """When setup succeeds but .githooks dir doesn't exist, raises."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)
        # Note: NOT creating .githooks dir

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_result = _make_run_result(1, "")

        def mock_run(args, **kwargs):
            if "--show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                return config_result
            return _make_run_result(0, "")

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  \u2713 core.hooksPath set to '.githooks'",
            ),
        ):
            with pytest.raises(RuntimeError, match="does not exist"):
                repair_git_hooks(dep)


class TestRepairGitHooksPostVerifyConfigMismatch:
    """repair_git_hooks raises when core.hooksPath not set to .githooks after repair."""

    def test_raises_when_config_not_set_after_repair(self, tmp_path: Path) -> None:
        """When .githooks dir exists but core.hooksPath still wrong, raises."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_call_count = 0

        def mock_run(args, **kwargs):
            nonlocal config_call_count
            if "--show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                config_call_count += 1
                if config_call_count == 1:
                    return _make_run_result(1, "")  # not configured pre-repair
                return _make_run_result(1, "")  # still not set post-repair

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  \u2713 core.hooksPath set to '.githooks'",
            ),
        ):
            with pytest.raises(RuntimeError, match="Post-verification failed"):
                repair_git_hooks(dep)

    def test_raises_when_config_set_to_wrong_value(self, tmp_path: Path) -> None:
        """When core.hooksPath is set to a different value after repair, raises."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_call_count = 0

        def mock_run(args, **kwargs):
            nonlocal config_call_count
            if "--show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                config_call_count += 1
                if config_call_count == 1:
                    return _make_run_result(1, "")  # not configured pre-repair
                return _make_run_result(0, ".git/hooks\n")  # wrong value post-repair

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  \u2713 core.hooksPath set to '.githooks'",
            ),
        ):
            with pytest.raises(RuntimeError, match="Post-verification failed"):
                repair_git_hooks(dep)

    def test_raises_when_post_verify_times_out(self, tmp_path: Path) -> None:
        """When post-verification git config call times out, raises RuntimeError."""
        hooks_dir = tmp_path / ".githooks"
        hooks_dir.mkdir()
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        config_call_count = 0

        def mock_run(args, **kwargs):
            nonlocal config_call_count
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                config_call_count += 1
                if config_call_count == 1:
                    return _make_run_result(1, "")  # not configured pre-repair
                raise subprocess.TimeoutExpired(cmd="git", timeout=10)

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value="  \u2713 core.hooksPath set to '.githooks'",
            ),
        ):
            with pytest.raises(RuntimeError, match="Post-verification failed"):
                repair_git_hooks(dep)


class TestRepairGitHooksConfigCheckFileNotFound:
    """repair_git_hooks raises when git config check hits FileNotFoundError."""

    def test_raises_on_config_check_file_not_found(self, tmp_path: Path) -> None:
        """When git config --get raises FileNotFoundError, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call: git rev-parse --show-toplevel succeeds
                return _make_run_result(0, str(tmp_path) + "\n")
            # Second call: git config --get fails with FileNotFoundError
            raise FileNotFoundError("git not found")

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=mock_run,
        ):
            with pytest.raises(RuntimeError, match="git binary not found"):
                repair_git_hooks(dep)

    def test_raises_on_config_check_timeout(self, tmp_path: Path) -> None:
        """When git config --get times out, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        call_count = 0

        def mock_run(args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return _make_run_result(0, str(tmp_path) + "\n")
            raise subprocess.TimeoutExpired(cmd="git", timeout=10)

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=mock_run,
        ):
            with pytest.raises(RuntimeError, match="timed out"):
                repair_git_hooks(dep)


class TestRepairGitHooksSetupGitHooksFileNotFound:
    """repair_git_hooks raises when setup_git_hooks raises FileNotFoundError."""

    def test_raises_on_setup_git_hooks_file_not_found(self, tmp_path: Path) -> None:
        """When setup_git_hooks raises FileNotFoundError, raises RuntimeError."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        toplevel_result = _make_run_result(0, str(tmp_path) + "\n")
        config_result = _make_run_result(1, "")

        def mock_run(args, **kwargs):
            if "--show-toplevel" in args:
                return toplevel_result
            if "core.hooksPath" in args:
                return config_result
            return _make_run_result(0, "")

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                side_effect=FileNotFoundError("git not found"),
            ),
        ):
            with pytest.raises(RuntimeError, match="git binary not found"):
                repair_git_hooks(dep)


def _write_project_config(git_root: Path, payload: dict[str, object]) -> None:
    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload), encoding="utf-8")


class TestRepairGitHooksEmptyConfiguredValue:
    """repair_git_hooks preserves an explicitly-configured empty core.hooksPath."""

    def test_preserves_empty_hooks_path(self, tmp_path: Path, capsys) -> None:
        """returncode=0 with empty stdout must not overwrite core.hooksPath."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)
        calls: list[list[str]] = []

        def mock_run(args, **kwargs):
            calls.append(list(args))
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(0, "")  # explicitly set to empty
            return _make_run_result(0, "")

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=mock_run,
        ):
            result = repair_git_hooks(dep)

        assert result is False
        assert dep.found is True
        # Must not write (no git config without --get)
        assert [c for c in calls if c[:2] == ["git", "config"] and "--get" not in c] == []
        assert not (tmp_path / ".githooks").exists()
        assert PRESERVED_MESSAGE_PREFIX in capsys.readouterr().out


class TestRepairGitHooksForeignPathPreserved:
    """repair_git_hooks preserves a hooks path owned by another tool."""

    def test_preserves_foreign_hooks_path(self, tmp_path: Path, capsys) -> None:
        """A foreign core.hooksPath is left alone: no write, no RuntimeError, no-op."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)
        calls: list[list[str]] = []

        def mock_run(args, **kwargs):
            calls.append(list(args))
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(0, ".husky/_\n")
            return _make_run_result(0, "")

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=mock_run,
        ):
            result = repair_git_hooks(dep)

        assert result is False
        assert dep.found is True
        assert [c for c in calls if c[:2] == ["git", "config"] and "--get" not in c] == []
        assert not (tmp_path / ".githooks").exists()

        out = capsys.readouterr().out
        assert PRESERVED_MESSAGE_PREFIX in out
        assert "'.husky/_'" in out
        assert PRESERVED_MESSAGE_SUFFIX in out


class TestRepairGitHooksDisabledByConfig:
    """repair_git_hooks is a no-op when manage_git_hooks is false."""

    def test_skips_when_disabled(self, tmp_path: Path, capsys) -> None:
        """The toggle short-circuits before core.hooksPath is even read."""
        _write_project_config(tmp_path, {"manage_git_hooks": False})
        dep = DependencyStatus(name="git-hooks", found=False, required=True)
        calls: list[list[str]] = []

        def mock_run(args, **kwargs):
            calls.append(list(args))
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            return _make_run_result(0, "")

        with patch(
            "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
            side_effect=mock_run,
        ):
            result = repair_git_hooks(dep)

        assert result is False
        assert dep.found is True
        assert all("core.hooksPath" not in c for c in calls)
        assert not (tmp_path / ".githooks").exists()
        assert HOOKS_DISABLED_MESSAGE in capsys.readouterr().out


class TestRepairGitHooksSetupDeclinedToWrite:
    """repair_git_hooks skips post-verification when setup_git_hooks declined."""

    def test_returns_false_when_setup_declined(self, tmp_path: Path, capsys) -> None:
        """A non-write message from setup_git_hooks must not trip the post-checks."""
        dep = DependencyStatus(name="git-hooks", found=False, required=True)

        def mock_run(args, **kwargs):
            if "--show-toplevel" in args:
                return _make_run_result(0, str(tmp_path) + "\n")
            if "core.hooksPath" in args:
                return _make_run_result(1, "")
            return _make_run_result(0, "")

        with (
            patch(
                "agentic_devtools.cli.setup.repairs.git_hooks_repair.subprocess.run",
                side_effect=mock_run,
            ),
            patch(
                "agentic_devtools.cli.setup.script_generators.required_setup.setup_git_hooks",
                return_value=HOOKS_DISABLED_MESSAGE,
            ),
        ):
            result = repair_git_hooks(dep)

        assert result is False
        assert dep.found is True
        assert HOOKS_DISABLED_MESSAGE in capsys.readouterr().out
