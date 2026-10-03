"""The harness registry: every coding agent Probe integrates with (see `registry`)."""

from probe.harness.registry import (
    FAMILY_DETECT_ONLY,
    FAMILY_EXTENSION,
    FAMILY_HOOK_PLUGIN,
    Capture,
    Harness,
    Registry,
    RegistryError,
    get_registry,
    load,
)

__all__ = [
    "FAMILY_DETECT_ONLY",
    "FAMILY_EXTENSION",
    "FAMILY_HOOK_PLUGIN",
    "Capture",
    "Harness",
    "Registry",
    "RegistryError",
    "get_registry",
    "load",
]
