"""Tests for _autorun_setup_dev_tools."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.autorun import _AUTORUN_MARKER, _autorun_setup_dev_tools
from agentic_devtools.cli.setup.phase_markers import EXECUTION_END, EXECUTION_START
from agentic_devtools.cli.setup.report import SetupReport
from agentic_devtools.cli.setup.script_generators.constants import (
    ORCHESTRATOR_MARKER,
    ROOT_ENTRY_POINT_FILENAME,
)


def _make_report() -> SetupReport:
    return SetupReport(
        schema_version=1,
        timestamp="2026-01-01T00:00:00+00:00",
        exit_code=0,
        exit_code_name="OK",
    )


def _write_managed_script(git_root: Path) -> Path:
    """Write a valid managed root entry-point script."""
    script = git_root / ROOT_ENTRY_POINT_FILENAME
    script.write_text(f"{ORCHESTRATOR_MARKER}\n# managed script content\n", encoding="utf-8")
    return script


def _make_worktree_run_git(*, add_returncode: int = 0, write_script: bool = True):
    """Return a fake ``run_git`` for the ``_run_from_created_branch`` worktree flow.

    On ``worktree add`` it creates the target directory and (optionally) writes a
    managed script into it, so the subsequent ``_locate_and_run`` finds a valid
    entry-point. All calls are recorded on ``.calls`` for assertions.
    """
    calls: list[tuple[str, ...]] = []

    def _fake_run_git(*args: str, check: bool = True) -> MagicMock:
        calls.append(args)
        result = MagicMock()
        result.stderr = "boom" if add_returncode != 0 else ""
        if args[:2] == ("worktree", "add"):
            result.returncode = add_returncode
            if add_returncode == 0:
                worktree_dir = Path(args[3])
                worktree_dir.mkdir(parents=True, exist_ok=True)
                if write_script:
                    _write_managed_script(worktree_dir)
        else:
            result.returncode = 0
        return result

    _fake_run_git.calls = calls  # type: ignore[attr-defined]
    return _fake_run_git


class TestAutorunSetupDevToolsSuccess:
    """Tests for the happy-path invocation."""

    def test_invokes_script_with_correct_args_and_env(self, tmp_path: Path) -> None:
        """run_safe is called with correct argv, shell=False, check=True, and marker env."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_called_once()
        call_kwargs = mock_run.call_args
        args = call_kwargs[0][0]
        assert args == [sys.executable, str(tmp_path / ROOT_ENTRY_POINT_FILENAME), "--foreground"]
        assert call_kwargs[1]["shell"] is False
        assert call_kwargs[1]["check"] is True
        assert call_kwargs[1]["env"][_AUTORUN_MARKER] == "1"

    def test_records_success_phase_result(self, tmp_path: Path) -> None:
        """report.record() is called with a success PhaseResult."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert len(report.phases) == 1
        assert report.phases[0].name == "autorun_setup"
        assert report.phases[0].status == "success"

    def test_prints_success_to_stdout(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Success message is printed to stdout."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert "Autorun complete" in captured.out
        assert captured.err == ""

    def test_parent_env_unchanged_after_success(self, tmp_path: Path) -> None:
        """Parent environment does not contain the marker after the helper returns."""
        _write_managed_script(tmp_path)
        report = _make_report()

        # Ensure marker is NOT set before
        env_backup = None
        if _AUTORUN_MARKER in __import__("os").environ:
            env_backup = __import__("os").environ.pop(_AUTORUN_MARKER)

        mock_result = MagicMock()
        mock_result.returncode = 0

        try:
            with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
                _autorun_setup_dev_tools(
                    autorun_enabled=True,
                    git_root=tmp_path,
                    system_only=False,
                    skip_repo_steps=False,
                    report=report,
                )

            assert _AUTORUN_MARKER not in __import__("os").environ
        finally:
            if env_backup is not None:
                __import__("os").environ[_AUTORUN_MARKER] = env_backup


class TestAutorunSetupDevToolsRecursionGuard:
    """Tests for recursion guard behavior."""

    def test_skips_when_marker_present_in_env(self, tmp_path: Path) -> None:
        """run_safe is not called when AGDT_SETUP_AUTORUN is already set."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch.dict("os.environ", {_AUTORUN_MARKER: "1"}),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()

    def test_records_skip_reason_for_recursion(self, tmp_path: Path) -> None:
        """PhaseResult with status=skipped is recorded for recursion guard."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch.dict("os.environ", {_AUTORUN_MARKER: "1"}):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert len(report.phases) == 1
        assert report.phases[0].status == "skipped"
        assert "Recursion guard" in (report.phases[0].error or "")

    def test_prints_diagnostic_to_stderr(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Diagnostic message is printed to stderr."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch.dict("os.environ", {_AUTORUN_MARKER: "1"}):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert "recursion guard" in captured.err.lower()

    def test_no_stdout_on_skip(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Nothing is printed to stdout on recursion skip."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch.dict("os.environ", {_AUTORUN_MARKER: "1"}):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_guard_fires_when_marker_is_empty_string(self, tmp_path: Path) -> None:
        """Guard fires on any defined value, including empty string."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch.dict("os.environ", {_AUTORUN_MARKER: ""}),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "Recursion guard" in (report.phases[0].error or "")


class TestAutorunSetupDevToolsSkipConditions:
    """Tests for skip conditions (FR-003)."""

    def test_skips_when_autorun_disabled(self, tmp_path: Path) -> None:
        """run_safe is not called when autorun_enabled is False."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=False,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "autorun_enabled" in (report.phases[0].error or "")

    def test_skips_when_git_root_none(self) -> None:
        """run_safe is not called when git_root is None."""
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=None,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "git_root" in (report.phases[0].error or "")

    def test_skips_when_system_only(self, tmp_path: Path) -> None:
        """run_safe is not called when system_only is True."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=True,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "system-only" in (report.phases[0].error or "")

    def test_skips_when_skip_repo_steps(self, tmp_path: Path) -> None:
        """run_safe is not called when skip_repo_steps is True."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=True,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "skip_repo_steps" in (report.phases[0].error or "")

    def test_records_skip_reason_for_each_condition(self, tmp_path: Path) -> None:
        """Each skip condition records the correct skip reason."""
        _write_managed_script(tmp_path)
        conditions = [
            {"autorun_enabled": False, "git_root": tmp_path, "system_only": False, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": None, "system_only": False, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": tmp_path, "system_only": True, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": tmp_path, "system_only": False, "skip_repo_steps": True},
        ]
        expected_reasons = ["autorun_enabled", "git_root", "system-only", "skip_repo_steps"]

        for kwargs, expected in zip(conditions, expected_reasons):
            report = _make_report()
            with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
                _autorun_setup_dev_tools(report=report, **kwargs)  # type: ignore[arg-type]
            mock_run.assert_not_called()
            assert expected in (report.phases[0].error or "")

    def test_prints_to_stderr_for_each_skip(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Each skip condition prints a message to stderr."""
        _write_managed_script(tmp_path)
        conditions = [
            {"autorun_enabled": False, "git_root": tmp_path, "system_only": False, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": None, "system_only": False, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": tmp_path, "system_only": True, "skip_repo_steps": False},
            {"autorun_enabled": True, "git_root": tmp_path, "system_only": False, "skip_repo_steps": True},
        ]

        for kwargs in conditions:
            report = _make_report()
            with patch("agentic_devtools.cli.setup.autorun.run_safe"):
                _autorun_setup_dev_tools(report=report, **kwargs)  # type: ignore[arg-type]
            captured = capsys.readouterr()
            assert "skipped" in captured.err.lower()
            assert captured.out == ""


class TestAutorunSetupDevToolsEntryPointValidation:
    """Tests for entry-point validation (FR-004)."""

    def test_skips_when_script_missing(self, tmp_path: Path) -> None:
        """Skips when setup-dev-tools.py does not exist."""
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "missing" in (report.phases[0].error or "").lower()

    def test_skips_when_script_is_legacy_no_marker(self, tmp_path: Path) -> None:
        """Skips when script exists but has no orchestrator marker."""
        script = tmp_path / ROOT_ENTRY_POINT_FILENAME
        script.write_text("# legacy script\nprint('hello')\n", encoding="utf-8")
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "legacy" in (report.phases[0].error or "").lower()

    def test_skips_when_script_unreadable(self, tmp_path: Path) -> None:
        """Skips when script exists but is unreadable."""
        script = tmp_path / ROOT_ENTRY_POINT_FILENAME
        script.write_text("content", encoding="utf-8")
        report = _make_report()

        with patch.object(Path, "read_text", side_effect=OSError("Permission denied")):
            with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
                _autorun_setup_dev_tools(
                    autorun_enabled=True,
                    git_root=tmp_path,
                    system_only=False,
                    skip_repo_steps=False,
                    report=report,
                )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "unreadable" in (report.phases[0].error or "").lower()

    def test_skips_when_script_non_utf8(self, tmp_path: Path) -> None:
        """Skips when script has non-UTF-8 content."""
        script = tmp_path / ROOT_ENTRY_POINT_FILENAME
        script.write_bytes(b"\xff\xfe invalid utf-8")
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "utf-8" in (report.phases[0].error or "").lower()

    def test_proceeds_when_script_has_orchestrator_marker(self, tmp_path: Path) -> None:
        """Proceeds to invocation when script has the orchestrator marker."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"


class TestAutorunSetupDevToolsFailure:
    """Tests for failure handling (FR-005)."""

    def test_catches_called_process_error(self, tmp_path: Path) -> None:
        """CalledProcessError is caught and recorded as failed."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(1, "cmd"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].status == "failed"

    def test_catches_os_error(self, tmp_path: Path) -> None:
        """OSError is caught and recorded as failed."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=OSError("No such file"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].status == "failed"
        assert "OS error" in (report.phases[0].error or "")

    def test_catches_generic_exception(self, tmp_path: Path) -> None:
        """Generic Exception is caught and recorded as failed."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=RuntimeError("Something went wrong"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].status == "failed"
        assert "Unexpected error" in (report.phases[0].error or "")

    def test_records_failed_status_with_error_message(self, tmp_path: Path) -> None:
        """Failed status includes an error message."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(42, "cmd"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].error is not None
        assert "42" in report.phases[0].error

    def test_prints_failure_to_stderr(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Failure message is printed to stderr."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(1, "cmd"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert "failed" in captured.err.lower()
        # stdout carries only the phase markers — the failure text is stderr-only.
        assert "failed" not in captured.out.lower()

    def test_handles_negative_returncode(self, tmp_path: Path) -> None:
        """Negative returncode from run_safe is treated as failure."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = -1

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].status == "failed"
        assert "-1" in (report.phases[0].error or "")

    def test_does_not_propagate_exception(self, tmp_path: Path) -> None:
        """Exceptions are caught; the function returns normally."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=RuntimeError("boom"),
        ):
            # Should not raise
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        assert report.phases[0].status == "failed"


class TestAutorunBranchCreatedSkip:
    """Tests for branch-created skip path (PR-workflow interaction)."""

    def test_skip_when_branch_created_non_empty_string(self, tmp_path: Path) -> None:
        """Autorun is skipped when branch_created is a non-empty string."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )

        mock_run.assert_not_called()
        assert len(report.phases) == 1
        assert report.phases[0].status == "skipped"
        error = report.phases[0].error or ""
        assert "chore/agdt-setup-1.0" in error
        assert "review & merge the setup PR" in error
        assert "python setup-dev-tools.py" in error
        assert "\n" not in error

    def test_stderr_diagnostic_emitted(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """stderr contains remediation substrings when branch_created is set."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe"):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )

        captured = capsys.readouterr()
        assert "review & merge the setup PR" in captured.err
        assert "python setup-dev-tools.py" in captured.err

    def test_autorun_disabled_takes_precedence(self, tmp_path: Path) -> None:
        """autorun_enabled=False fires before branch_created check."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=False,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        error = report.phases[0].error or ""
        assert "autorun_enabled" in error
        assert "branch" not in error.lower()

    def test_recursion_guard_takes_precedence(self, tmp_path: Path) -> None:
        """AGDT_SETUP_AUTORUN env wins over branch_created."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch.dict("os.environ", {_AUTORUN_MARKER: "1"}),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        error = report.phases[0].error or ""
        assert "Recursion guard" in error
        assert "branch" not in error.lower()

    def test_proceeds_when_branch_created_none(self, tmp_path: Path) -> None:
        """Autorun proceeds normally when branch_created is None."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created=None,
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"

    def test_proceeds_when_branch_created_empty_string(self, tmp_path: Path) -> None:
        """Empty string is treated as falsy — autorun proceeds."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="",
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"


class TestAutorunWorkflowSuppression:
    """Tests for workflow-state suppression of auto-run."""

    def test_skips_when_scaffolding_workflow_is_active(self, tmp_path: Path) -> None:
        """An active scaffolding workflow step suppresses auto-run."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'work-on-jira-issue' workflow is at the 'setup' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_not_called()
        assert len(report.phases) == 1
        assert report.phases[0].status == "skipped"
        error = report.phases[0].error or ""
        assert "work-on-jira-issue" in error
        assert "setup" in error
        assert "python setup-dev-tools.py" in error

    def test_skip_message_goes_to_stdout(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """The workflow-suppression skip message is informational (stdout)."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'pull-request-review' workflow is at the 'initiate' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert "pull-request-review" in captured.out
        assert "python setup-dev-tools.py" in captured.out
        assert captured.err == ""

    def test_explicit_run_overrides_suppression(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """--run overrides workflow suppression and warns on stderr instead of skipping."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'work-on-jira-issue' workflow is at the 'setup' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                explicit_run=True,
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"
        captured = capsys.readouterr()
        assert "--run" in captured.err
        assert "work-on-jira-issue" in captured.err
        assert "setup" in captured.err
        assert "Auto-run skipped" not in captured.out

    def test_recursion_guard_is_not_overridable_by_explicit_run(self, tmp_path: Path) -> None:
        """--run never defeats the recursion guard."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch.dict("os.environ", {_AUTORUN_MARKER: "1"}),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                explicit_run=True,
            )

        mock_run.assert_not_called()
        assert "Recursion guard" in (report.phases[0].error or "")

    def test_explicit_run_overrides_branch_created_skip(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--run overrides branch-created suppression and runs from the created branch worktree."""
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0
        fake_run_git = _make_worktree_run_git()

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
                explicit_run=True,
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"
        # The worktree is added for the created branch and removed afterwards.
        assert ("worktree", "add", "--detach") == fake_run_git.calls[0][:3]
        assert fake_run_git.calls[0][4] == "chore/agdt-setup-1.0"
        assert any(call[:2] == ("worktree", "remove") for call in fake_run_git.calls)
        captured = capsys.readouterr()
        assert "--run" in captured.err
        assert "chore/agdt-setup-1.0" in captured.err

    def test_explicit_run_branch_created_worktree_add_fails(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When the worktree checkout fails, the phase is recorded as failed and nothing runs."""
        report = _make_report()
        fake_run_git = _make_worktree_run_git(add_returncode=1)

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
                explicit_run=True,
            )

        mock_run.assert_not_called()
        assert report.phases[0].status == "failed"
        assert "chore/agdt-setup-1.0" in (report.phases[0].error or "")
        # No worktree remove is attempted when the add failed.
        assert all(call[:2] != ("worktree", "remove") for call in fake_run_git.calls)
        assert "could not check out branch" in capsys.readouterr().err

    def test_proceeds_when_no_workflow_suppression(self, tmp_path: Path) -> None:
        """No suppression reason → auto-run proceeds normally."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason", return_value=None),
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run,
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"


class TestAutorunPhaseMarkers:
    """Tests for the execution phase markers emitted around the child process."""

    def test_markers_bracket_successful_execution(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """execution:start and execution:end bracket a successful auto-run."""
        _write_managed_script(tmp_path)
        report = _make_report()

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        out = capsys.readouterr().out
        assert EXECUTION_START in out
        assert EXECUTION_END in out
        assert out.index(EXECUTION_START) < out.index(EXECUTION_END)

    def test_end_marker_emitted_when_child_fails(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """execution:end is emitted even when the child process raises."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(3, "setup-dev-tools.py"),
        ):
            _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        out = capsys.readouterr().out
        assert EXECUTION_START in out
        assert EXECUTION_END in out
        assert report.phases[0].status == "failed"

    def test_no_execution_markers_when_skipped(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Skipped auto-run emits neither execution marker."""
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe"):
            _autorun_setup_dev_tools(
                autorun_enabled=False,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )

        captured = capsys.readouterr()
        assert EXECUTION_START not in captured.out + captured.err
        assert EXECUTION_END not in captured.out + captured.err


class TestAutorunReturnValue:
    """Tests for the bool return value of _autorun_setup_dev_tools."""

    def test_returns_false_when_disabled(self, tmp_path: Path) -> None:
        """Returns False when autorun_enabled is False (child not invoked)."""
        report = _make_report()
        result = _autorun_setup_dev_tools(
            autorun_enabled=False,
            git_root=tmp_path,
            system_only=False,
            skip_repo_steps=False,
            report=report,
        )
        assert result is False

    def test_returns_false_when_branch_created_no_explicit(self, tmp_path: Path) -> None:
        """Returns False when branch_created suppresses and no --run override."""
        report = _make_report()
        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )
        mock_run.assert_not_called()
        assert result is False

    def test_returns_false_when_workflow_suppressed(self, tmp_path: Path) -> None:
        """Returns False when workflow suppression fires (child not invoked)."""
        _write_managed_script(tmp_path)
        report = _make_report()
        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'work-on-jira-issue' workflow is at the 'setup' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )
        mock_run.assert_not_called()
        assert result is False

    def test_returns_false_when_entrypoint_validation_skips(self, tmp_path: Path) -> None:
        """Returns False when entry-point validation skips before child invocation."""
        report = _make_report()
        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )
        mock_run.assert_not_called()
        assert result is False

    def test_returns_true_when_child_invoked_successfully(self, tmp_path: Path) -> None:
        """Returns True when the child process was invoked and succeeded."""
        _write_managed_script(tmp_path)
        report = _make_report()
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )
        assert result is True

    def test_returns_true_when_child_fails(self, tmp_path: Path) -> None:
        """Returns True even when the child process fails (it was invoked)."""
        _write_managed_script(tmp_path)
        report = _make_report()
        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(3, "setup-dev-tools.py"),
        ):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
            )
        assert result is True

    def test_returns_false_when_worktree_add_fails(self, tmp_path: Path) -> None:
        """Returns False when --run + branch_created but worktree creation fails."""
        report = _make_report()
        fake_run_git = _make_worktree_run_git(add_returncode=1)
        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
                explicit_run=True,
            )
        mock_run.assert_not_called()
        assert result is False


class TestAutorunSuppressionOrdering:
    """branch_created suppression takes precedence over workflow suppression."""

    def test_branch_created_suppression_takes_precedence_for_non_explicit(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When both suppressions are active, non-explicit run gets the merge-and-rerun hint."""
        _write_managed_script(tmp_path)
        report = _make_report()
        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'work-on-jira-issue' workflow is at the 'setup' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
            )

        mock_run.assert_not_called()
        assert result is False
        # The branch-created remediation hint (review & merge) must appear, not
        # the workflow-step hint ("manually once the workflow step is complete").
        err = capsys.readouterr().err
        assert "review" in err.lower() and "merge" in err.lower()
        assert "chore/agdt-setup-1.0" in err
        assert "manually once the workflow step is complete" not in err

    def test_explicit_run_with_both_suppressions_emits_all_warnings(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When both suppressions apply and --run is set, both warnings are printed."""
        report = _make_report()
        mock_result = MagicMock()
        mock_result.returncode = 0
        fake_run_git = _make_worktree_run_git()
        with (
            patch(
                "agentic_devtools.cli.setup.autorun.get_workflow_suppression_reason",
                return_value="the 'work-on-jira-issue' workflow is at the 'setup' step",
            ),
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            result = _autorun_setup_dev_tools(
                autorun_enabled=True,
                git_root=tmp_path,
                system_only=False,
                skip_repo_steps=False,
                report=report,
                branch_created="chore/agdt-setup-1.0",
                explicit_run=True,
            )

        assert result is True
        err = capsys.readouterr().err
        # Both warnings must be present.
        assert "work-on-jira-issue" in err
        assert "chore/agdt-setup-1.0" in err
        assert "--run" in err
