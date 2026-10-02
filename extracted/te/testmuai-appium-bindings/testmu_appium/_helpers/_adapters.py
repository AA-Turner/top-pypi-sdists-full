"""Platform-keyed operation-adapter registries.

One registry per operation domain (gestures, key dispatch, deeplinks, ...), each
a data table: platform family → operation name → adapter callable. Domain
modules declare their rows at import time; a row may be declared empty, meaning
the platform is a known family whose operations are all unshipped, so every
lookup on it raises ``UnsupportedOnPlatform`` naming the feature. Activating a
platform for a domain is filling its row — call sites resolve through
``adapter()`` and never change.
"""
from typing import Callable, Mapping, Optional

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform

#: registry name → platform family → operation name → adapter callable.
_REGISTRIES: dict[str, dict[str, dict[str, Callable]]] = {}


def register(registry: str, rows: Mapping[str, Mapping[str, Callable]]) -> None:
    """Declare a registry's platform rows; repeated calls merge per platform.

    An empty mapping still declares its row — the platform family is known and
    none of the domain's operations are shipped for it.
    """
    table = _REGISTRIES.setdefault(registry, {})
    for platform, operations in rows.items():
        table.setdefault(str(platform).lower(), {}).update(operations)


def adapter(
    registry: str, operation: str, feature: str, *, platform: Optional[str] = None
) -> Callable:
    """The adapter for one operation on the given (default: configured) platform.

    Args:
        registry: The operation domain's registry name.
        operation: The operation's row entry name.
        feature: Human-readable feature name carried by the raise.
        platform: Platform family; defaults to the configured platform.

    Raises:
        UnsupportedOnPlatform: the registry has no row for the platform, or the
            platform's row has no entry for the operation.
    """
    resolved = (_config.platform() if platform is None else str(platform or "")).lower()
    row = _REGISTRIES.get(registry, {}).get(resolved)
    if row is None or operation not in row:
        raise UnsupportedOnPlatform(feature, resolved)
    return row[operation]
