"""Registry of UDF sidecars, keyed by Python minor version.

The SDK owns the registry; the kernel package owns the implementation and
registers a *factory* into it at kernel start.

Why a factory rather than a builder: a sidecar is only correct for one
**(Python minor, Spark version) pair** -- the Python must match the worker and
the pyspark must match the engine's Spark. At kernel start no session exists, so
the Spark version is unknown. The factory takes it at first use, once the SDK
has read it off the live session, and each Spark version gets its own cached
builder so a kernel talking to both Glue 5 and Glue 6 works.

A "builder" is any object exposing ``build(request: dict) -> dict``.
"""

from __future__ import annotations

import logging
import sys
import threading
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("SparkConnect")

DEFAULT_CAPABILITIES = ("udf", "pandas_udf")


def client_python_version() -> str:
    """This (client) process's Python minor version, e.g. ``'3.11'``."""
    return "%d.%d" % sys.version_info[:2]


def normalize_python_version(version: str) -> str:
    """Coerce any version string to ``major.minor``.

    The registry key granularity matches the upstream gate, which compares
    ``"%d.%d" % sys.version_info[:2]``. A patch-level key would never match.
    """
    parts = str(version).split(".")
    if len(parts) < 2:
        raise ValueError(f"cannot derive a major.minor version from {version!r}")
    return f"{parts[0]}.{parts[1]}"


class SidecarEntry:
    """One registered sidecar implementation for a Python minor version."""

    def __init__(
        self,
        python_version: str,
        factory: Callable[[str], Any],
        capabilities: Optional[List[str]] = None,
    ) -> None:
        self.python_version = normalize_python_version(python_version)
        self._factory = factory
        self.capabilities = list(capabilities or DEFAULT_CAPABILITIES)
        self._builders: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def builder(self, spark_version: str) -> Any:
        """Return the builder for ``spark_version``, creating it on first use."""
        builder = self._builders.get(spark_version)
        if builder is None:
            with self._lock:
                builder = self._builders.get(spark_version)
                if builder is None:
                    logger.info(
                        "creating UDF sidecar builder for python=%s spark=%s",
                        self.python_version,
                        spark_version,
                    )
                    builder = self._factory(spark_version)
                    self._builders[spark_version] = builder
        return builder


_REGISTRY: Dict[str, SidecarEntry] = {}
_REGISTRY_LOCK = threading.Lock()


def register_sidecar(
    python_version: str,
    factory: Callable[[str], Any],
    capabilities: Optional[List[str]] = None,
) -> SidecarEntry:
    """Register a sidecar factory for a Python minor version.

    Called by the kernel's startup script. ``factory(spark_version)`` returns a
    builder; it is invoked lazily on the first version-mismatched UDF for that
    Spark version, never here.
    """
    entry = SidecarEntry(python_version, factory, capabilities)
    with _REGISTRY_LOCK:
        _REGISTRY[entry.python_version] = entry
    logger.info(
        "registered UDF sidecar for python_version=%s (capabilities=%s)",
        entry.python_version,
        entry.capabilities,
    )
    return entry


def get_sidecar(python_version: str) -> Optional[SidecarEntry]:
    """Return the entry registered for a Python minor version, or ``None``."""
    key = normalize_python_version(python_version)
    with _REGISTRY_LOCK:
        return _REGISTRY.get(key)


def unregister_sidecar(python_version: str) -> None:
    key = normalize_python_version(python_version)
    with _REGISTRY_LOCK:
        _REGISTRY.pop(key, None)


def clear_registry() -> None:
    with _REGISTRY_LOCK:
        _REGISTRY.clear()


def registered_versions() -> List[str]:
    with _REGISTRY_LOCK:
        return sorted(_REGISTRY)
