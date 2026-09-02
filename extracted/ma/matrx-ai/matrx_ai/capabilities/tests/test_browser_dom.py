"""Tests for the ``browser-dom`` capability + ``load_chrome_tools`` handler.

The matrx-extend Chrome extension is the first multi-tool capability with
a discovery handler. These tests exercise:

  - Payload schema validation (BrowserDomPayload)
  - Capability registration and the always-on spec factory
  - The discovery handler's filter rules: admin gating, optional Chrome
    permission gating, desktop-bridge gating
  - Mutation queue side effects (``ctx.queue_tool_changes``)
  - Error paths: unknown category, admin-only category for non-admin

Handler tests that exercise category routing require the registry to be
populated from the database (``initialize_tool_system_sync()``). They are
marked ``integration`` and skipped in pure-unit environments.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai.capabilities.browser_dom import (
    BROWSER_DOM,
    BrowserDomPayload,
    get_admin_only_categories,
    get_category_names,
)
from matrx_ai.tools.implementations.browser_discovery import load_chrome_tools
from matrx_ai.tools.models import _PENDING_TOOL_MUTATIONS_KEY, ToolContext


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


def _make_app_ctx(
    state: dict[str, Any] | None = None,
    *,
    active_executors: list[str] | None = ("chrome-extension",),
):
    """Build an AppContext with a `browser-dom` payload mounted under the
    canonical client_capabilities_payloads key (mirrors what
    apply_unified_tools writes). ``active_executors`` mirrors the
    ACTIVE_TOOL_EXECUTORS_KEY the host stamps at the request edge; the
    chrome-extension default reflects a real extension request. Pass None
    to model a surface with no extension client (the refusal path)."""
    from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY
    from matrx_connect import AppContext

    metadata: dict[str, Any] = {}
    if state is not None:
        metadata["client_capabilities_payloads"] = {"browser-dom": state}
    if active_executors is not None:
        metadata[ACTIVE_TOOL_EXECUTORS_KEY] = list(active_executors)
    return AppContext(emitter=_NullEmitter(), metadata=metadata, is_authenticated=True)


def _tool_ctx(name: str = "load_chrome_tools") -> ToolContext:
    return ToolContext(call_id="call-1", tool_name=name)


def _has_registry_tools() -> bool:
    """Return True if the registry has chrome-extension-bound tools loaded."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    for t in registry.list_tools():
        bindings = registry.bindings_for_tool(t.name)
        if any(
            b == "chrome-extension" or b.startswith("chrome-extension.")
            for b in bindings
        ):
            return True
    return False


# ---------------------------------------------------------------------------
# BrowserDomPayload — schema validation (pure unit tests, no DB needed)
# ---------------------------------------------------------------------------


class TestBrowserDomPayload:
    def test_minimum_required_fields(self) -> None:
        payload = BrowserDomPayload.model_validate(
            {
                "surface": "assistant",
                "is_admin": False,
                "permission_mode": "ask",
                "desktop_bridge": "none",
                "onbox_ai_available": True,
                "optional_permissions_granted": [],
            }
        )
        assert payload.surface == "assistant"
        assert payload.is_admin is False
        assert payload.optional_permissions_granted == []

    def test_full_payload_round_trip(self) -> None:
        raw = {
            "current_url": "https://example.com/article/42",
            "current_tab_id": 1234,
            "current_window_id": 7,
            "page_title": "Example",
            "page_lang": "en",
            "tab_status": "complete",
            "surface": "pilot",
            "is_admin": True,
            "permission_mode": "act",
            "desktop_bridge": "native",
            "onbox_ai_available": True,
            "optional_permissions_granted": ["debugger", "cookies"],
            "open_tab_count": 5,
            "extension_version": "0.1.4",
            "extension_id": "cihdmkcdjjckfhjpgoedmgfpoljebaml",
            "loaded_categories": ["core"],
        }
        payload = BrowserDomPayload.model_validate(raw)
        assert payload.optional_permissions_granted == ["debugger", "cookies"]
        assert payload.loaded_categories == ["core"]

    def test_invalid_surface_rejected(self) -> None:
        with pytest.raises(ValidationError):
            BrowserDomPayload.model_validate(
                {
                    "surface": "magic",
                    "is_admin": False,
                    "permission_mode": "ask",
                    "desktop_bridge": "none",
                    "onbox_ai_available": False,
                    "optional_permissions_granted": [],
                }
            )

    def test_invalid_desktop_bridge_rejected(self) -> None:
        with pytest.raises(ValidationError):
            BrowserDomPayload.model_validate(
                {
                    "surface": "assistant",
                    "is_admin": False,
                    "permission_mode": "ask",
                    "desktop_bridge": "wifi",
                    "onbox_ai_available": False,
                    "optional_permissions_granted": [],
                }
            )


# ---------------------------------------------------------------------------
# BROWSER_DOM capability shape (no DB needed)
# ---------------------------------------------------------------------------


class TestBrowserDomCapability:
    def test_capability_metadata(self) -> None:
        assert BROWSER_DOM.name == "browser-dom"
        assert BROWSER_DOM.payload_model is BrowserDomPayload
        # Guest mode (2026-05-18): browser-dom is available unauthenticated
        # (browser_dom.py sets requires_auth=False).
        assert BROWSER_DOM.requires_auth is False
        # enabled_tools is empty — all specs come from the factory at request time.
        assert BROWSER_DOM.enabled_tools == ()
        # factory is set and callable
        assert callable(BROWSER_DOM.enabled_tools_factory)

    def test_factory_returns_tuple_of_specs(self) -> None:
        """Factory must return a tuple of ToolSpec — even when the registry
        has no matrx-extend rows it returns at least the discovery tool."""
        import matrx_ai.capabilities.browser_dom as _dom_mod

        # Clear cache so we get a fresh call regardless of test order.
        _dom_mod._specs_cache = None
        try:
            specs = BROWSER_DOM.enabled_tools_factory()
            assert isinstance(specs, tuple)
            # load_chrome_tools is always first
            assert len(specs) >= 1
            assert specs[0].name == "load_chrome_tools"
        finally:
            _dom_mod._specs_cache = None


# ---------------------------------------------------------------------------
# Integration tests — require the registry populated from the DB.
# Skip gracefully in pure-unit environments.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def registry_with_tools():
    """Ensure the registry has matrx-extend tools; skip if not available."""
    if not _has_registry_tools():
        pytest.skip(
            "ToolRegistry has no matrx-extend tools. "
            "Run initialize_tool_system_sync() before these tests or "
            "run against a real database."
        )


class TestBrowserDomCapabilityWithRegistry:
    """Capability spec assertions that require DB data in the registry."""

    def test_always_on_specs_match_db_auto_load(self, registry_with_tools: None) -> None:
        """The factory should return one InlineToolSpec per always-include
        entry in tool_surface_defaults (plus load_chrome_tools as
        RegisteredToolSpec)."""
        import matrx_ai.capabilities.browser_dom as _dom_mod
        from matrx_ai.tools.registry import ToolRegistry
        from matrx_ai.tools.specs import InlineToolSpec, RegisteredToolSpec

        _dom_mod._specs_cache = None
        try:
            specs = BROWSER_DOM.enabled_tools_factory()
            assert len(specs) >= 1

            discovery = specs[0]
            assert isinstance(discovery, RegisteredToolSpec)
            assert discovery.name == "load_chrome_tools"
            assert discovery.delegate is False

            for spec in specs[1:]:
                assert isinstance(spec, InlineToolSpec), f"{spec.name!r} should be InlineToolSpec"
                assert spec.description, f"{spec.name!r} must carry a description"
                assert spec.input_schema, f"{spec.name!r} must carry an input_schema"

            # Verify count matches tool_surface_defaults.always_include_tools.
            always_include = _dom_mod._read_always_include_tools(
                "matrx-extend.browser"
            )
            assert len(specs) == len(always_include) + 1  # +1 for load_chrome_tools
        finally:
            _dom_mod._specs_cache = None

    def test_admin_only_categories_are_all_admin_gated(self, registry_with_tools: None) -> None:
        import matrx_ai.capabilities.browser_dom as _dom_mod

        _dom_mod._admin_only_categories_cache = None
        try:
            admin_cats = get_admin_only_categories()
            category_names = set(get_category_names())
            for cat in admin_cats:
                assert cat in category_names, (
                    f"admin-gated category {cat!r} not in known categories"
                )
        finally:
            _dom_mod._admin_only_categories_cache = None

    def test_category_names_non_empty(self, registry_with_tools: None) -> None:
        import matrx_ai.capabilities.browser_dom as _dom_mod

        _dom_mod._category_names_cache = None
        try:
            names = get_category_names()
            assert len(names) > 0, "Registry must expose at least one matrx-extend category"
        finally:
            _dom_mod._category_names_cache = None


# ---------------------------------------------------------------------------
# load_chrome_tools handler tests — require registry
# ---------------------------------------------------------------------------


class TestLoadBrowserToolsHandler:
    async def test_unknown_category_returns_failure(self, registry_with_tools: None) -> None:
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": "made-up"}, _tool_ctx())
            assert result.success is False
            assert result.error.error_type == "unknown_category"
            assert "made-up" in result.error.message
        finally:
            clear_app_context(token)

    async def test_missing_category_returns_failure(self, registry_with_tools: None) -> None:
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                }
            )
        )
        try:
            result = await load_chrome_tools({}, _tool_ctx())
            assert result.success is False
            assert result.error.error_type == "invalid_argument"
        finally:
            clear_app_context(token)

    async def test_admin_only_category_blocked_for_non_admin(
        self, registry_with_tools: None
    ) -> None:
        admin_cats = get_admin_only_categories()
        if not admin_cats:
            pytest.skip("No admin-only categories in current DB data")

        from matrx_connect.context.app_context import clear_app_context, set_app_context

        category = next(iter(admin_cats))
        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": ["debugger"],
                    "desktop_bridge": "none",
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": category}, _tool_ctx())
            assert result.success is False
            assert result.error.error_type == "forbidden"
            assert "admin-only" in result.error.message
        finally:
            clear_app_context(token)

    async def test_non_admin_category_loads_for_anyone(self, registry_with_tools: None) -> None:
        admin_cats = get_admin_only_categories()
        non_admin_cats = [c for c in get_category_names() if c not in admin_cats]
        if not non_admin_cats:
            pytest.skip("No non-admin categories in current DB data")

        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        category = non_admin_cats[0]
        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": category}, _tool_ctx())
            assert result.success is True
            assert result.output["category"] == category
            assert result.output["missing_from_catalog"] == []

            pending = get_app_context().metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending is not None
            actions = [m["action"] for m in pending]
            assert "add" in actions
            assert "remove" in actions
            add_entry = next(m for m in pending if m["action"] == "add")
            for spec in add_entry["specs"]:
                assert spec["kind"] == "inline"
                assert spec["description"], f"{spec['name']!r} missing description"
                assert spec["input_schema"]["type"] == "object"
            remove_entry = next(m for m in pending if m["action"] == "remove")
            assert "load_chrome_tools" in remove_entry["names"]
        finally:
            clear_app_context(token)

    async def test_already_loaded_category_short_circuits(self, registry_with_tools: None) -> None:
        non_admin_cats = [c for c in get_category_names() if c not in get_admin_only_categories()]
        if not non_admin_cats:
            pytest.skip("No non-admin categories available")

        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        category = non_admin_cats[0]
        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                    "loaded_categories": [category],
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": category}, _tool_ctx())
            assert result.success is True
            assert result.output["already_loaded"] is True
            assert result.output["count"] == 0
            assert result.output["tools_loaded"] == []

            pending = get_app_context().metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending is not None
            actions = [m["action"] for m in pending]
            assert "remove" in actions
            for entry in pending:
                if entry["action"] == "add":
                    assert entry["specs"] == []
        finally:
            clear_app_context(token)

    async def test_loaded_categories_does_not_block_other_categories(
        self, registry_with_tools: None
    ) -> None:
        non_admin_cats = [c for c in get_category_names() if c not in get_admin_only_categories()]
        if len(non_admin_cats) < 2:
            pytest.skip("Need at least 2 non-admin categories")

        from matrx_connect.context.app_context import clear_app_context, set_app_context

        cat_a, cat_b = non_admin_cats[0], non_admin_cats[1]
        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                    "loaded_categories": [cat_a],
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": cat_b}, _tool_ctx())
            assert result.success is True
            assert result.output.get("already_loaded") is None
        finally:
            clear_app_context(token)

    async def test_no_payload_falls_back_to_non_admin_no_perms(
        self, registry_with_tools: None
    ) -> None:
        """When AppContext has no browser-dom payload, handler treats the
        user as non-admin with no granted permissions — safest default."""
        non_admin_cats = [c for c in get_category_names() if c not in get_admin_only_categories()]
        if not non_admin_cats:
            pytest.skip("No non-admin categories available")

        from matrx_connect.context.app_context import clear_app_context, set_app_context

        token = set_app_context(_make_app_ctx(state=None))
        try:
            result = await load_chrome_tools({"category": non_admin_cats[0]}, _tool_ctx())
            assert result.success is True
        finally:
            clear_app_context(token)

    async def test_desktop_gated_tool_skipped_when_bridge_none(
        self, registry_with_tools: None
    ) -> None:
        """desktop_run_command must be absent when desktop_bridge=none."""
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        from matrx_ai.tools.implementations.browser_discovery import (
            _registry_routing_for_category,
        )

        # Find which category desktop_run_command lives in.
        desktop_cat: str | None = None
        for cat in get_category_names():
            if cat in get_admin_only_categories():
                continue
            _, candidates = _registry_routing_for_category(cat)
            if "desktop_run_command" in candidates:
                desktop_cat = cat
                break

        if desktop_cat is None:
            pytest.skip("desktop_run_command not found in any non-admin category")

        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "none",
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": desktop_cat}, _tool_ctx())
            assert result.success is True
            assert "desktop_run_command" not in result.output["tools_loaded"]
            assert "desktop_run_command" in result.output["skipped_desktop_unavailable"]
        finally:
            clear_app_context(token)

    async def test_desktop_gated_tool_included_when_bridge_native(
        self, registry_with_tools: None
    ) -> None:
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        from matrx_ai.tools.implementations.browser_discovery import (
            _registry_routing_for_category,
        )

        desktop_cat: str | None = None
        for cat in get_category_names():
            if cat in get_admin_only_categories():
                continue
            _, candidates = _registry_routing_for_category(cat)
            if "desktop_run_command" in candidates:
                desktop_cat = cat
                break

        if desktop_cat is None:
            pytest.skip("desktop_run_command not found in any non-admin category")

        token = set_app_context(
            _make_app_ctx(
                state={
                    "is_admin": False,
                    "optional_permissions_granted": [],
                    "desktop_bridge": "native",
                }
            )
        )
        try:
            result = await load_chrome_tools({"category": desktop_cat}, _tool_ctx())
            assert result.success is True
            assert "desktop_run_command" in result.output["tools_loaded"]
            assert result.output["skipped_desktop_unavailable"] == []
        finally:
            clear_app_context(token)


# ---------------------------------------------------------------------------
# Executor-viability refusal — the 2026-08-21 stuck-'delegated' incident.
# A matrx-user/chat request (no chrome-extension client) carried
# load_chrome_tools; it loaded the extension's tools anyway and `navigate`
# delegated to a client that could never answer, pausing the request until
# the 30-day abandonment sweep. The loader must refuse OUTRIGHT when the
# chrome-extension executor is not live. Pure unit test — the gate fires
# before any registry access, so no DB is needed.
# ---------------------------------------------------------------------------


class TestLoadBrowserToolsExecutorGate:
    @pytest.mark.asyncio
    async def test_refuses_without_chrome_extension_executor(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        from matrx_ai.tools.models import _PENDING_TOOL_MUTATIONS_KEY

        # matrx-user surface: executors resolved, extension NOT among them.
        token = set_app_context(_make_app_ctx(active_executors=["matrx-user"]))
        try:
            result = await load_chrome_tools({"category": "reading"}, _tool_ctx())
            assert result.success is False
            assert result.error is not None
            assert result.error.error_type == "client_unavailable"
            # The loader must remove itself so the model can't loop on it.
            pending = get_app_context().metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending, "expected a queued self-removal mutation"
            remove_entry = next(m for m in pending if m.get("action") == "remove")
            assert "load_chrome_tools" in remove_entry["names"]
            # And it must not have queued ANY additions.
            assert not [m for m in pending if m.get("action") == "add" and m.get("specs")]
        finally:
            clear_app_context(token)

    @pytest.mark.asyncio
    async def test_refuses_with_no_resolved_executors(self) -> None:
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        token = set_app_context(_make_app_ctx(active_executors=None))
        try:
            result = await load_chrome_tools({"category": "reading"}, _tool_ctx())
            assert result.success is False
            assert result.error.error_type == "client_unavailable"
        finally:
            clear_app_context(token)

    @pytest.mark.asyncio
    async def test_dot_descendant_executor_counts_as_live(self) -> None:
        """chrome-extension.pilot (a sub-executor kind) satisfies the gate —
        the refusal must not fire; the call proceeds into normal category
        handling. In a pure-unit environment the registry is empty, so the
        proof the gate passed is that we get the registry RuntimeError (or a
        real result on an integration run) — never client_unavailable."""
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        token = set_app_context(
            _make_app_ctx(active_executors=["chrome-extension.pilot"])
        )
        try:
            try:
                result = await load_chrome_tools({"category": "reading"}, _tool_ctx())
            except RuntimeError:
                return  # empty registry — the gate was passed, as required
            if result.error is not None:
                assert result.error.error_type != "client_unavailable"
        finally:
            clear_app_context(token)
