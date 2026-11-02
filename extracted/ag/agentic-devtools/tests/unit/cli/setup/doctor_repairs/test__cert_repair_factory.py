"""Tests for _cert_repair_factory and _cli_repair_factory."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.doctor_repairs import (
    _cert_repair_factory,
    _cli_repair_factory,
    repair_managed_cli,
)


class TestCertRepairFactory:
    """_cert_repair_factory captures repo root and returns a RepairFn closure."""

    @patch("agentic_devtools.cli.setup.doctor_repairs.repair_certs")
    @patch("agentic_devtools.state._get_git_repo_root", return_value="/repo")
    def test_returns_callable_that_calls_repair_certs(
        self,
        mock_root: MagicMock,
        mock_repair: MagicMock,
    ) -> None:
        """Factory returns a callable that invokes repair_certs with captured repo_root."""
        fn = _cert_repair_factory()
        dep = MagicMock()
        fn(dep)
        mock_repair.assert_called_once_with(dep, repo_root=Path("/repo"))

    @patch("agentic_devtools.cli.setup.doctor_repairs.repair_certs")
    @patch("agentic_devtools.state._get_git_repo_root", return_value=None)
    def test_falls_back_to_cwd_when_no_git_root(
        self,
        mock_root: MagicMock,
        mock_repair: MagicMock,
    ) -> None:
        """When _get_git_repo_root returns None, falls back to Path.cwd()."""
        fn = _cert_repair_factory()
        dep = MagicMock()
        fn(dep)
        call_args = mock_repair.call_args
        assert call_args is not None
        assert isinstance(call_args.kwargs["repo_root"], Path)


class TestCliRepairFactory:
    """_cli_repair_factory returns repair_managed_cli directly."""

    def test_returns_repair_managed_cli(self) -> None:
        """Factory returns the repair_managed_cli function itself."""
        fn = _cli_repair_factory()
        assert fn is repair_managed_cli
