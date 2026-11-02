"""Tests for register_stale_install_repair."""

from unittest.mock import MagicMock

from agentic_devtools.cli.setup.commands import register_stale_install_repair
from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestRegisterStaleInstallRepair:
    """Tests for register_stale_install_repair helper."""

    def test_registers_factory(self) -> None:
        registry = MagicMock()
        register_stale_install_repair(registry)
        registry.register.assert_called_once()
        call_args = registry.register.call_args
        assert call_args[0][0] is ErrorClass.STALE_PARTIAL_INSTALL

    def test_factory_does_not_import_doctor_repair_at_registration(self) -> None:
        """doctor_repair module is not imported during registration."""
        import sys

        registry = MagicMock()
        # Remove from cache if present.
        sys.modules.pop("agentic_devtools.cli.setup.doctor_repair", None)
        register_stale_install_repair(registry)
        # doctor_repair should NOT have been imported.
        assert "agentic_devtools.cli.setup.doctor_repair" not in sys.modules

    def test_factory_invocation_imports_repair_fn(self) -> None:
        """Factory invocation lazily imports doctor_repair."""
        registry = MagicMock()
        register_stale_install_repair(registry)
        factory = registry.register.call_args[0][1]
        fn = factory()
        from agentic_devtools.cli.setup.doctor_repair import repair_corrupted_artifacts

        assert fn is repair_corrupted_artifacts
