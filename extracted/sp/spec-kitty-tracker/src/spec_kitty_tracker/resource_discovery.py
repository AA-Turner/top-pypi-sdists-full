"""Compatibility shim for resource discovery.

DEPRECATED: Use ``spec_kitty_tracker.discover_resources`` directly.
Import ``DiscoveredResource`` and ``DiscoveryResult`` from the top-level
``spec_kitty_tracker`` package.

This module re-exports the canonical symbols for backward compatibility
only and emits a DeprecationWarning on import. It will not be removed
in a backward-incompatible way without a separate migration mission.
"""

import warnings

from spec_kitty_tracker.discovery import discover_resources
from spec_kitty_tracker.discovery.types import DiscoveredResource, DiscoveryResult

warnings.warn(
    "spec_kitty_tracker.resource_discovery is deprecated. "
    "Use spec_kitty_tracker.discover_resources instead, and import "
    "DiscoveredResource and DiscoveryResult from the top-level "
    "spec_kitty_tracker package.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "DiscoveredResource",
    "DiscoveryResult",
    "discover_resources",
]
