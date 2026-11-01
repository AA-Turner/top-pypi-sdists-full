"""The daemon's session-log reader for a harness (`for_source`), found through its HarnessIntegration.
The ONE place the daemon looks a harness name up: every spelling comes from the registry."""

from __future__ import annotations

from probe.foundation.harness_registry import get_registry
from probe.shared.harness.harness import find_integration, get_integrations
from probe.shared.harness.session_log import Adapter, Capabilities


def for_source(source: str | None) -> Adapter:
    """A reader for a harness id, alias or route (no source: the registry's default harness)."""
    integration = find_integration((source or get_registry().default).strip().lower())
    adapter = integration.session_log if integration is not None else None
    if adapter is None:
        raise LookupError(f"no daemon adapter for harness {source!r}: daemon mode is unavailable there")
    return adapter()


def known() -> tuple[str, ...]:
    """Every harness the daemon can read, in registry order."""
    return tuple(i.harness_id for i in get_integrations() if i.session_log is not None)


__all__ = ["Adapter", "Capabilities", "for_source", "known"]
