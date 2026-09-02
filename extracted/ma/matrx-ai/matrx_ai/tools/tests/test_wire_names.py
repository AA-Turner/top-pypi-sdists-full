"""Tests for the wire-name layer — the provider-safe serialization of
colon-namespaced tool names and its reverse at dispatch.

The bug class this pins down: the 2026 tool-registry redesign renamed
tool rows to canonical ``<namespace>:<local>`` form (``bundle:list_*``
listers), but every provider enforces ``^[a-zA-Z0-9_-]{1,64}$`` on tool
names — sending a canonical name raw produced a hard 400
(``Invalid 'tools[0].name': string does not match pattern``) and killed
the whole request. The fix is a wire seam (``matrx_ai.config.wire_names``)
applied at the provider boundary and reversed at dispatch.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.wire_names import (
    WIRE_SAFE_RE,
    is_wire_safe,
    resolve_wire_name,
    to_wire_name,
)


# ---------------------------------------------------------------------------
# Primitive
# ---------------------------------------------------------------------------


class TestPrimitive:
    def test_colon_converts_to_double_underscore(self):
        assert to_wire_name("bundle:list_agent-core") == "bundle__list_agent-core"

    def test_plain_name_unchanged(self):
        assert to_wire_name("web_search") == "web_search"

    def test_idempotent(self):
        once = to_wire_name("bundle:list_supabase")
        assert to_wire_name(once) == once

    def test_is_wire_safe(self):
        assert is_wire_safe("bundle__list_agent-core")
        assert is_wire_safe("web_search")
        assert not is_wire_safe("bundle:list_agent-core")
        assert not is_wire_safe("")
        assert not is_wire_safe("x" * 65)

    def test_every_live_lister_shape_round_trips(self):
        # The exact naming convention in tool.definition today.
        for bundle in ("agent-core", "google-workspace", "code_ingest", "supabase"):
            canonical = f"bundle:list_{bundle}"
            wire = to_wire_name(canonical)
            assert WIRE_SAFE_RE.match(wire), wire
            assert resolve_wire_name(wire, [canonical, "web_search"]) == canonical

    def test_resolve_returns_none_for_plain_names(self):
        # A name with no wire separator can never be a mangled canonical.
        assert resolve_wire_name("web_search", ["web_search"]) is None

    def test_resolve_never_matches_colonless_candidates(self):
        # 'some__tool' is a legitimate plain name — reversing it to itself
        # would mask direct-lookup bugs, so colonless candidates are skipped.
        assert resolve_wire_name("some__tool", ["some__tool"]) is None

    def test_resolve_misses_cleanly(self):
        assert resolve_wire_name("nope__missing", ["bundle:list_x"]) is None


# ---------------------------------------------------------------------------
# Outbound seam — BaseTranslator.build_provider_tools
# ---------------------------------------------------------------------------


def _load_base_translator():
    from matrx_ai.providers.base_translator import BaseTranslator

    return BaseTranslator


class _FakeConfig:
    """Duck-typed stand-in for UnifiedConfig — build_provider_tools only
    touches .tools and .custom_tools."""

    def __init__(self, tools: list[str] | None = None, custom_tools: list[Any] | None = None):
        self.tools = tools or []
        self.custom_tools = custom_tools or []


class _InlineTool:
    """Duck-typed stand-in for CustomTool — only get_provider_format is used."""

    def __init__(self, name: str, provider_shape: str = "flat"):
        self.name = name
        self._shape = provider_shape

    def get_provider_format(self, provider: str) -> dict[str, Any]:
        if self._shape == "nested":
            return {"type": "function", "function": {"name": self.name, "parameters": {}}}
        return {"type": "function", "name": self.name, "parameters": {}}


@pytest.fixture()
def translator():
    BaseTranslator = _load_base_translator()

    class _T(BaseTranslator):
        def _assemble_request(self, config, api_class=""):  # pragma: no cover
            return None

    return _T()


class TestOutboundSeam:
    def test_colon_name_rewritten_flat_shape(self, translator):
        config = _FakeConfig(custom_tools=[_InlineTool("bundle:list_agent-core")])
        decls = translator.build_provider_tools(config, "openai")
        assert [d["name"] for d in decls] == ["bundle__list_agent-core"]

    def test_colon_name_rewritten_nested_shape(self, translator):
        config = _FakeConfig(
            custom_tools=[_InlineTool("bundle:list_agent-core", provider_shape="nested")]
        )
        decls = translator.build_provider_tools(config, "groq")
        assert [d["function"]["name"] for d in decls] == ["bundle__list_agent-core"]

    def test_plain_names_untouched(self, translator):
        config = _FakeConfig(custom_tools=[_InlineTool("web_search"), _InlineTool("note")])
        decls = translator.build_provider_tools(config, "openai")
        assert [d["name"] for d in decls] == ["web_search", "note"]

    def test_every_emitted_name_is_wire_safe(self, translator):
        config = _FakeConfig(
            custom_tools=[
                _InlineTool("bundle:list_google-workspace"),
                _InlineTool("agent-core:note"),
                _InlineTool("plain_tool"),
            ]
        )
        decls = translator.build_provider_tools(config, "anthropic")
        for d in decls:
            name = translator._declaration_name(d)
            assert name is None or is_wire_safe(name), name

    def test_wire_collision_drops_second_and_keeps_first(self, translator):
        # 'a:b' and 'a__b' collapse to the same wire name — the provider
        # would 400 on the duplicate; the seam must keep exactly one.
        config = _FakeConfig(custom_tools=[_InlineTool("a:b"), _InlineTool("a__b")])
        decls = translator.build_provider_tools(config, "openai")
        assert [d["name"] for d in decls] == ["a__b"]

    def test_unserializable_after_conversion_is_dropped(self, translator):
        # 63-char name + colon → 64 internal, 65 on the wire → cannot be
        # declared; the request must survive without it.
        long_name = "n" * 62 + ":x"
        config = _FakeConfig(custom_tools=[_InlineTool(long_name), _InlineTool("ok_tool")])
        decls = translator.build_provider_tools(config, "openai")
        assert [d["name"] for d in decls] == ["ok_tool"]

    def test_registered_lister_full_round_trip(self, translator, registry_with_lister):
        """The exact /ai/manual failure shape: a registered colon-named
        lister in config.tools must reach every provider as its wire name,
        and the model's wire-form call must dispatch back to the canonical."""
        from matrx_ai.tools.executor import ToolExecutor

        config = _FakeConfig(tools=["bundle:list_agent-core"])
        for provider in ("openai", "anthropic", "google", "groq"):
            decls = translator.build_provider_tools(config, provider)
            names = [translator._declaration_name(d) for d in decls]
            assert names == ["bundle__list_agent-core"], (provider, names)

        ex = ToolExecutor(registry=registry_with_lister)
        assert (
            ex._normalize_called_name("bundle__list_agent-core")
            == "bundle:list_agent-core"
        )

    def test_original_declaration_not_mutated(self, translator):
        tool = _InlineTool("bundle:list_x")
        shape = tool.get_provider_format("openai")
        config = _FakeConfig(custom_tools=[tool])
        translator.build_provider_tools(config, "openai")
        # the tool's own formatter output is rebuilt per call; the seam must
        # copy-on-rewrite, never mutate the dict it was handed
        assert shape["name"] == "bundle:list_x"


# ---------------------------------------------------------------------------
# History serializers — replayed blocks always carry the wire form
# ---------------------------------------------------------------------------


class TestHistorySerializers:
    def test_tool_call_content_serializers(self):
        from matrx_ai.config.tools_config import ToolCallContent

        tc = ToolCallContent(id="call_1", name="bundle:list_agent-core", arguments={"a": 1})
        assert tc.wire_name == "bundle__list_agent-core"
        assert tc.to_anthropic()["name"] == "bundle__list_agent-core"
        assert tc.to_google()["functionCall"]["name"] == "bundle__list_agent-core"
        assert tc.to_openai()["name"] == "bundle__list_agent-core"

    def test_tool_call_content_storage_keeps_internal_name(self):
        from matrx_ai.config.tools_config import ToolCallContent

        tc = ToolCallContent(id="call_1", name="bundle:list_agent-core", arguments={})
        # Storage/FE shapes speak internal names — only provider payloads
        # are wire-converted.
        assert tc.to_storage_dict()["name"] == "bundle:list_agent-core"
        assert tc.to_dict()["name"] == "bundle:list_agent-core"

    def test_tool_result_content_google_pairs_with_wire_call_name(self):
        from matrx_ai.config.tools_config import ToolResultContent

        tr = ToolResultContent(
            tool_use_id="call_1", name="bundle:list_agent-core", content="done"
        )
        assert tr.to_google()["functionResponse"]["name"] == "bundle__list_agent-core"

    def test_wire_form_passes_through_unchanged(self):
        from matrx_ai.config.tools_config import ToolCallContent

        tc = ToolCallContent(id="c", name="bundle__list_agent-core", arguments={})
        assert tc.to_anthropic()["name"] == "bundle__list_agent-core"


# ---------------------------------------------------------------------------
# Inbound seam — ToolExecutor._normalize_called_name
# ---------------------------------------------------------------------------


async def _noop_tool(args: dict[str, Any], ctx: Any) -> Any:
    from matrx_ai.tools.models import ToolResult

    return ToolResult(success=True, output={"ok": True}, tool_name=ctx.tool_name)


@pytest.fixture()
def registry_with_lister():
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.register_local(name="bundle:list_agent-core", func=_noop_tool, description="lister")
    registry.register_local(
        name="plain__tool",
        func=_noop_tool,
        description="a legit plain name containing a double underscore",
    )
    yield registry
    registry.clear()


@pytest.fixture()
def executor(registry_with_lister):
    from matrx_ai.tools.executor import ToolExecutor

    return ToolExecutor(registry=registry_with_lister)


class _NullEmitter:
    def __getattr__(self, _name: str):
        async def _noop(*_a: Any, **_kw: Any) -> None: ...

        return _noop


@pytest.fixture()
def app_ctx_set():
    """Set an AppContext so dispatch-path context reads don't blow up."""
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)
    token = set_app_context(ctx)
    yield ctx
    clear_app_context(token)


class TestInboundSeam:
    def test_wire_name_normalizes_to_canonical(self, executor):
        assert (
            executor._normalize_called_name("bundle__list_agent-core")
            == "bundle:list_agent-core"
        )

    def test_direct_registry_hit_wins_over_reversal(self, executor):
        # 'plain__tool' exists verbatim — never rewrite it, even though it
        # contains the wire separator.
        assert executor._normalize_called_name("plain__tool") == "plain__tool"

    def test_plain_name_passthrough(self, executor):
        assert executor._normalize_called_name("web_search") == "web_search"

    def test_unknown_wire_name_passthrough(self, executor):
        # Unresolvable stays as-called; the not-found path downstream owns
        # the error reporting.
        assert executor._normalize_called_name("ghost__tool") == "ghost__tool"

    @pytest.mark.asyncio
    async def test_allowlist_accepts_wire_call_for_canonical_entry(
        self, executor, app_ctx_set
    ):
        """The full regression: the model calls the wire name of a canonical
        colon-named tool that IS in the allowed set (stored canonically).
        The call must clear the allowlist and resolve to the canonical
        tool_def — the exact flow that 400'd /ai/manual before the fix."""
        from matrx_ai.tools.models import ToolContext

        ctx = ToolContext(call_id="call_x", tool_name="bundle__list_agent-core")
        content, result = await executor.execute(
            "bundle__list_agent-core",
            {},
            ctx,
            client_tools=None,
            allowed_tools=frozenset({"bundle:list_agent-core"}),
        )
        # It must NOT be rejected pre-dispatch: not_allowed / not_found are
        # the two failure modes this seam eliminates. (The call itself fails
        # later at the DB layer in this test env — that's fine; the seam's
        # job ends at resolution.)
        err_type = getattr(result.error, "error_type", None)
        assert err_type not in ("not_allowed", "not_found")
        assert result.tool_name != ""

    @pytest.mark.asyncio
    async def test_unlisted_tool_still_rejected_without_error_log(
        self, executor, caplog
    ):
        from matrx_ai.tools.models import ToolContext

        ctx = ToolContext(call_id="call_y", tool_name="bundle__list_agent-core")
        with caplog.at_level("WARNING"):
            _content, result = await executor.execute(
                "bundle__list_agent-core",
                {},
                ctx,
                client_tools=None,
                allowed_tools=frozenset({"something_else"}),
            )
        assert result.error is not None
        assert result.error.error_type == "not_allowed"
        matching = [
            record
            for record in caplog.records
            if "was not in the allowed set" in record.getMessage()
        ]
        assert matching
        assert all(record.levelname == "WARNING" for record in matching)


# ---------------------------------------------------------------------------
# Second layer — outbound payload observer
# ---------------------------------------------------------------------------


class TestPayloadObserver:
    def test_flags_unserializable_declaration_name(self):
        from matrx_ai.tools.validate import inspect_outbound_payload

        payload = {"tools": [{"type": "function", "name": "bundle:list_agent-core"}]}
        assert inspect_outbound_payload(payload) is False

    def test_clean_payload_passes(self):
        from matrx_ai.tools.validate import inspect_outbound_payload

        payload = {"tools": [{"type": "function", "name": "bundle__list_agent-core"}]}
        assert inspect_outbound_payload(payload) is True

    def test_schema_internals_never_trip_the_check(self):
        from matrx_ai.tools.validate import inspect_outbound_payload

        # An arbitrary "name" string inside a parameters schema (here a
        # default value with a space) is NOT a declaration name.
        payload = {
            "tools": [
                {
                    "type": "function",
                    "name": "ok_tool",
                    "parameters": {
                        "properties": {"who": {"type": "string", "default": {"name": "Jane Doe"}}}
                    },
                }
            ]
        }
        assert inspect_outbound_payload(payload) is True

    def test_google_nested_declarations_checked(self):
        from matrx_ai.tools.validate import inspect_outbound_payload

        payload = {
            "tools": [{"function_declarations": [{"name": "bundle:list_x", "parameters": {}}]}]
        }
        assert inspect_outbound_payload(payload) is False

    def test_google_pydantic_config_shape_is_inspected(self):
        """Google's literal payload nests tools as pydantic objects at
        payload['config'].tools — the observer must not go blind there."""
        from types import SimpleNamespace

        from matrx_ai.tools.validate import inspect_outbound_payload

        fn = SimpleNamespace(name="bundle:list_x")
        tool = SimpleNamespace(function_declarations=[fn])
        cfg = SimpleNamespace(tools=[tool])
        assert inspect_outbound_payload({"model": "gemini", "config": cfg}) is False

        good_cfg = SimpleNamespace(
            tools=[SimpleNamespace(function_declarations=[SimpleNamespace(name="ok_tool")])]
        )
        assert inspect_outbound_payload({"model": "gemini", "config": good_cfg}) is True

    def test_xai_protobuf_like_shape_is_inspected(self):
        """xAI tools are protobuf messages with .function.name — attribute
        access must cover them."""
        from types import SimpleNamespace

        from matrx_ai.tools.validate import inspect_outbound_payload

        decl = SimpleNamespace(function=SimpleNamespace(name="bundle:list_x"))
        assert inspect_outbound_payload({"tools": [decl]}) is False


# ---------------------------------------------------------------------------
# Wire-squatting guards — an inline name may not collide with a registry
# tool's wire form (shadowing at dispatch, process-wide)
# ---------------------------------------------------------------------------


class TestWireSquattingGuards:
    def test_ensure_registered_refuses_wire_squatter(self, registry_with_lister):
        with pytest.raises(ValueError, match="wire form"):
            registry_with_lister.ensure_registered(name="bundle__list_agent-core")

    def test_ensure_registered_identity_still_idempotent(self, registry_with_lister):
        # Same exact name → returns the existing entry, no raise.
        td = registry_with_lister.ensure_registered(name="bundle:list_agent-core")
        assert td.name == "bundle:list_agent-core"

    def test_merge_rejects_wire_squatting_inline_spec(self, registry_with_lister):
        from matrx_ai.tools.merge import ToolMergeError, _reject_wire_squatter

        with pytest.raises(ToolMergeError, match="wire form"):
            _reject_wire_squatter("bundle__list_agent-core")
        # Non-colliding names pass silently.
        _reject_wire_squatter("totally_new_tool")
        _reject_wire_squatter("bundle:list_agent-core")  # identity — not a squat

    def test_registry_screams_but_keeps_colliding_db_rows(self, registry_with_lister):
        # Colliding canonical rows loaded from the DB: both stay (refusing one
        # would break a live tool) but the load-time scan must flag them.
        registry_with_lister._tools["bundle__list_agent-core"] = registry_with_lister._tools[
            "bundle:list_agent-core"
        ]
        registry_with_lister._scream_on_wire_collisions()  # must not raise
        assert registry_with_lister.get("bundle__list_agent-core") is not None


# ---------------------------------------------------------------------------
# Delegation checkpoint — wire-called names must match internal client_tools
# ---------------------------------------------------------------------------


class TestDelegationCheckpoint:
    def test_response_has_client_delegated_call_wire_vs_internal(self):
        from matrx_ai.config import TextContent, UnifiedMessage
        from matrx_ai.config.tools_config import ToolCallContent
        from matrx_ai.orchestrator.executor import _response_has_client_delegated_call

        class _Resp:
            def __init__(self, messages):
                self.messages = messages

        # The model can only speak the WIRE form; client_tools holds the
        # internal name. The checkpoint must still fire.
        msg = UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="acme__ask_user", arguments={})],
        )
        assert _response_has_client_delegated_call(
            _Resp([msg]), frozenset({"acme:ask_user"})
        )
        # Plain names keep working.
        msg2 = UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c2", name="take_screenshot", arguments={})],
        )
        assert _response_has_client_delegated_call(
            _Resp([msg2]), frozenset({"take_screenshot"})
        )
        # Non-delegated call → False.
        assert not _response_has_client_delegated_call(
            _Resp([msg2]), frozenset({"other_tool"})
        )
        # Text-only response → False.
        msg3 = UnifiedMessage(role="assistant", content=[TextContent(text="hi")])
        assert not _response_has_client_delegated_call(
            _Resp([msg3]), frozenset({"take_screenshot"})
        )

    def test_live_checkpoint_sees_mid_loop_delegation_update(self):
        from matrx_connect import AppContext
        from matrx_connect.context.app_context import clear_app_context, set_app_context

        from matrx_ai.config import UnifiedMessage
        from matrx_ai.config.tools_config import ToolCallContent
        from matrx_ai.orchestrator.executor import (
            _response_has_live_client_delegated_call,
        )

        class _Resp:
            def __init__(self, messages):
                self.messages = messages

        response = _Resp(
            [
                UnifiedMessage(
                    role="assistant",
                    content=[
                        ToolCallContent(
                            id="dynamic-1",
                            name="new_desktop_tool",
                            arguments={},
                        )
                    ],
                )
            ]
        )
        stale_ctx = AppContext(emitter=None, client_tools=[])
        token = set_app_context(stale_ctx)
        try:
            assert not _response_has_live_client_delegated_call(response)

            # Mirrors drain_pending replacing the request ContextVar while the
            # executor's original exec_ctx object remains unchanged.
            set_app_context(
                stale_ctx.with_overrides(client_tools=["new_desktop_tool"])
            )

            assert stale_ctx.client_tools == []
            assert _response_has_live_client_delegated_call(response)
        finally:
            clear_app_context(token)


# ---------------------------------------------------------------------------
# Undeliverable names fail at the edge, not silently at the boundary
# ---------------------------------------------------------------------------


class TestUndeliverableNameGate:
    def test_wire_overflow_rejected_at_validation(self):
        from matrx_ai.config.custom_tool import CustomTool

        # 64 internal chars, 65 on the wire — can never be declared.
        with pytest.raises(ValueError, match="64-char"):
            CustomTool(name="x" * 62 + ":y")

    def test_boundary_name_accepted(self):
        from matrx_ai.config.custom_tool import CustomTool

        # 63 internal chars with one colon → exactly 64 on the wire: fine.
        CustomTool(name="x" * 61 + ":y")
        CustomTool(name="x" * 64)
