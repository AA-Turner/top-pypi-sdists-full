"""Catalog Tools: the host-injected executor and the lazy definition resolver.

A catalog Tool is a ``tool.definition`` row with ``source_kind = 'catalog'``:
one job ("Domain Authority") run by ONE host executor (the router behind the
call layer), never a code ``@tool``. Thousands of them exist, so they are never
preloaded into the registry: whole-catalog readers filter them out and every
request resolves the few it names, at the async edges, through the host's
resolver. Contract: common-docs/projects/third-party-services/CONTRACT.md §4.

Both seams are optional. Unconfigured, a catalog definition answers a plain
``configuration`` error and a lazy resolve finds nothing (matrx-ai standalone).
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, Iterable
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext

    from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult

CATALOG_SOURCE_KIND = "catalog"
CATALOG_FUNCTION_PREFIX = "catalog:"

CatalogExecutor = Callable[["ToolDefinition", dict[str, Any], "ToolContext"], Awaitable["ToolResult"]]
LazyToolResolver = Callable[[list[str]], Awaitable[list["ToolDefinition"]]]
#: How long (seconds) a resolved definition is kept for new requests — the host's knob.
CacheSeconds = Callable[[], Awaitable[float]]

_CATALOG_EXECUTOR: CatalogExecutor | None = None
_LAZY_RESOLVER: LazyToolResolver | None = None
_CACHE_SECONDS: CacheSeconds | None = None

# Per-process cache of resolved definitions: key (name or id) -> (expires_at, def).
# Only NEW requests read it; a live request holds its own pinned copy
# (stash_request_tool_definition), so eviction never pulls a definition from
# under a running turn. With no host window configured nothing is kept.
_LAZY_CACHE: dict[str, tuple[float, ToolDefinition]] = {}


def configure_catalog_executor(fn: CatalogExecutor | None) -> None:
    """Install the one executor every catalog Tool dispatches to."""
    global _CATALOG_EXECUTOR
    _CATALOG_EXECUTOR = fn


def get_catalog_executor() -> CatalogExecutor | None:
    return _CATALOG_EXECUTOR


def configure_lazy_tool_resolver(fn: LazyToolResolver | None, *, cache_seconds: CacheSeconds | None = None) -> None:
    """Install the async resolver that turns catalog names or ids into definitions.

    ``cache_seconds`` is the host's knob reader for how long a resolved definition is reused by
    new requests; without it every request resolves afresh.
    """
    global _LAZY_RESOLVER, _CACHE_SECONDS
    _LAZY_RESOLVER = fn
    _CACHE_SECONDS = cache_seconds
    _LAZY_CACHE.clear()


def get_lazy_tool_resolver() -> LazyToolResolver | None:
    return _LAZY_RESOLVER


def clear_lazy_cache() -> None:
    _LAZY_CACHE.clear()


def strip_ui_keywords(schema: Any) -> Any:
    """Drop every ``ui:*`` keyword, recursively. Providers never see form hints."""
    if isinstance(schema, dict):
        return {k: strip_ui_keywords(v) for k, v in schema.items() if not (isinstance(k, str) and k.startswith("ui:"))}
    if isinstance(schema, list):
        return [strip_ui_keywords(v) for v in schema]
    return schema


def cached_lazy_definition(name_or_id: str) -> ToolDefinition | None:
    entry = _LAZY_CACHE.get(name_or_id)
    if entry is None:
        return None
    expires_at, tool_def = entry
    if expires_at < time.monotonic():
        _LAZY_CACHE.pop(name_or_id, None)
        return None
    return tool_def


def _remember(tool_def: ToolDefinition, window: float) -> None:
    if window <= 0:
        return
    expires_at = time.monotonic() + window
    _LAZY_CACHE[tool_def.name] = (expires_at, tool_def)
    if tool_def.tool_id:
        _LAZY_CACHE[str(tool_def.tool_id)] = (expires_at, tool_def)


def _pin(ctx: AppContext | None, tool_def: ToolDefinition) -> None:
    if ctx is None:
        return
    from matrx_ai.tools.agent_projection import stash_request_tool_definition

    stash_request_tool_definition(ctx, tool_def)


async def resolve_lazy_tools(
    names_or_ids: Iterable[Any],
    *,
    ctx: AppContext | None = None,
) -> list[ToolDefinition]:
    """Resolve the catalog definitions a request names and pin them to it.

    Names the registry already holds (and request projections) are skipped.
    Every definition used — fresh from the resolver or from the process
    cache — is pinned on ``ctx`` for the life of the request. A name the
    resolver cannot find stays unresolved here and is reported where it is
    used (the registry's missing-tools warning, the executor's not-found).
    """
    from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
    from matrx_ai.tools.registry import ToolRegistry

    if ctx is None:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    pinned: dict[str, Any] = {}
    if ctx is not None and isinstance(ctx.metadata, dict):
        pinned = ctx.metadata.get(PROJECTED_AGENT_TOOLS_KEY) or {}

    registry = ToolRegistry.get_instance()
    wanted: list[str] = []
    for raw in names_or_ids:
        if not isinstance(raw, str) or not raw.strip():
            continue
        key = raw.strip()
        if key in pinned or key in wanted:
            continue
        known = registry.get(key)
        if known is not None and getattr(known, "source_kind", None) != CATALOG_SOURCE_KIND:
            continue
        wanted.append(key)
    if not wanted:
        return []

    found: list[ToolDefinition] = []
    misses: list[str] = []
    for key in wanted:
        cached = cached_lazy_definition(key)
        if cached is not None:
            found.append(cached)
        else:
            misses.append(key)

    resolver = _LAZY_RESOLVER
    if misses and resolver is not None:
        try:
            fresh = await resolver(misses)
        except Exception as exc:
            vcprint(
                {"names": misses, "error": repr(exc)},
                "[catalog_seam] lazy tool resolver failed — these catalog tools are unavailable to this request",
                color="red",
            )
            fresh = []
        window = 0.0
        if _CACHE_SECONDS is not None:
            try:
                window = float(await _CACHE_SECONDS())
            except Exception as exc:
                vcprint(f"[catalog_seam] cache window unreadable ({exc!r}); not caching", color="yellow")
        for tool_def in fresh:
            _remember(tool_def, window)
            found.append(tool_def)

    seen: set[str] = set()
    out: list[ToolDefinition] = []
    for tool_def in found:
        if tool_def.name in seen:
            continue
        seen.add(tool_def.name)
        _pin(ctx, tool_def)
        out.append(tool_def)
    return out


__all__ = [
    "CATALOG_FUNCTION_PREFIX",
    "CATALOG_SOURCE_KIND",
    "CatalogExecutor",
    "CacheSeconds",
    "LazyToolResolver",
    "cached_lazy_definition",
    "clear_lazy_cache",
    "configure_catalog_executor",
    "configure_lazy_tool_resolver",
    "get_catalog_executor",
    "get_lazy_tool_resolver",
    "resolve_lazy_tools",
    "strip_ui_keywords",
]
