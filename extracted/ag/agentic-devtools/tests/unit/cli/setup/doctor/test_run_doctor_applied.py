"""Tests for run_doctor return-value handling (applied field)."""

from __future__ import annotations

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import RepairRegistry, run_doctor
from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestRunDoctorAppliedField:
    """run_doctor sets applied based on repair function return value."""

    def test_repair_returns_true_sets_applied_true(self) -> None:
        """When repair returns True, outcome.applied is True."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> bool:
            d.found = True
            return True

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is True
        assert result.repair_outcomes[0].applied is True

    def test_repair_returns_false_sets_applied_false(self) -> None:
        """When repair returns False (no-op), outcome.applied is False."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> bool:
            d.found = True
            return False

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is True
        assert result.repair_outcomes[0].applied is False

    def test_repair_returns_none_sets_applied_true(self) -> None:
        """When repair returns None (backward compat), outcome.applied is True."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> None:
            d.found = True
            return None

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is True
        assert result.repair_outcomes[0].applied is True

    def test_repair_raises_sets_applied_false(self) -> None:
        """When repair raises, outcome.applied is False."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> bool:
            raise RuntimeError("boom")

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is False
        assert result.repair_outcomes[0].applied is False

    def test_repair_noop_not_fixed_sets_applied_false(self) -> None:
        """When repair returns True but dep still broken, applied reflects the repair attempt (True)."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> bool:
            # Does NOT set d.found = True
            return True

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is False
        assert result.repair_outcomes[0].applied is True

    def test_no_factory_registered_sets_applied_false(self) -> None:
        """When no factory registered for an error class, outcome.applied is False."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        registry = RepairRegistry()
        # Intentionally do not register a factory for PATH_PROFILE_NOT_UPDATED

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is False
        assert result.repair_outcomes[0].applied is False

    def test_repair_returns_invalid_type_is_treated_as_failure(self) -> None:
        """When repair returns an unexpected type, outcome is a failed repair."""
        dep = DependencyStatus(name="path-profile", found=False, required=True)

        def repair(d: DependencyStatus) -> object:
            d.found = True
            return 0  # invalid — not True/False/None

        registry = RepairRegistry()
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, lambda: repair)  # type: ignore[arg-type, return-value]

        result = run_doctor([dep], fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is False
        assert result.repair_outcomes[0].applied is False
