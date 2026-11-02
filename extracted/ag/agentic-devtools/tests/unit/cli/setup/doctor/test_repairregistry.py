"""Tests for RepairRegistry."""

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import RepairRegistry
from agentic_devtools.cli.setup.fixloop import ErrorClass


def _make_status(name: str = "git", required: bool = True, found: bool = False) -> DependencyStatus:
    return DependencyStatus(name=name, found=found, required=required)


class TestRepairRegistryRegisterAndGet:
    """RepairRegistry.register() stores and .get() retrieves repair factories."""

    def test_register_then_get_returns_factory(self):
        """Registered factory is returned by get() for the same error class."""
        registry = RepairRegistry()
        calls: list[DependencyStatus] = []

        def repair(dep: DependencyStatus) -> None:
            calls.append(dep)

        factory = lambda: repair  # noqa: E731

        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)
        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is factory

    def test_get_returns_none_for_unregistered_class(self):
        """get() returns None when no factory is registered for the class."""
        registry = RepairRegistry()
        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is None

    def test_register_overwrites_previous(self):
        """Re-registering for the same class silently replaces the old factory."""
        registry = RepairRegistry()

        def first(_: DependencyStatus) -> None: ...
        def second(_: DependencyStatus) -> None: ...

        factory_first = lambda: first  # noqa: E731
        factory_second = lambda: second  # noqa: E731

        registry.register(ErrorClass.MISSING_DEPENDENCY, factory_first)
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory_second)
        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is factory_second

    def test_register_multiple_classes(self):
        """Different error classes can each have their own registered factory."""
        registry = RepairRegistry()

        def repair_missing(_: DependencyStatus) -> None: ...
        def repair_stale(_: DependencyStatus) -> None: ...

        factory_missing = lambda: repair_missing  # noqa: E731
        factory_stale = lambda: repair_stale  # noqa: E731

        registry.register(ErrorClass.MISSING_DEPENDENCY, factory_missing)
        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, factory_stale)

        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is factory_missing
        assert registry.get(ErrorClass.STALE_PARTIAL_INSTALL) is factory_stale

    def test_get_unrelated_class_returns_none_after_registration(self):
        """get() returns None for a class that was never registered."""
        registry = RepairRegistry()

        def repair(_: DependencyStatus) -> None: ...

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: repair)
        assert registry.get(ErrorClass.AUTH_SECRET) is None

    def test_factory_not_invoked_at_registration_time(self):
        """The factory callable is NOT invoked when register() is called."""
        registry = RepairRegistry()
        invoked = []

        def factory():
            invoked.append(True)

            def repair(_: DependencyStatus) -> None: ...

            return repair

        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)
        assert invoked == [], "Factory should not be invoked at registration time"


class TestRepairRegistryClear:
    """RepairRegistry.clear() removes all registered factories."""

    def test_clear_empties_registry(self):
        """After clear(), get() returns None for previously registered classes."""
        registry = RepairRegistry()

        def repair(_: DependencyStatus) -> None: ...

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: repair)
        registry.clear()
        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is None

    def test_clear_on_empty_registry_is_safe(self):
        """clear() on an empty registry does not raise."""
        registry = RepairRegistry()
        registry.clear()  # Should not raise

    def test_register_after_clear_works(self):
        """Registry is usable again after clear()."""
        registry = RepairRegistry()

        def repair(_: DependencyStatus) -> None: ...

        factory = lambda: repair  # noqa: E731

        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)
        registry.clear()
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)
        assert registry.get(ErrorClass.MISSING_DEPENDENCY) is factory
