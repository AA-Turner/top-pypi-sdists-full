"""Regression guards for the deprecated shim modules' DeprecationWarning emission.

WP03 of mission 006-hosted-discovery-contract-hardening added
``warnings.warn(..., DeprecationWarning, stacklevel=2)`` to the two
backward-compatibility shim modules:

- ``spec_kitty_tracker.workspace_discovery`` → directs callers to
  ``spec_kitty_tracker.discover_workspaces``
- ``spec_kitty_tracker.resource_discovery`` → directs callers to
  ``spec_kitty_tracker.discover_resources``

The mission verified the warning behavior manually but added no automated
regression guard. The post-merge mission review (RISK-1) flagged this gap:
if a future refactor accidentally removes the ``warnings.warn(...)`` call,
the shim's documentary purpose is preserved by its docstring but the runtime
deprecation signal silently disappears, and pinned downstream consumers lose
the migration prompt.

These tests close that gap. They use ``importlib`` to clear any cached module
state (so the warning fires fresh on each test) and ``pytest.warns`` to
assert the warning is emitted with the expected category and text.
"""

from __future__ import annotations

import importlib
import sys

import pytest


def _force_fresh_import(module_name: str) -> None:
    """Remove a module from ``sys.modules`` so the next import re-runs its body.

    Python caches imported modules, which means a second ``import foo`` would
    not re-execute ``foo``'s top-level statements (including ``warnings.warn``).
    Tests that need to observe import-time warnings must clear the cache first.
    """
    sys.modules.pop(module_name, None)


def test_workspace_discovery_shim_emits_deprecation_warning() -> None:
    """Importing ``spec_kitty_tracker.workspace_discovery`` must emit a
    DeprecationWarning that names ``spec_kitty_tracker.discover_workspaces``
    as the canonical replacement.
    """
    _force_fresh_import("spec_kitty_tracker.workspace_discovery")
    with pytest.warns(
        DeprecationWarning,
        match=r"spec_kitty_tracker\.discover_workspaces",
    ):
        importlib.import_module("spec_kitty_tracker.workspace_discovery")


def test_resource_discovery_shim_emits_deprecation_warning() -> None:
    """Importing ``spec_kitty_tracker.resource_discovery`` must emit a
    DeprecationWarning that names ``spec_kitty_tracker.discover_resources``
    as the canonical replacement.
    """
    _force_fresh_import("spec_kitty_tracker.resource_discovery")
    with pytest.warns(
        DeprecationWarning,
        match=r"spec_kitty_tracker\.discover_resources",
    ):
        importlib.import_module("spec_kitty_tracker.resource_discovery")


def test_workspace_discovery_shim_re_exports_still_resolve() -> None:
    """Even after the deprecation warning fires, the shim's re-exports must
    still resolve at runtime — the deprecation is non-breaking.
    """
    _force_fresh_import("spec_kitty_tracker.workspace_discovery")
    with pytest.warns(DeprecationWarning):
        from spec_kitty_tracker.workspace_discovery import (  # noqa: F401
            DiscoveredWorkspace,
            DiscoveryResult,
            discover_workspaces,
        )

    # The names must be importable and bound to real callables/types.
    assert DiscoveredWorkspace is not None
    assert DiscoveryResult is not None
    assert callable(discover_workspaces)


def test_resource_discovery_shim_re_exports_still_resolve() -> None:
    """Even after the deprecation warning fires, the shim's re-exports must
    still resolve at runtime — the deprecation is non-breaking.
    """
    _force_fresh_import("spec_kitty_tracker.resource_discovery")
    with pytest.warns(DeprecationWarning):
        from spec_kitty_tracker.resource_discovery import (  # noqa: F401
            DiscoveredResource,
            DiscoveryResult,
            discover_resources,
        )

    assert DiscoveredResource is not None
    assert DiscoveryResult is not None
    assert callable(discover_resources)
