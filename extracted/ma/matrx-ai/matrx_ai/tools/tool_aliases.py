"""Per-request tool name alias map (Step 2 of the tool registry redesign).

Generalizes the existing ``custom_tool_N → agent`` projection map
(``agent_projection.py``) into a unified mechanism: every tool the
model sees in a given request has an *exposed* name, and every exposed
name resolves to a *canonical* tool identity through the per-request
``tool_aliases`` map on ``AppContext.metadata``.

Two distinct sources populate the map:

  1. **Bundle loading** — when a discovery handler loads a bundle, each
     member gets an *identity* entry under its canonical name. (The
     original Decision-26 plan of rebranding members to
     ``<bundle_name>:<local_alias>`` was removed — the merge primitive
     keys registered specs by UUID and stores canonical names, so a
     rebranded name never reached the model; see
     ``implementations/bundle_lister.py``. Non-identity entries remain
     fully supported at dispatch should a future loader rebrand
     through the merge primitive.)

  2. **Auto-load / direct inclusion** — when a tool is added to the
     active set without a bundle wrapper (e.g. a
     ``tool_surface_defaults.always_include_tools`` entry, or a
     ``RegisteredToolSpec`` declared directly in the
     request), the alias map gets an *identity* entry mapping the
     canonical name to itself. Same code path, no special case at
     dispatch.

Provider-safety note: exposed names may carry a namespace colon; they are
serialized to the model in wire form (``:`` → ``__``) by the provider
boundary, and the executor reverses that before consulting this map. See
``matrx_ai.config.wire_names``.

The agent-projection map (``custom_tool_N → ToolDefinition`` synthetic
dict) keeps its own storage on ``AppContext.metadata`` because it
needs to rehydrate a synthetic ``ToolDefinition`` (function_path
``agent:<uuid>``, opaque parameters), which the alias map alone can't
encode. The dispatcher consults projected tools FIRST, then the alias
map, then the global registry.

Lifetime: per-request. The map lives on ``AppContext.metadata`` and is
cleared when the streaming task completes.
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from matrx_utils import vcprint

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext


# Key under which the unified alias map lives on ``AppContext.metadata``.
TOOL_ALIASES_KEY = "tool_aliases"


def add_aliases(
    ctx: "AppContext",
    aliases: dict[str, str],
    *,
    overwrite: bool = False,
) -> None:
    """Merge ``aliases`` into the per-request alias map.

    Parameters
    ----------
    ctx:
        The active AppContext. The map is mutated in place on
        ``ctx.metadata['tool_aliases']`` so downstream lookups via the
        ContextVar see the updates immediately.
    aliases:
        ``{exposed_name: canonical_name}`` to record. Identity entries
        (``{X: X}``) are valid and useful for non-bundled tools.
    overwrite:
        When ``False`` (default), an entry that conflicts with an
        existing entry is logged and skipped. When ``True``, the new
        value replaces the old. Conflicts during a single request
        usually mean the discovery handler ran twice or two bundles
        chose the same exposed name — the conflict is signal, not noise.
    """
    if not aliases:
        return

    metadata = ctx.metadata if ctx.metadata is not None else {}
    if ctx.metadata is None:
        # Defensive — AppContext.metadata may be None in tests.
        ctx.metadata = metadata

    existing = metadata.setdefault(TOOL_ALIASES_KEY, {})
    if not isinstance(existing, dict):
        # Repair — someone wrote the wrong shape into metadata.
        existing = {}
        metadata[TOOL_ALIASES_KEY] = existing

    for exposed, canonical in aliases.items():
        prior = existing.get(exposed)
        if prior is not None and prior != canonical:
            if overwrite:
                vcprint(
                    f"[tool_aliases] overwrite: {exposed!r} {prior!r} → {canonical!r}",
                    color="yellow",
                )
                existing[exposed] = canonical
            else:
                vcprint(
                    f"[tool_aliases] conflict ignored: {exposed!r} already → {prior!r}, "
                    f"refused to set → {canonical!r}",
                    color="yellow",
                )
            continue
        existing[exposed] = canonical


def add_identity_aliases(
    ctx: "AppContext", canonical_names: Iterable[str]
) -> None:
    """Convenience: register ``{name: name}`` for every canonical name.

    Used when a tool is loaded outside a bundle. Makes the dispatcher's
    lookup uniform: every exposed name resolves through the alias map
    even when no rebranding happens.
    """
    add_aliases(ctx, {name: name for name in canonical_names})


def lookup_canonical(exposed_name: str) -> str | None:
    """Resolve an exposed name to its canonical via the active request's
    alias map.

    Returns ``None`` when no entry exists. The dispatcher treats that as
    "not aliased" and falls back to direct registry lookup using the
    exposed name as canonical (back-compat for code paths that don't
    populate the map).

    Reads the active ``AppContext`` directly via the ContextVar — the
    executor is always invoked inside the streaming task that has set
    the ContextVar.
    """
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not ctx.metadata:
        return None
    aliases = ctx.metadata.get(TOOL_ALIASES_KEY)
    if not isinstance(aliases, dict):
        return None
    canonical = aliases.get(exposed_name)
    if canonical is None:
        return None
    return canonical


def get_alias_map() -> dict[str, str]:
    """Return a defensive copy of the active request's alias map for
    debugging / logging. Empty dict when no map exists.
    """
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not ctx.metadata:
        return {}
    aliases = ctx.metadata.get(TOOL_ALIASES_KEY)
    if not isinstance(aliases, dict):
        return {}
    return dict(aliases)


def clear_aliases(ctx: "AppContext") -> None:
    """Drop the alias map entirely. Used when a request needs to reset
    its loaded toolset (rare — the natural lifetime is the streaming
    task scope, after which AppContext is cleared anyway)."""
    if ctx.metadata is None:
        return
    ctx.metadata.pop(TOOL_ALIASES_KEY, None)


def remove_aliases(ctx: "AppContext", exposed_names: Iterable[str]) -> int:
    """Remove specific exposed-name entries from the map. Returns the
    count of entries actually removed. Used when a bundle is unloaded
    mid-loop (e.g. a discovery handler queues a removal).
    """
    if ctx.metadata is None:
        return 0
    aliases = ctx.metadata.get(TOOL_ALIASES_KEY)
    if not isinstance(aliases, dict):
        return 0
    removed = 0
    for name in exposed_names:
        if aliases.pop(name, None) is not None:
            removed += 1
    return removed
