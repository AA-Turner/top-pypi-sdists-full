"""Tests for _locate_and_run."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.autorun import (
    _AUTORUN_MARKER,
    _PHASE_NAME,
    _TARGET_REPO_ROOT_ENV,
    _locate_and_run,
)
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


def _write_managed_script(script_root: Path) -> Path:
    """Write a valid managed root entry-point script under *script_root*."""
    script = script_root / ROOT_ENTRY_POINT_FILENAME
    script.write_text(f"{ORCHESTRATOR_MARKER}\n# managed script content\n", encoding="utf-8")
    return script


class TestLocateAndRunSuccess:
    """A valid managed entry-point is invoked and recorded as success."""

    def test_invokes_script_and_sets_recursion_marker(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()
        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _locate_and_run(tmp_path, report)

        mock_run.assert_called_once()
        # The child env carries the recursion guard marker.
        _, kwargs = mock_run.call_args
        assert kwargs["env"][_AUTORUN_MARKER] == "1"
        assert kwargs["env"]["PYTHONUNBUFFERED"] == "1"
        assert report.phases[0].status == "success"
        assert report.phases[0].name == _PHASE_NAME

    def test_sets_target_repo_root_env_when_provided(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()
        mock_result = MagicMock()
        mock_result.returncode = 0
        target_repo_root = Path("/tmp/user-checkout")

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run:
            _locate_and_run(tmp_path, report, target_repo_root=target_repo_root)

        _, kwargs = mock_run.call_args
        assert kwargs["env"][_TARGET_REPO_ROOT_ENV] == str(target_repo_root)


class TestLocateAndRunEntryPointValidation:
    """Missing, unreadable, or legacy entry-points are skipped."""

    def test_skips_when_script_missing(self, tmp_path: Path) -> None:
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _locate_and_run(tmp_path, report)

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "missing" in (report.phases[0].error or "")

    def test_skips_when_legacy_script(self, tmp_path: Path) -> None:
        (tmp_path / ROOT_ENTRY_POINT_FILENAME).write_text("# no marker here\n", encoding="utf-8")
        report = _make_report()

        with patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run:
            _locate_and_run(tmp_path, report)

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "legacy" in (report.phases[0].error or "")

    def test_skips_when_unreadable_oserror(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()

        with (
            patch("pathlib.Path.read_text", side_effect=OSError("permission denied")),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _locate_and_run(tmp_path, report)

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "unreadable" in (report.phases[0].error or "")

    def test_skips_when_non_utf8_content(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()
        err = UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

        with (
            patch("pathlib.Path.read_text", side_effect=err),
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
        ):
            _locate_and_run(tmp_path, report)

        mock_run.assert_not_called()
        assert report.phases[0].status == "skipped"
        assert "non-UTF-8" in (report.phases[0].error or "")


class TestLocateAndRunFailure:
    """Child-process failures are recorded as a failed phase."""

    def test_records_failure_on_called_process_error(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=subprocess.CalledProcessError(3, "setup-dev-tools.py"),
        ):
            _locate_and_run(tmp_path, report)

        assert report.phases[0].status == "failed"
        assert "code 3" in (report.phases[0].error or "")

    def test_records_failure_on_oserror(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=OSError("exec failed"),
        ):
            _locate_and_run(tmp_path, report)

        assert report.phases[0].status == "failed"
        assert "OS error" in (report.phases[0].error or "")

    def test_records_failure_on_unexpected_exception(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()

        with patch(
            "agentic_devtools.cli.setup.autorun.run_safe",
            side_effect=RuntimeError("boom"),
        ):
            _locate_and_run(tmp_path, report)

        assert report.phases[0].status == "failed"
        assert "Unexpected error" in (report.phases[0].error or "")

    def test_records_failure_on_nonzero_returncode(self, tmp_path: Path) -> None:
        _write_managed_script(tmp_path)
        report = _make_report()
        mock_result = MagicMock()
        mock_result.returncode = 2

        with patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result):
            _locate_and_run(tmp_path, report)

        assert report.phases[0].status == "failed"
        assert "code 2" in (report.phases[0].error or "")
