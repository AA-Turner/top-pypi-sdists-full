"""Provider discovery registry with fail-fast duplicate protection."""

from __future__ import annotations

from typing import Callable, Protocol, runtime_checkable

from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.nango import NangoConnectionContext


@runtime_checkable
class WorkspaceProviderDiscovery(Protocol):
    """Protocol for per-provider workspace discovery implementations."""

    async def discover(self) -> DiscoveryResult[DiscoveredWorkspace]: ...


@runtime_checkable
class ResourceProviderDiscovery(Protocol):
    """Protocol for per-provider resource discovery implementations."""

    async def discover(
        self, workspace: DiscoveredWorkspace
    ) -> DiscoveryResult[DiscoveredResource]: ...


WorkspaceDiscovererFactory = Callable[[NangoConnectionContext], WorkspaceProviderDiscovery]
ResourceDiscovererFactory = Callable[[NangoConnectionContext], ResourceProviderDiscovery]

_workspace_discoverers: dict[str, WorkspaceDiscovererFactory] = {}
_resource_discoverers: dict[str, ResourceDiscovererFactory] = {}


def register_workspace_discoverer(
    provider: str,
    factory: WorkspaceDiscovererFactory,
    *,
    _allow_override: bool = False,
) -> None:
    """Register a workspace discoverer factory for *provider*.

    Raises ``ConnectorConfigError`` if *provider* is already registered
    and *_allow_override* is ``False``.
    """
    if provider in _workspace_discoverers and not _allow_override:
        raise ConnectorConfigError(f"Duplicate workspace discoverer for provider: {provider}")
    _workspace_discoverers[provider] = factory


def register_resource_discoverer(
    provider: str,
    factory: ResourceDiscovererFactory,
    *,
    _allow_override: bool = False,
) -> None:
    """Register a resource discoverer factory for *provider*.

    Raises ``ConnectorConfigError`` if *provider* is already registered
    and *_allow_override* is ``False``.
    """
    if provider in _resource_discoverers and not _allow_override:
        raise ConnectorConfigError(f"Duplicate resource discoverer for provider: {provider}")
    _resource_discoverers[provider] = factory


def get_workspace_discoverer(provider: str) -> WorkspaceDiscovererFactory:
    """Return the workspace discoverer factory for *provider*.

    Raises ``ConnectorConfigError`` if no factory is registered.
    """
    try:
        return _workspace_discoverers[provider]
    except KeyError:
        raise ConnectorConfigError(f"Unknown provider: {provider}") from None


def get_resource_discoverer(provider: str) -> ResourceDiscovererFactory:
    """Return the resource discoverer factory for *provider*.

    Raises ``ConnectorConfigError`` if no factory is registered.
    """
    try:
        return _resource_discoverers[provider]
    except KeyError:
        raise ConnectorConfigError(f"Unknown provider: {provider}") from None


def registered_workspace_providers() -> frozenset[str]:
    """Return the set of providers with registered workspace discoverers."""
    return frozenset(_workspace_discoverers)


def registered_resource_providers() -> frozenset[str]:
    """Return the set of providers with registered resource discoverers."""
    return frozenset(_resource_discoverers)
