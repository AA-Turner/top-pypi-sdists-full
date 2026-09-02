"""Tests for register_default_repairs."""

from __future__ import annotations

from agentic_devtools.cli.setup.doctor import RepairRegistry
from agentic_devtools.cli.setup.fixloop import ErrorClass
from agentic_devtools.cli.setup.repairs.registration import register_default_repairs


class TestRegisterDefaultRepairs:
    """register_default_repairs registers both factories."""

    def test_registers_path_and_git_hooks_factories(self) -> None:
        """Both ErrorClass keys are registered after calling."""
        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        assert registry.get(ErrorClass.PATH_PROFILE_NOT_UPDATED) is not None
        assert registry.get(ErrorClass.GIT_HOOKS_NOT_CONFIGURED) is not None

    def test_uses_default_registry_when_none(self) -> None:
        """When no registry passed, uses the process-wide default."""
        from agentic_devtools.cli.setup.doctor import get_default_registry

        registry = get_default_registry()
        registry.clear()

        register_default_repairs()

        assert registry.get(ErrorClass.PATH_PROFILE_NOT_UPDATED) is not None
        assert registry.get(ErrorClass.GIT_HOOKS_NOT_CONFIGURED) is not None

        # Cleanup
        registry.clear()


class TestLazyImport:
    """Repair modules are lazily imported only on factory invocation."""

    def test_factory_returns_callable(self) -> None:
        """Factories return callable repair functions."""
        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        path_factory = registry.get(ErrorClass.PATH_PROFILE_NOT_UPDATED)
        hooks_factory = registry.get(ErrorClass.GIT_HOOKS_NOT_CONFIGURED)

        assert path_factory is not None
        assert hooks_factory is not None
        assert callable(path_factory)
        assert callable(hooks_factory)

    def test_path_factory_does_lazy_import(self) -> None:
        """Path factory uses lazy import pattern (from .path_repair)."""
        from unittest.mock import MagicMock, patch

        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        factory = registry.get(ErrorClass.PATH_PROFILE_NOT_UPDATED)
        assert factory is not None

        mock_fn = MagicMock()
        with patch.dict(
            "sys.modules",
            {"agentic_devtools.cli.setup.repairs.path_repair": MagicMock(repair_path_profile=mock_fn)},
        ):
            result = factory()
            assert result is mock_fn

    def test_git_hooks_factory_does_lazy_import(self) -> None:
        """Git hooks factory uses lazy import pattern (from .git_hooks_repair)."""
        from unittest.mock import MagicMock, patch

        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        factory = registry.get(ErrorClass.GIT_HOOKS_NOT_CONFIGURED)
        assert factory is not None

        mock_fn = MagicMock()
        with patch.dict(
            "sys.modules",
            {"agentic_devtools.cli.setup.repairs.git_hooks_repair": MagicMock(repair_git_hooks=mock_fn)},
        ):
            result = factory()
            assert result is mock_fn


class TestCertAndCliFactories:
    """Cert and managed CLI factories delegate to doctor_repairs."""

    def test_cert_factory_registered_and_delegates(self) -> None:
        """CERT_CA_FETCH factory delegates to doctor_repairs._cert_repair_factory."""
        from unittest.mock import MagicMock, patch

        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        factory = registry.get(ErrorClass.CERT_CA_FETCH)
        assert factory is not None

        sentinel = MagicMock()
        with patch(
            "agentic_devtools.cli.setup.doctor_repairs._cert_repair_factory",
            return_value=sentinel,
        ):
            result = factory()
            assert result is sentinel

    def test_cli_factory_registered_and_delegates(self) -> None:
        """MANAGED_CLI_MISSING factory delegates to doctor_repairs._cli_repair_factory."""
        from unittest.mock import MagicMock, patch

        registry = RepairRegistry()
        register_default_repairs(registry=registry)

        factory = registry.get(ErrorClass.MANAGED_CLI_MISSING)
        assert factory is not None

        sentinel = MagicMock()
        with patch(
            "agentic_devtools.cli.setup.doctor_repairs._cli_repair_factory",
            return_value=sentinel,
        ):
            result = factory()
            assert result is sentinel
