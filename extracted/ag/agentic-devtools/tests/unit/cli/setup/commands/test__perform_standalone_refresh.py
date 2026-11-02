"""Tests for the _perform_standalone_refresh helper."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.commands import _perform_standalone_refresh
from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome


def _args(**overrides: object) -> argparse.Namespace:
    """Build a minimal argparse.Namespace for the standalone-refresh helper."""
    defaults: dict[str, object] = {"skip_platform_detection": False}
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class TestPerformStandaloneRefresh:
    """Branch coverage for _perform_standalone_refresh."""

    def test_skip_platform_detection(self, tmp_path: Path, capsys) -> None:
        """--skip-platform-detection → skipped(skip_platform_detection), debug log only."""
        outcome = _perform_standalone_refresh(
            _args(skip_platform_detection=True), tmp_path, dry_run=False, skip_repo_steps=False
        )
        assert outcome == RefreshOutcome.skipped("skip_platform_detection")
        assert capsys.readouterr().out == ""

    def test_skip_platform_detection_dry_run(self, tmp_path: Path, capsys) -> None:
        """--skip-platform-detection with dry_run prints the would-skip line."""
        outcome = _perform_standalone_refresh(
            _args(skip_platform_detection=True), tmp_path, dry_run=True, skip_repo_steps=False
        )
        assert outcome.reason == "skip_platform_detection"
        assert "skipped (--skip-platform-detection)" in capsys.readouterr().out

    def test_missing_git_root(self, capsys) -> None:
        """git_root=None → skipped(missing_git_root), stderr warning."""
        outcome = _perform_standalone_refresh(_args(), None, dry_run=False, skip_repo_steps=False)
        assert outcome == RefreshOutcome.skipped("missing_git_root")
        assert "not inside a git repository" in capsys.readouterr().err

    def test_missing_git_root_dry_run(self, capsys) -> None:
        """git_root=None dry_run prints the would-skip line."""
        outcome = _perform_standalone_refresh(_args(), None, dry_run=True, skip_repo_steps=False)
        assert outcome.reason == "missing_git_root"
        assert "skipped (no git root)" in capsys.readouterr().out

    def test_force_old_version(self, tmp_path: Path, capsys) -> None:
        """skip_repo_steps=True → skipped(force_old_version), stderr warning."""
        outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=True)
        assert outcome == RefreshOutcome.skipped("force_old_version")
        assert "file modifications are disabled" in capsys.readouterr().err

    def test_force_old_version_dry_run(self, tmp_path: Path, capsys) -> None:
        """skip_repo_steps=True dry_run prints the would-skip line."""
        outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=True, skip_repo_steps=True)
        assert outcome.reason == "force_old_version"
        assert "skipped (--force-old-version)" in capsys.readouterr().out

    def test_missing_config(self, tmp_path: Path, capsys) -> None:
        """No agdt-config.json → skipped(missing_config), stderr warning."""
        outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=False)
        assert outcome == RefreshOutcome.skipped("missing_config")
        assert "no platform configuration found" in capsys.readouterr().err

    def test_missing_config_dry_run(self, tmp_path: Path, capsys) -> None:
        """No agdt-config.json dry_run prints the would-skip line."""
        outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=True, skip_repo_steps=False)
        assert outcome.reason == "missing_config"
        assert "skipped (no platform configuration)" in capsys.readouterr().out

    def test_dry_run_would_refresh(self, tmp_path: Path, capsys) -> None:
        """Config present + dry_run → skipped(dry_run), prints would-refresh line."""
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")
        outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=True, skip_repo_steps=False)
        assert outcome == RefreshOutcome.skipped("dry_run")
        assert "would refresh issue types" in capsys.readouterr().out

    def test_discovery_success(self, tmp_path: Path) -> None:
        """Config present, not dry_run → delegates to discover_issue_types, returns its outcome."""
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")
        with patch(
            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
            return_value=RefreshOutcome.success(),
        ) as mock_discover:
            outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=False)
        assert outcome.status == "success"
        mock_discover.assert_called_once_with(tmp_path, force_refresh=True, standalone=True)

    def test_discovery_failed_prints_warning(self, tmp_path: Path, capsys) -> None:
        """A failed discovery outcome prints the failure warning to stderr."""
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")
        with patch(
            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
            return_value=RefreshOutcome.failed("provider_unreachable", "boom"),
        ):
            outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=False)
        assert outcome.status == "failed"
        assert "Issue type refresh failed (boom)" in capsys.readouterr().err

    def test_discovery_unexpected_exception_returns_failed(self, tmp_path: Path, capsys) -> None:
        """An unexpected exception from discovery is caught → failed(unexpected_error), exit-safe."""
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")
        with patch(
            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
            side_effect=RuntimeError("kaboom"),
        ):
            outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=False)
        assert outcome.status == "failed"
        assert outcome.reason == "unexpected_error"
        assert outcome.error == "kaboom"
        assert "Issue type refresh failed (kaboom)" in capsys.readouterr().err

    def test_discovery_empty_message_exception_falls_back_to_type_name(self, tmp_path: Path, capsys) -> None:
        """An exception with an empty message falls back to the type name so failed() never raises."""
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")
        with patch(
            "agentic_devtools.cli.setup.issue_type_discovery.discover_issue_types",
            side_effect=RuntimeError(),
        ):
            outcome = _perform_standalone_refresh(_args(), tmp_path, dry_run=False, skip_repo_steps=False)
        assert outcome.status == "failed"
        assert outcome.reason == "unexpected_error"
        assert outcome.error == "RuntimeError"
        assert "RuntimeError" in capsys.readouterr().err
