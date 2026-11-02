"""Tests for write_report function."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.report import REPORT_PATH, make_report, write_report


class TestWriteReport:
    """write_report happy path, dir creation, atomic write, and failure handling."""

    def test_happy_path_writes_valid_json(self, tmp_path: Path) -> None:
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path):
            result = write_report(report)

        assert result is True
        assert report_path.exists()
        data = json.loads(report_path.read_text())
        assert data["exit_code"] == 0
        assert data["exit_code_name"] == "OK"
        assert data["schema_version"] == 1

    def test_creates_directory_if_missing(self, tmp_path: Path) -> None:
        report_path = tmp_path / "new_dir" / "report.json"
        report = make_report(exit_code=10)

        with patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path):
            result = write_report(report)

        assert result is True
        assert report_path.parent.exists()

    def test_dir_chmod_failure_is_silent(self, tmp_path: Path) -> None:
        """chmod hardening failure is silently ignored and does not warn."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with (
            patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path),
            patch("pathlib.Path.chmod", side_effect=OSError("permission denied")),
        ):
            result = write_report(report)

        assert result is True
        assert report_path.exists()

    def test_write_failure_returns_false_and_warns(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Directory-creation or file-write failure warns to stderr."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with (
            patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path),
            patch(
                "agentic_devtools.cli.setup.report.atomic_write",
                side_effect=OSError("disk full"),
            ),
        ):
            result = write_report(report)

        assert result is False
        captured = capsys.readouterr()
        assert "agdt-setup: failed to write setup report to" in captured.err
        assert "OSError: disk full" in captured.err

    def test_atomic_write_no_partial_file(self, tmp_path: Path) -> None:
        """Atomic write ensures no partial file is visible."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path):
            write_report(report)

        # Verify no temp files left behind
        parent = report_path.parent
        tmp_files = [f for f in parent.iterdir() if f.suffix == ".tmp"]
        assert len(tmp_files) == 0

    def test_report_path_default(self) -> None:
        """REPORT_PATH points to ~/.agdt/last-setup-report.json."""
        assert REPORT_PATH == Path.home() / ".agdt" / "last-setup-report.json"

    def test_skips_chmod_on_windows(self, tmp_path: Path) -> None:
        """On Windows (os.name == 'nt'), chmod is not called."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with (
            patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path),
            patch("agentic_devtools.cli.setup.report.os.name", "nt"),
            patch("pathlib.Path.chmod") as mock_chmod,
        ):
            result = write_report(report)

        assert result is True
        mock_chmod.assert_not_called()

    def test_replace_failure_cleans_temp_file(self, tmp_path: Path) -> None:
        """When atomic_write fails, write returns False and no temp file remains."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report_path.parent.mkdir(parents=True)
        report = make_report(exit_code=0)

        with (
            patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path),
            patch(
                "agentic_devtools.cli.setup.report.atomic_write",
                side_effect=OSError("cross-device"),
            ),
        ):
            result = write_report(report)

        assert result is False

    def test_baseexception_reraised(self, tmp_path: Path) -> None:
        """BaseException subclasses are re-raised after cleanup."""
        report_path = tmp_path / ".agdt" / "last-setup-report.json"
        report = make_report(exit_code=0)

        with (
            patch("agentic_devtools.cli.setup.report.REPORT_PATH", report_path),
            patch(
                "agentic_devtools.cli.setup.report.atomic_write",
                side_effect=KeyboardInterrupt,
            ),
            pytest.raises(KeyboardInterrupt),
        ):
            write_report(report)
