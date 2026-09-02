"""Tests for the per-request ``tool_aliases`` map (Step 2 of the
tool registry redesign).

The alias map lives at ``AppContext.metadata['tool_aliases']`` and
maps ``exposed_name → canonical_name``. The dispatcher consults it
between the agent-projection lookup and the registry fallback.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.tool_aliases import (
    TOOL_ALIASES_KEY,
    add_aliases,
    add_identity_aliases,
    clear_aliases,
    get_alias_map,
    lookup_canonical,
    remove_aliases,
)


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _make_app_ctx() -> Any:
    from matrx_connect import AppContext

    return AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)


class TestAliasMapWrites:
    def test_add_aliases_creates_map_on_empty_metadata(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"cool_stuff:scrape_page": "scraper:scrape_page"})
        assert ctx.metadata[TOOL_ALIASES_KEY] == {
            "cool_stuff:scrape_page": "scraper:scrape_page"
        }

    def test_add_identity_aliases(self) -> None:
        ctx = _make_app_ctx()
        add_identity_aliases(
            ctx, ["matrx-ai:shell", "matrx-extend:take_screenshot"]
        )
        assert ctx.metadata[TOOL_ALIASES_KEY] == {
            "matrx-ai:shell": "matrx-ai:shell",
            "matrx-extend:take_screenshot": "matrx-extend:take_screenshot",
        }

    def test_add_aliases_merges_into_existing(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"a:1": "x:1"})
        add_aliases(ctx, {"a:2": "x:2"})
        assert ctx.metadata[TOOL_ALIASES_KEY] == {
            "a:1": "x:1",
            "a:2": "x:2",
        }

    def test_conflict_without_overwrite_keeps_first(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"shared:tool": "ns_a:tool"})
        add_aliases(ctx, {"shared:tool": "ns_b:tool"})  # conflict
        assert ctx.metadata[TOOL_ALIASES_KEY]["shared:tool"] == "ns_a:tool"

    def test_conflict_with_overwrite_replaces(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"shared:tool": "ns_a:tool"})
        add_aliases(ctx, {"shared:tool": "ns_b:tool"}, overwrite=True)
        assert ctx.metadata[TOOL_ALIASES_KEY]["shared:tool"] == "ns_b:tool"

    def test_add_aliases_repairs_wrong_shape(self) -> None:
        """If something writes the wrong type to the alias key, add_aliases
        repairs it rather than crashing."""
        ctx = _make_app_ctx()
        ctx.metadata[TOOL_ALIASES_KEY] = "not a dict"
        add_aliases(ctx, {"a:1": "x:1"})
        assert ctx.metadata[TOOL_ALIASES_KEY] == {"a:1": "x:1"}

    def test_remove_aliases(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"a:1": "x:1", "a:2": "x:2", "a:3": "x:3"})
        removed = remove_aliases(ctx, ["a:2", "nonexistent"])
        assert removed == 1
        assert ctx.metadata[TOOL_ALIASES_KEY] == {"a:1": "x:1", "a:3": "x:3"}

    def test_clear_aliases(self) -> None:
        ctx = _make_app_ctx()
        add_aliases(ctx, {"a:1": "x:1"})
        clear_aliases(ctx)
        assert TOOL_ALIASES_KEY not in ctx.metadata


class TestAliasLookup:
    def test_lookup_canonical_via_contextvar(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_app_ctx()
        add_aliases(ctx, {"forms:fill_form": "matrx-extend:fill_form"})
        token = set_app_context(ctx)
        try:
            assert (
                lookup_canonical("forms:fill_form")
                == "matrx-extend:fill_form"
            )
        finally:
            clear_app_context(token)

    def test_lookup_canonical_returns_none_for_unknown(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_app_ctx()
        token = set_app_context(ctx)
        try:
            assert lookup_canonical("nonexistent:tool") is None
        finally:
            clear_app_context(token)

    def test_lookup_canonical_returns_none_when_no_context(self) -> None:
        # No active AppContext. Should not raise.
        assert lookup_canonical("anything") is None

    def test_get_alias_map_is_defensive_copy(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_app_ctx()
        add_aliases(ctx, {"a:1": "x:1"})
        token = set_app_context(ctx)
        try:
            snapshot = get_alias_map()
            # Mutate the snapshot — original should be unaffected.
            snapshot["b:2"] = "y:2"
            assert "b:2" not in ctx.metadata[TOOL_ALIASES_KEY]
        finally:
            clear_app_context(token)


class TestAliasIntegrationWithExecutorLookupOrder:
    """The executor consults projected_agent_tools first, then the alias
    map, then the registry. Validate that ordering works as designed."""

    def test_alias_resolution_returns_canonical_name(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_app_ctx()
        add_aliases(
            ctx,
            {
                "research:scrape_page": "scraper:scrape_page",
                "research:web_search": "matrx-ai:web_search",
            },
        )
        token = set_app_context(ctx)
        try:
            # Same canonical reachable under bundle alias and identity.
            assert (
                lookup_canonical("research:scrape_page")
                == "scraper:scrape_page"
            )
            assert (
                lookup_canonical("research:web_search")
                == "matrx-ai:web_search"
            )
        finally:
            clear_app_context(token)

    def test_two_bundles_can_alias_same_canonical(self) -> None:
        """A single canonical tool may appear in multiple bundles. Each
        bundle's exposed name resolves to the same canonical."""
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        ctx = _make_app_ctx()
        add_aliases(
            ctx,
            {
                "research:scrape_page": "scraper:scrape_page",
                "data_extraction:scrape_page": "scraper:scrape_page",
            },
        )
        token = set_app_context(ctx)
        try:
            assert (
                lookup_canonical("research:scrape_page")
                == lookup_canonical("data_extraction:scrape_page")
                == "scraper:scrape_page"
            )
        finally:
            clear_app_context(token)
