from __future__ import annotations

from typing import Literal

from connector_sdk_types.generated.capability_levels import CAPABILITY_LEVELS

__all__ = ["get_capability_level_from_name"]


def get_capability_level_from_name(capability_name: str) -> Literal["read", "write"]:
    """Return 'read' or 'write' for a capability name. Defaults to 'write' for custom capabilities."""
    return CAPABILITY_LEVELS.get(capability_name, "write")
