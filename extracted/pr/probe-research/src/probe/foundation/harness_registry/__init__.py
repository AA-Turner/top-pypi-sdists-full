"""The harness registry: every coding agent Probe integrates with (see `registry`)."""

from probe.foundation.harness_registry.harness_registry import (
    FAMILY_EXTENSION,
    FAMILY_HOOK_PLUGIN,
    WAKE_BY_QUEUE,
    WAKE_BY_STOP_HOOK,
    Capture,
    Harness,
    Registry,
    RegistryError,
    get_registry,
    load,
)

__all__ = [
    "FAMILY_EXTENSION",
    "FAMILY_HOOK_PLUGIN",
    "WAKE_BY_QUEUE",
    "WAKE_BY_STOP_HOOK",
    "Capture",
    "Harness",
    "Registry",
    "RegistryError",
    "get_registry",
    "load",
]
