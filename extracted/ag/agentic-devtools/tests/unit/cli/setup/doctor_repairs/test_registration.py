"""Tests for repair factory registration — cert and managed CLI factories."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import RepairRegistry, run_doctor
from agentic_devtools.cli.setup.fixloop import ErrorClass
from agentic_devtools.cli.setup.repairs.registration import register_default_repairs


def _dep(name: str, *, required: bool, found: bool) -> DependencyStatus:
    return DependencyStatus(name=name, found=found, required=required)


class TestRepairRegistration:
    """register_default_repairs registers cert and CLI repair factories."""

    def test_cert_ca_fetch_registered(self) -> None:
        """CERT_CA_FETCH has a registered factory after registration."""
        registry = RepairRegistry()
        register_default_repairs(registry)
        assert registry.get(ErrorClass.CERT_CA_FETCH) is not None

    def test_managed_cli_missing_registered(self) -> None:
        """MANAGED_CLI_MISSING has a registered factory after registration."""
        registry = RepairRegistry()
        register_default_repairs(registry)
        assert registry.get(ErrorClass.MANAGED_CLI_MISSING) is not None

    def test_path_profile_still_registered(self) -> None:
        """PATH_PROFILE_NOT_UPDATED is still registered (backward compat)."""
        registry = RepairRegistry()
        register_default_repairs(registry)
        assert registry.get(ErrorClass.PATH_PROFILE_NOT_UPDATED) is not None

    def test_git_hooks_still_registered(self) -> None:
        """GIT_HOOKS_NOT_CONFIGURED is still registered (backward compat)."""
        registry = RepairRegistry()
        register_default_repairs(registry)
        assert registry.get(ErrorClass.GIT_HOOKS_NOT_CONFIGURED) is not None


class TestRegistrationFactoryDelegation:
    """Wrapper factories in registration.py delegate to doctor_repairs."""

    @patch("agentic_devtools.cli.setup.doctor_repairs._cert_repair_factory")
    def test_cert_factory_delegates_to_doctor_repairs(
        self,
        mock_inner: MagicMock,
    ) -> None:
        """registration._cert_repair_factory calls doctor_repairs._cert_repair_factory."""
        from agentic_devtools.cli.setup.repairs.registration import (
            _cert_repair_factory,
        )

        sentinel = MagicMock()
        mock_inner.return_value = sentinel
        result = _cert_repair_factory()
        mock_inner.assert_called_once()
        assert result is sentinel

    @patch("agentic_devtools.cli.setup.doctor_repairs._cli_repair_factory")
    def test_cli_factory_delegates_to_doctor_repairs(
        self,
        mock_inner: MagicMock,
    ) -> None:
        """registration._cli_repair_factory calls doctor_repairs._cli_repair_factory."""
        from agentic_devtools.cli.setup.repairs.registration import (
            _cli_repair_factory,
        )

        sentinel = MagicMock()
        mock_inner.return_value = sentinel
        result = _cli_repair_factory()
        mock_inner.assert_called_once()
        assert result is sentinel


class TestAllHealthyNoOp:
    """When all components are healthy, no repair functions are called."""

    def test_all_healthy_fix_mode_no_repairs(self) -> None:
        """All deps found + --fix → zero repairs dispatched."""
        registry = RepairRegistry()
        register_default_repairs(registry)

        statuses = [
            _dep("git", required=True, found=True),
            _dep("gh", required=False, found=True),
            _dep("copilot", required=False, found=True),
            _dep("ca-bundle", required=True, found=True),
        ]

        result = run_doctor(statuses, fix=True, registry=registry)
        assert result.report.exit_code == 0
        assert result.repair_outcomes == []
        assert result.problems == []

    def test_all_healthy_check_only_no_problems(self) -> None:
        """All deps found + check-only → exit code 0, no problems."""
        statuses = [
            _dep("git", required=True, found=True),
            _dep("gh", required=False, found=True),
            _dep("copilot", required=False, found=True),
            _dep("ca-bundle", required=True, found=True),
        ]

        result = run_doctor(statuses, fix=False)
        assert result.report.exit_code == 0
        assert result.problems == []


class TestIndependentRepairExecution:
    """Cert failure does not prevent CLI repair and vice versa."""

    @patch("agentic_devtools.cli.setup.repairs.registration._cert_repair_factory")
    @patch("agentic_devtools.cli.setup.repairs.registration._cli_repair_factory")
    def test_cert_failure_does_not_block_cli_repair(
        self,
        mock_cli_factory: MagicMock,
        mock_cert_factory: MagicMock,
    ) -> None:
        """Cert repair failure does not prevent managed CLI repair."""

        # Cert repair raises, CLI repair succeeds.
        def cert_raises(dep: DependencyStatus) -> None:
            raise RuntimeError("cert fetch failed")

        def cli_succeeds(dep: DependencyStatus) -> None:
            dep.found = True

        mock_cert_factory.return_value = cert_raises
        mock_cli_factory.return_value = cli_succeeds

        registry = RepairRegistry()
        registry.register(ErrorClass.CERT_CA_FETCH, mock_cert_factory)
        registry.register(ErrorClass.MANAGED_CLI_MISSING, mock_cli_factory)

        statuses = [
            _dep("ca-bundle", required=True, found=False),
            _dep("gh", required=False, found=False),
        ]

        result = run_doctor(statuses, fix=True, registry=registry)

        # Both repairs were attempted.
        assert len(result.repair_outcomes) == 2
        cert_outcome = next(o for o in result.repair_outcomes if o.dependency.name == "ca-bundle")
        cli_outcome = next(o for o in result.repair_outcomes if o.dependency.name == "gh")
        assert cert_outcome.success is False
        assert cli_outcome.success is True
