"""Lazy registration of default repair factories.

Repair modules are not imported until a factory is actually invoked at
dispatch time, keeping import cost at registration time near zero.
"""

from __future__ import annotations

from ..doctor import RepairFn, RepairRegistry, get_default_registry
from ..fixloop import ErrorClass


def _path_repair_factory() -> RepairFn:
    """Lazily import and return the PATH profile repair function."""
    from .path_repair import repair_path_profile

    return repair_path_profile


def _git_hooks_repair_factory() -> RepairFn:
    """Lazily import and return the git hooks repair function."""
    from .git_hooks_repair import repair_git_hooks

    return repair_git_hooks


def _cert_repair_factory() -> RepairFn:
    """Lazily import and return the cert repair function (with repo root capture)."""
    from ..doctor_repairs import _cert_repair_factory as _factory

    return _factory()


def _cli_repair_factory() -> RepairFn:
    """Lazily import and return the managed CLI repair function."""
    from ..doctor_repairs import _cli_repair_factory as _factory

    return _factory()


def register_default_repairs(registry: RepairRegistry | None = None) -> None:
    """Register all default repair factories into the given registry.

    Args:
        registry: The registry to populate.  Defaults to the process-wide
            default registry from :func:`get_default_registry`.
    """
    if registry is None:
        registry = get_default_registry()

    registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, _path_repair_factory)
    registry.register(ErrorClass.GIT_HOOKS_NOT_CONFIGURED, _git_hooks_repair_factory)
    registry.register(ErrorClass.CERT_CA_FETCH, _cert_repair_factory)
    registry.register(ErrorClass.MANAGED_CLI_MISSING, _cli_repair_factory)
