"""Tests for repair_managed_cli — managed CLI installation repair."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor_repairs import repair_managed_cli


def _cli_dep(name: str, found: bool = False) -> DependencyStatus:
    return DependencyStatus(name=name, found=found, required=False)


class TestRepairManagedCliGh:
    """repair_managed_cli handles gh CLI installation."""

    @patch("agentic_devtools.cli.setup.gh_cli_installer.get_gh_cli_binary", return_value="/tmp/gh")
    @patch("agentic_devtools.cli.setup.gh_cli_installer.install_gh_cli", return_value=True)
    def test_gh_missing_calls_install(self, mock_install: MagicMock, mock_get_binary: MagicMock) -> None:
        """Missing gh → install_gh_cli called and dep.path updated from discovered binary."""
        dep = _cli_dep("gh")
        repair_managed_cli(dep)

        mock_install.assert_called_once_with(force=False, dry_run=False)
        mock_get_binary.assert_called_once_with()
        assert dep.found is True
        assert dep.path == "/tmp/gh"

    @patch("agentic_devtools.cli.setup.gh_cli_installer.install_gh_cli", return_value=False)
    def test_gh_install_returns_false_raises(self, mock_install: MagicMock) -> None:
        """install_gh_cli returning False → RuntimeError raised."""
        dep = _cli_dep("gh")
        with pytest.raises(RuntimeError, match="gh CLI installation returned failure"):
            repair_managed_cli(dep)

    @patch(
        "agentic_devtools.cli.setup.gh_cli_installer.install_gh_cli",
        side_effect=OSError("network error"),
    )
    def test_gh_install_exception_reraised(self, mock_install: MagicMock) -> None:
        """install_gh_cli raising exception → RuntimeError with context."""
        dep = _cli_dep("gh")
        with pytest.raises(RuntimeError, match="Failed to install gh CLI"):
            repair_managed_cli(dep)

    @patch("agentic_devtools.cli.setup.gh_cli_installer.get_gh_cli_binary", return_value=None)
    @patch("agentic_devtools.cli.setup.gh_cli_installer.install_gh_cli", return_value=True)
    def test_gh_install_without_discoverable_binary_raises(
        self,
        mock_install: MagicMock,
        mock_get_binary: MagicMock,
    ) -> None:
        """Successful installer result still fails when gh is not discoverable afterwards."""
        dep = _cli_dep("gh")
        with pytest.raises(RuntimeError, match="gh CLI installation succeeded but binary was not found"):
            repair_managed_cli(dep)

        mock_install.assert_called_once_with(force=False, dry_run=False)
        mock_get_binary.assert_called_once_with()


class TestRepairManagedCliCopilot:
    """repair_managed_cli handles copilot CLI installation."""

    @patch("agentic_devtools.cli.setup.copilot_cli_installer.get_copilot_cli_binary", return_value="/tmp/copilot")
    @patch("agentic_devtools.cli.setup.copilot_cli_installer.install_copilot_cli", return_value=True)
    def test_copilot_missing_calls_install(self, mock_install: MagicMock, mock_get_binary: MagicMock) -> None:
        """Missing copilot → install_copilot_cli called and dep.path updated."""
        dep = _cli_dep("copilot")
        repair_managed_cli(dep)

        mock_install.assert_called_once_with(force=False, dry_run=False)
        mock_get_binary.assert_called_once_with()
        assert dep.found is True
        assert dep.path == "/tmp/copilot"

    @patch("agentic_devtools.cli.setup.copilot_cli_installer.install_copilot_cli", return_value=False)
    def test_copilot_install_returns_false_raises(self, mock_install: MagicMock) -> None:
        """install_copilot_cli returning False → RuntimeError."""
        dep = _cli_dep("copilot")
        with pytest.raises(RuntimeError, match="copilot CLI installation returned failure"):
            repair_managed_cli(dep)

    @patch(
        "agentic_devtools.cli.setup.copilot_cli_installer.install_copilot_cli",
        side_effect=OSError("download failed"),
    )
    def test_copilot_install_exception_reraised(self, mock_install: MagicMock) -> None:
        """install_copilot_cli exception → RuntimeError with context."""
        dep = _cli_dep("copilot")
        with pytest.raises(RuntimeError, match="Failed to install copilot CLI"):
            repair_managed_cli(dep)

    @patch("agentic_devtools.cli.setup.copilot_cli_installer.get_copilot_cli_binary", return_value=None)
    @patch("agentic_devtools.cli.setup.copilot_cli_installer.install_copilot_cli", return_value=True)
    def test_copilot_install_without_discoverable_binary_raises(
        self,
        mock_install: MagicMock,
        mock_get_binary: MagicMock,
    ) -> None:
        """Successful installer result still fails when copilot is not discoverable afterwards."""
        dep = _cli_dep("copilot")
        with pytest.raises(
            RuntimeError,
            match="copilot CLI installation succeeded but binary was not found",
        ):
            repair_managed_cli(dep)

        mock_install.assert_called_once_with(force=False, dry_run=False)
        mock_get_binary.assert_called_once_with()


class TestRepairManagedCliUnknown:
    """repair_managed_cli raises ValueError for unknown dep names."""

    def test_unknown_name_raises_value_error(self) -> None:
        """Unknown dep.name raises ValueError."""
        dep = _cli_dep("node")
        with pytest.raises(ValueError, match="Unknown managed CLI"):
            repair_managed_cli(dep)

    def test_git_raises_value_error(self) -> None:
        """'git' is not a managed CLI → ValueError."""
        dep = _cli_dep("git")
        with pytest.raises(ValueError, match="Unknown managed CLI"):
            repair_managed_cli(dep)
