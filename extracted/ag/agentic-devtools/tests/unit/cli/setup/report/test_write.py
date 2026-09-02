"""Tests for SetupReport.write() method."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.report import REPORT_PATH, PhaseResult, SetupReport


class TestWrite:
    """SetupReport.write() atomic persistence with path resolution."""

    def _make_report(self) -> SetupReport:
        return SetupReport(
            schema_version=1,
            timestamp="2026-01-15T10:00:00+00:00",
            exit_code=0,
            exit_code_name="OK",
            phases=[PhaseResult(name="test", status="success")],
            details={},
            mode="setup",
            git_root="/tmp/repo",
        )

    def test_write_success_returns_true(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        result = report.write(path=target)
        assert result is True
        assert target.exists()
        data = json.loads(target.read_text())
        assert data["schema_version"] == 1
        assert data["exit_code"] == 0

    def test_write_creates_parent_directory(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "deep" / "nested" / "dir" / "report.json"
        result = report.write(path=target)
        assert result is True
        assert target.exists()

    def test_write_env_override_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        env_target = tmp_path / "env-report.json"
        monkeypatch.setenv("AGDT_SETUP_REPORT_PATH", str(env_target))
        report = self._make_report()
        result = report.write()
        assert result is True
        assert env_target.exists()

    def test_write_explicit_path_argument(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "explicit.json"
        result = report.write(path=target)
        assert result is True
        assert target.exists()

    def test_write_precedence_explicit_over_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        env_target = tmp_path / "env.json"
        explicit_target = tmp_path / "explicit.json"
        monkeypatch.setenv("AGDT_SETUP_REPORT_PATH", str(env_target))
        report = self._make_report()
        result = report.write(path=explicit_target)
        assert result is True
        assert explicit_target.exists()
        assert not env_target.exists()

    def test_write_expands_user_in_env_override_path(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.setenv("AGDT_SETUP_REPORT_PATH", "~/env-report.json")
        report = self._make_report()
        result = report.write()
        assert result is True
        assert (tmp_path / "env-report.json").exists()

    def test_write_does_not_chmod_override_directory(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "shared" / "report.json"
        with patch("pathlib.Path.chmod") as mock_chmod:
            result = report.write(path=target)
        assert result is True
        mock_chmod.assert_not_called()

    def test_write_failure_returns_false_stderr_format(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        with patch(
            "agentic_devtools.cli.setup.report.atomic_write",
            side_effect=OSError("disk full"),
        ):
            result = report.write(path=target)
        assert result is False
        captured = capsys.readouterr()
        assert f"agdt-setup: failed to write setup report to {target}: OSError: disk full" in captured.err

    def test_write_failure_no_partial_file(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        with patch(
            "agentic_devtools.cli.setup.report.atomic_write",
            side_effect=OSError("disk full"),
        ):
            report.write(path=target)
        assert not target.exists()

    def test_write_baseexception_reraised(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        with (
            patch(
                "agentic_devtools.cli.setup.report.atomic_write",
                side_effect=KeyboardInterrupt,
            ),
            pytest.raises(KeyboardInterrupt),
        ):
            report.write(path=target)

    def test_write_chmod_skipped_on_windows(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        with (
            patch("agentic_devtools.cli.setup.report.os.name", "nt"),
            patch("pathlib.Path.chmod") as mock_chmod,
        ):
            result = report.write(path=target)
        assert result is True
        mock_chmod.assert_not_called()

    def test_write_chmod_failure_silent(self, tmp_path: Path) -> None:
        report = self._make_report()
        target = tmp_path / "report.json"
        with patch("pathlib.Path.chmod", side_effect=OSError("permission denied")):
            result = report.write(path=target)
        assert result is True
        assert target.exists()

    def test_write_default_path(self) -> None:
        """Default path is ~/.agdt/last-setup-report.json."""
        assert REPORT_PATH == Path.home() / ".agdt" / "last-setup-report.json"
