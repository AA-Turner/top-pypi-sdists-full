"""Discovery package: public entry points and type re-exports."""

from __future__ import annotations

from spec_kitty_tracker.discovery import providers as _providers  # noqa: F401
from spec_kitty_tracker.discovery.registry import (
    get_resource_discoverer,
    get_workspace_discoverer,
)
from spec_kitty_tracker.discovery._validation import (
    validate_resource_result,
    validate_workspace_result,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.nango import NangoConnectionContext

__all__ = [
    "DiscoveredResource",
    "DiscoveredWorkspace",
    "DiscoveryResult",
    "discover_resources",
    "discover_workspaces",
]


async def discover_workspaces(
    provider: str,
    nango_ctx: NangoConnectionContext,
) -> DiscoveryResult[DiscoveredWorkspace]:
    """Discover workspaces for *provider* via the registered factory.

    The result is validated against the hybrid metadata contract before
    being returned. Raises DiscoveryContractError if the per-provider
    adapter returns discovery data that violates the contract.
    """
    factory = get_workspace_discoverer(provider)
    discoverer = factory(nango_ctx)
    result = await discoverer.discover()
    validate_workspace_result(result)
    return result


async def discover_resources(
    provider: str,
    workspace: DiscoveredWorkspace,
    nango_ctx: NangoConnectionContext,
) -> DiscoveryResult[DiscoveredResource]:
    """Discover resources for *provider* within *workspace*.

    The result is validated against the hybrid metadata contract before
    being returned. Raises DiscoveryContractError if the per-provider
    adapter returns discovery data that violates the contract.
    """
    factory = get_resource_discoverer(provider)
    discoverer = factory(nango_ctx)
    result = await discoverer.discover(workspace)
    validate_resource_result(result)
    return result
