"""matrx_ai.capabilities — client-capability registry.

A capability is a named bundle of:
  (a) a typed payload the client carries (e.g. editor cursor, sandbox binding),
  (b) tool enablements that come online when the capability is declared.

Replaces the per-feature request fields (``ide_state``, ``sandbox``, future
``chrome_extension``, …) with a single envelope where the client says "I have
these capabilities, here's the state for each." A client that's both an IDE
and a browser extension declares both bundles and gets the union of tools.

Hosts (aidream, matrx-local, etc.) register their bundles at startup via
``matrx_ai.configure(capabilities=[Capability(...), ...])`` — same registry,
multiple sources contributing. matrx-ai itself ships with platform-level
defaults; the host adds product-specific bundles on top.

Read TOOL_INJECTION_REFACTOR.md (root) for the full design.
"""
from __future__ import annotations

from .models import (
    Capability,
    CapabilityResolutionError,
    ClientContext,
    SurfaceAmendments,
    UserOverrides,
)
from .registry import (
    clear_capabilities,
    get_capability,
    list_capabilities,
    register_capability,
    resolve_client_capabilities,
)

# Importing built_in registers the platform-level bundles into the registry
# at first import. This is a deliberate side-effect — the registry must be
# populated before any request handler resolves a ClientContext.
from . import built_in as _built_in  # noqa: F401

__all__ = [
    "Capability",
    "CapabilityResolutionError",
    "ClientContext",
    "SurfaceAmendments",
    "UserOverrides",
    "register_capability",
    "get_capability",
    "list_capabilities",
    "clear_capabilities",
    "resolve_client_capabilities",
]
