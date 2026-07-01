"""Compatibility shim for workspace discovery.

DEPRECATED: Use ``spec_kitty_tracker.discover_workspaces`` directly.
Import ``DiscoveredWorkspace`` and ``DiscoveryResult`` from the top-level
``spec_kitty_tracker`` package.

This module re-exports the canonical symbols for backward compatibility
only and emits a DeprecationWarning on import. It will not be removed
in a backward-incompatible way without a separate migration mission.
"""

import warnings

from spec_kitty_tracker.discovery.types import DiscoveredWorkspace, DiscoveryResult
from spec_kitty_tracker.discovery import discover_workspaces

warnings.warn(
    "spec_kitty_tracker.workspace_discovery is deprecated. "
    "Use spec_kitty_tracker.discover_workspaces instead, and import "
    "DiscoveredWorkspace and DiscoveryResult from the top-level "
    "spec_kitty_tracker package.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "DiscoveredWorkspace",
    "DiscoveryResult",
    "discover_workspaces",
]
