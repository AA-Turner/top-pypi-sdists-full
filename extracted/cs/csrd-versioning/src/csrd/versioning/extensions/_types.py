"""Core types for the unified extension system.

Extensions are the primary mechanism for composing functionality into a
versioned FastAPI application.  Built-in extensions (actuator, swagger docs)
and custom extensions share the same protocol.

This module is a dependency leaf: it imports no host-specific modules.
"""

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from fastapi import FastAPI

from .._types import VersionMap


@dataclass(frozen=True)
class ExtensionContext:
    """Read-only metadata passed to extensions during ``apply()``.

    Extensions receive this to make decisions about routing, naming,
    and version-aware behaviour without needing access to the full config.
    """

    app_name: str
    """Human-readable application name."""

    prefix: str
    """Normalised API prefix, e.g. ``"/api"``."""

    version_mapping: VersionMap
    """The version key → FastAPI sub-app mapping."""

    hit_id_header: str = ""
    """Header name for hit/correlation IDs."""

    app_id_header: str = ""
    """Header name for application IDs."""

    default_version: Any = None
    """Default version key for dispatch."""

    strict_version_matching: bool = False
    """Whether version matching is strict."""

    build_tag: str | None = None
    """Build tag from versioning settings."""

    settings: Any = None
    """Versioning settings (``VersioningSettings`` instance), if loaded."""


@runtime_checkable
class Extension(Protocol):
    """Protocol for composable units of functionality.

    Extensions wire themselves into the FastAPI app during
    ``configure_versioned_api()``.  They can register routes, add
    middleware, mount sub-apps, or perform any other app-level setup.

    Built-in extensions (actuator, swagger docs) follow this same
    protocol and are included by default.  Consumers can override,
    disable, or add custom extensions via ``VersionedApiConfig.extensions``.

    Resolution semantics:

    - Default extensions are loaded first.
    - User-provided extensions override defaults **by name**.
    - Extensions with ``enabled = False`` are filtered out.
    - Remaining extensions are sorted by ``order`` (ascending).
    """

    name: str
    """Unique extension identifier.  User extensions with the same name
    override built-in defaults."""

    order: int
    """Execution order within the extension list (lower = earlier).
    Built-in defaults: actuator=50, swagger_docs=90."""

    enabled: bool
    """Whether this extension is active.  Set to ``False`` to disable
    a built-in extension without removing it from the list."""

    def apply(self, app: FastAPI, ctx: ExtensionContext) -> None:
        """Wire this extension into *app*.

        Called once during ``configure_versioned_api()``.  The extension
        can register routes, add middleware, mount sub-apps, etc.

        Parameters
        ----------
        app:
            The root FastAPI application being configured.
        ctx:
            Read-only context with app metadata and version mapping.
        """
        ...
