"""Phase A1 tests — ToolSpec discriminated union + merge_request_tools primitive.

Covers spec validation/dispatch and every behavior the merge primitive promises:
no-op idempotence, dedup, conflict detection, exclusion filtering, and the
not-yet-implemented AgentToolSpec error.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect import AppContext
from pydantic import TypeAdapter, ValidationError

from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.merge import ToolMergeError, merge_request_tools
from matrx_ai.tools.models import CustomToolInputSchema
from matrx_ai.tools.specs import (
    AgentToolSpec,
    InlineToolSpec,
    RegisteredToolSpec,
    ToolSpec,
    spec_identity,
)


class _NullEmitter:
    """Minimal stub satisfying the Emitter Protocol shape for tests.

    Production code goes through StreamEmitter / ConsoleEmitter; the merge
    primitive never calls the emitter so a no-op stub is fine.
    """

    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _make_ctx(client_tools: list[str] | None = None) -> AppContext:
    return AppContext(emitter=_NullEmitter(), client_tools=list(client_tools or []))


def _make_config(
    tools: list[str] | None = None,
    custom_tools: list[Any] | None = None,
) -> UnifiedConfig:
    return UnifiedConfig(
        model="test-model",
        messages=MessageList(_messages=[]),
        tools=list(tools or []),
        custom_tools=list(custom_tools or []),
    )


# ---------------------------------------------------------------------------
# ToolSpec discriminated-union parsing
# ---------------------------------------------------------------------------


class TestToolSpecParsing:
    def test_registered_default(self) -> None:
        spec = TypeAdapter(ToolSpec).validate_python({"kind": "registered", "name": "fs_read"})
        assert isinstance(spec, RegisteredToolSpec)
        assert spec.name == "fs_read"
        assert spec.delegate is False
        assert spec.tool_id is None

    def test_registered_with_delegate(self) -> None:
        spec = TypeAdapter(ToolSpec).validate_python(
            {"kind": "registered", "name": "vsc_apply_edit", "delegate": True}
        )
        assert isinstance(spec, RegisteredToolSpec)
        assert spec.delegate is True

    def test_inline_minimal(self) -> None:
        spec = TypeAdapter(ToolSpec).validate_python(
            {
                "kind": "inline",
                "name": "weather_lookup",
                "description": "Looks up the weather",
                "input_schema": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"],
                },
            }
        )
        assert isinstance(spec, InlineToolSpec)
        assert spec.input_schema.properties["city"].type == "string"

    def test_agent_minimal(self) -> None:
        spec = TypeAdapter(ToolSpec).validate_python({"kind": "agent", "agent_id": "abc-123"})
        assert isinstance(spec, AgentToolSpec)
        assert spec.agent_id == "abc-123"

    def test_unknown_kind_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TypeAdapter(ToolSpec).validate_python({"kind": "magic", "name": "unicorn"})

    def test_spec_identity_distinguishes_kinds(self) -> None:
        # Same name, different kinds → different identities (so the merge
        # primitive can detect the conflict at lookup time).
        reg = RegisteredToolSpec(name="foo")
        inl = InlineToolSpec(name="foo")
        assert spec_identity(reg) != spec_identity(inl)


# ---------------------------------------------------------------------------
# merge_request_tools — happy paths
# ---------------------------------------------------------------------------


class TestMergeBasics:
    def test_empty_specs_reconciles_stale_delegation(self) -> None:
        config = _make_config(tools=["pre_existing"])
        ctx = _make_ctx(client_tools=["pre_existing_client"])
        new_ctx = merge_request_tools(config, ctx, [])
        assert config.tools == ["pre_existing"]
        assert new_ctx.client_tools == []

    def test_detached_executor_removes_stale_registered_delegation(self) -> None:
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        saved_tool = registry._tools.get("desktop_only")
        saved_bindings = registry._bindings_by_tool.get("desktop_only")
        try:
            registry._tools["desktop_only"] = ToolDefinition(
                name="desktop_only",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
            registry._bindings_by_tool["desktop_only"] = {"matrx-local"}
            config = _make_config(tools=["desktop_only"])
            attached = merge_request_tools(
                config,
                _make_ctx(),
                [],
                active_executors=frozenset({"matrx-local"}),
            )
            assert attached.client_tools == ["desktop_only"]

            detached = merge_request_tools(config, attached, [])

            assert detached.client_tools == []
            assert config.tools == []  # no viable executor after detach
        finally:
            if saved_tool is None:
                registry._tools.pop("desktop_only", None)
            else:
                registry._tools["desktop_only"] = saved_tool
            if saved_bindings is None:
                registry._bindings_by_tool.pop("desktop_only", None)
            else:
                registry._bindings_by_tool["desktop_only"] = saved_bindings

    def test_reconciliation_retains_preloaded_inline_delegation(self) -> None:
        from matrx_ai.tools.models import CustomTool

        config = _make_config()
        config.custom_tools = [CustomTool(name="inline_existing", description="fixture")]
        ctx = _make_ctx(client_tools=["stale_registered"])

        new_ctx = merge_request_tools(config, ctx, [])

        assert new_ctx.client_tools == ["inline_existing"]

    def test_registered_server_side(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        new_ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="fs_read")])
        assert config.tools == ["fs_read"]
        assert new_ctx.client_tools == []

    def test_registered_delegated(self) -> None:
        """Delegation comes from tool_binding × active_executors — NOT from the
        legacy ``RegisteredToolSpec.delegate`` flag (no longer consulted).

        With a binding to a client executor in this request's active set the
        tool delegates; with an empty active set (server-direct run) the same
        spec stays server-side even with ``delegate=True``.
        """
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        registry._bindings_by_tool["vsc_apply_edit"] = {"matrx-user"}
        try:
            # Active client executor present → delegated.
            config = _make_config()
            ctx = _make_ctx()
            new_ctx = merge_request_tools(
                config,
                ctx,
                [RegisteredToolSpec(name="vsc_apply_edit", delegate=True)],
                active_executors=frozenset({"matrx-user"}),
            )
            assert config.tools == ["vsc_apply_edit"]
            assert new_ctx.client_tools == ["vsc_apply_edit"]

            # No active client executors → server-side despite delegate=True.
            config2 = _make_config()
            ctx2 = _make_ctx()
            new_ctx2 = merge_request_tools(
                config2,
                ctx2,
                [RegisteredToolSpec(name="vsc_apply_edit", delegate=True)],
            )
            assert config2.tools == ["vsc_apply_edit"]
            assert new_ctx2.client_tools == []
        finally:
            registry._bindings_by_tool.pop("vsc_apply_edit", None)

    def test_inline_always_delegated(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        new_ctx = merge_request_tools(
            config,
            ctx,
            [
                InlineToolSpec(
                    name="weather",
                    description="Weather lookup",
                    input_schema={
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"],
                    },
                )
            ],
        )
        assert config.tools == []
        assert len(config.custom_tools) == 1
        assert config.custom_tools[0].name == "weather"
        assert new_ctx.client_tools == ["weather"]

    def test_mixed_specs(self) -> None:
        """Registered tools delegate via tool_binding × active_executors;
        inline tools ALWAYS delegate (no server impl exists for them)."""
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        registry._bindings_by_tool["vsc_apply_edit"] = {"matrx-user"}
        try:
            config = _make_config()
            ctx = _make_ctx()
            new_ctx = merge_request_tools(
                config,
                ctx,
                [
                    RegisteredToolSpec(name="fs_read"),
                    RegisteredToolSpec(name="vsc_apply_edit", delegate=True),
                    InlineToolSpec(name="weather", description="W"),
                ],
                active_executors=frozenset({"matrx-user"}),
            )
            assert config.tools == ["fs_read", "vsc_apply_edit"]
            assert [ct.name for ct in config.custom_tools] == ["weather"]
            assert sorted(new_ctx.client_tools) == ["vsc_apply_edit", "weather"]
        finally:
            registry._bindings_by_tool.pop("vsc_apply_edit", None)


# ---------------------------------------------------------------------------
# Idempotence + dedup
# ---------------------------------------------------------------------------


class TestMergeIdempotence:
    def test_re_merging_same_spec_is_noop(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="fs_read")])
        ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="fs_read")])
        assert config.tools == ["fs_read"]

    def test_dup_within_call_dedupes(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(
            config,
            ctx,
            [RegisteredToolSpec(name="fs_read"), RegisteredToolSpec(name="fs_read")],
        )
        assert config.tools == ["fs_read"]

    def test_identical_inline_redeclaration_is_noop(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(config, ctx, [InlineToolSpec(name="weather", description="A")])
        ctx = merge_request_tools(config, ctx, [InlineToolSpec(name="weather", description="A")])
        assert len(config.custom_tools) == 1
        assert config.custom_tools[0].description == "A"

    def test_conflicting_inline_redeclaration_is_rejected(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(config, ctx, [InlineToolSpec(name="weather", description="A")])
        with pytest.raises(ToolMergeError, match="Tool definition conflict"):
            merge_request_tools(
                config,
                ctx,
                [InlineToolSpec(name="weather", description="B")],
            )

    def test_semantically_equivalent_inline_schema_order_dedupes(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        properties = {"a": {"type": "string"}, "b": {"type": "integer"}}
        ctx = merge_request_tools(
            config,
            ctx,
            [
                InlineToolSpec(
                    name="ordered",
                    description="same",
                    input_schema={
                        "type": "object",
                        "properties": properties,
                        "required": ["a", "b"],
                    },
                )
            ],
        )
        merge_request_tools(
            config,
            ctx,
            [
                InlineToolSpec(
                    name="ordered",
                    description="same",
                    input_schema={
                        "type": "object",
                        "properties": properties,
                        "required": ["b", "a"],
                    },
                )
            ],
        )
        assert [tool.name for tool in config.custom_tools] == ["ordered"]


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------


class TestMergeConflicts:
    def test_kind_conflict_within_call(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        with pytest.raises(ToolMergeError, match="Tool conflict"):
            merge_request_tools(
                config,
                ctx,
                [
                    RegisteredToolSpec(name="foo"),
                    InlineToolSpec(name="foo", description="x"),
                ],
            )

    def test_delegate_flag_difference_is_not_a_conflict(self) -> None:
        """Identity is (key → kind) ONLY. ``delegate`` is no longer part of
        tool identity — the old "same name, different delegate" conflict class
        is structurally impossible. Same-name specs dedupe cleanly; routing is
        decided once from bindings × active executors."""
        config = _make_config()
        ctx = _make_ctx()
        new_ctx = merge_request_tools(
            config,
            ctx,
            [
                RegisteredToolSpec(name="foo", delegate=False),
                RegisteredToolSpec(name="foo", delegate=True),
            ],
        )
        assert config.tools == ["foo"]
        assert new_ctx.client_tools == []  # no bindings, no active executors

    def test_cross_call_kind_conflict(self) -> None:
        config = _make_config(tools=["foo"])
        ctx = _make_ctx()
        with pytest.raises(ToolMergeError):
            merge_request_tools(config, ctx, [InlineToolSpec(name="foo", description="x")])

    def test_cross_call_delegate_flag_is_ignored(self) -> None:
        """A pre-loaded server-side tool re-specified with ``delegate=True``
        dedupes silently — the flag carries no identity and no routing
        authority (bindings × active executors decide, once)."""
        config = _make_config(tools=["foo"])
        ctx = _make_ctx()  # foo is in config.tools but not client_tools → server-executed
        new_ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="foo", delegate=True)])
        assert config.tools == ["foo"]
        assert new_ctx.client_tools == []


# ---------------------------------------------------------------------------
# Exclusion filtering
# ---------------------------------------------------------------------------


class TestMergeExclusion:
    def test_excluded_name_filtered_out(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(
            config,
            ctx,
            [
                RegisteredToolSpec(name="fs_read"),
                RegisteredToolSpec(name="shell_exec"),
            ],
            excluded=["shell_exec"],
        )
        assert config.tools == ["fs_read"]

    def test_excluded_does_not_block_unrelated(self) -> None:
        # Excluding one tool must not prevent another spec from being merged.
        config = _make_config()
        ctx = _make_ctx()
        ctx = merge_request_tools(
            config,
            ctx,
            [
                RegisteredToolSpec(name="shell_exec"),
                RegisteredToolSpec(name="fs_read"),
            ],
            excluded=["shell_exec"],
        )
        assert config.tools == ["fs_read"]


# ---------------------------------------------------------------------------
# AgentToolSpec — phase A1 placeholder
# ---------------------------------------------------------------------------


class TestAgentToolSpecMerge:
    """AgentToolSpec must be pre-resolved by apply_unified_tools before
    reaching the merge primitive. If it leaks through unresolved, the
    primitive surfaces a clear conflict-style error rather than silently
    skipping it."""

    def test_unresolved_agent_spec_raises_merge_error(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        with pytest.raises(ToolMergeError, match="resolve_agent_specs"):
            merge_request_tools(config, ctx, [AgentToolSpec(agent_id="abc-123")])


# ---------------------------------------------------------------------------
# Phase A2 — existing injection paths now route through merge_request_tools
# ---------------------------------------------------------------------------


class TestPhaseA2InjectionRouting:
    """Regression tests for ``inject_editable_tools`` after it was rerouted
    through the merge primitive. The helper's contract (idempotent, name
    dedup, mutates config.tools when needed) must be preserved exactly.

    ``inject_vsc_tool`` was deleted in the cleanup commit — its behavior is
    now covered end-to-end by the editor-state capability tests in
    ``aidream/api/tests/test_request_shape.py``."""

    def test_inject_editable_tools_idempotent_with_ctx(self) -> None:
        from dataclasses import dataclass, field

        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        from matrx_ai.config.message_config import UnifiedMessage
        from matrx_ai.config.structured_input_config import _StructuredInputBase
        from matrx_ai.config.structured_input_resolver import inject_editable_tools

        @dataclass
        class _FakeEditableBlock(_StructuredInputBase):
            type: str = "fake_editable"
            _editable_tools: frozenset[str] = field(
                default=frozenset({"fake_create", "fake_update"}),
                init=False,
                repr=False,
                compare=False,
            )

        block = _FakeEditableBlock(editable=True)
        msg = UnifiedMessage(role="user", content=[block])
        config = _make_config()
        messages = MessageList(_messages=[msg])

        ctx = _make_ctx()
        token = set_app_context(ctx)
        try:
            inject_editable_tools(messages, config)
            assert sorted(config.tools) == ["fake_create", "fake_update"]
            # Second call: idempotent.
            inject_editable_tools(messages, config)
            assert sorted(config.tools) == ["fake_create", "fake_update"]
        finally:
            clear_app_context(token)

    def test_inject_editable_tools_no_editable_blocks_is_noop(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            set_app_context,
        )

        from matrx_ai.config.message_config import UnifiedMessage
        from matrx_ai.config.structured_input_resolver import inject_editable_tools

        msg = UnifiedMessage(role="user", content=[])
        config = _make_config(tools=["pre_existing"])
        messages = MessageList(_messages=[msg])

        token = set_app_context(_make_ctx())
        try:
            inject_editable_tools(messages, config)
            assert config.tools == ["pre_existing"]
        finally:
            clear_app_context(token)

    def test_inject_editable_tools_fallback_without_ctx(self) -> None:
        # When no contextvar is set (raw-test path), helper falls back to
        # direct mutation. Confirms the defensive fallback works.
        from dataclasses import dataclass, field

        from matrx_ai.config.message_config import UnifiedMessage
        from matrx_ai.config.structured_input_config import _StructuredInputBase
        from matrx_ai.config.structured_input_resolver import inject_editable_tools

        @dataclass
        class _FakeEditableBlock(_StructuredInputBase):
            type: str = "fake_editable"
            _editable_tools: frozenset[str] = field(
                default=frozenset({"fake_create"}),
                init=False,
                repr=False,
                compare=False,
            )

        block = _FakeEditableBlock(editable=True)
        msg = UnifiedMessage(role="user", content=[block])
        config = _make_config()
        messages = MessageList(_messages=[msg])

        # No set_app_context — ctx is None.
        inject_editable_tools(messages, config)
        assert config.tools == ["fake_create"]

    # NOTE: inject_vsc_tool was deleted alongside the editor-state capability
    # cutover. The tool_merge.apply_unified_tools tests + the
    # capability-resolution tests cover the same behavior end-to-end.


# ---------------------------------------------------------------------------
# UUID ↔ canonical-name dedup keying
# ---------------------------------------------------------------------------


class TestRegisteredToolSpecResolution:
    """``RegisteredToolSpec.resolved_tool_id()`` is the linchpin: it lets the
    merge primitive treat ``RegisteredToolSpec(name=...)`` and the agent's
    stored UUID as the same logical tool. Without this, the agent's UUID
    and a capability that adds the tool by name both land in
    ``config.tools`` and the API request carries two function declarations
    that resolve to one tool (Anthropic 400 / Gemini 400 / OpenAI silent
    duplicate)."""

    def test_returns_explicit_tool_id_when_set(self) -> None:
        spec = RegisteredToolSpec(name="x", tool_id="11111111-1111-1111-1111-111111111111")
        assert spec.resolved_tool_id() == "11111111-1111-1111-1111-111111111111"

    def test_resolves_name_via_registry(self) -> None:
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        td = ToolDefinition(
            name="resolves_me",
            tool_id="22222222-2222-2222-2222-222222222222",
            description="x",
            tool_type=ToolType.AGENT,  # avoids callable resolution
        )
        registry._tools["resolves_me"] = td
        registry._tools_by_id[td.tool_id] = "resolves_me"
        try:
            spec = RegisteredToolSpec(name="resolves_me")
            assert spec.resolved_tool_id() == "22222222-2222-2222-2222-222222222222"
        finally:
            registry._tools.pop("resolves_me", None)
            registry._tools_by_id.pop("22222222-2222-2222-2222-222222222222", None)

    def test_returns_none_for_unknown_name(self) -> None:
        spec = RegisteredToolSpec(name="never_in_registry_xyz")
        assert spec.resolved_tool_id() is None

    def test_returns_none_for_synthetic_projection_name(self) -> None:
        # custom_tool_N is the synthetic name produced by agent projection
        # (matrx_ai.tools.agent_projection). Never in the global registry
        # by design — its dispatch goes through ctx.metadata's projection map.
        spec = RegisteredToolSpec(name="custom_tool_3")
        assert spec.resolved_tool_id() is None


class TestMergeUuidNameDedup:
    """End-to-end: agent's UUID-form entry + capability's name-form spec
    for the SAME tool collapse to one entry. Reproduces the failure mode
    diagnosed 2026-05-03 from a live Anthropic 400 (``tools: Tool names
    must be unique``)."""

    def test_agent_uuid_dedups_against_capability_name_spec(self) -> None:
        # Stand in for ``load_chrome_tools``: the agent stores it as a
        # UUID (agx_agent.tools is UUIDArrayField), the browser-dom
        # capability's enabled_tools adds it by canonical name.
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        td = ToolDefinition(
            name="load_chrome_tools",
            tool_id="3dd2eef1-212c-4ca2-a128-ec5c95e086de",
            description="x",
            tool_type=ToolType.AGENT,
        )
        registry._tools["load_chrome_tools"] = td
        registry._tools_by_id[td.tool_id] = "load_chrome_tools"
        try:
            # Agent's row.tools landed in config.tools as a UUID.
            config = _make_config(tools=["3dd2eef1-212c-4ca2-a128-ec5c95e086de"])
            ctx = _make_ctx()
            ctx = merge_request_tools(
                config,
                ctx,
                [RegisteredToolSpec(name="load_chrome_tools")],
            )
            # Single entry — the API request will carry one function
            # declaration for this tool, not two.
            assert len(config.tools) == 1, (
                f"expected single tool entry; got {config.tools!r}. "
                f"Duplicate entry → API 400 'tool names must be unique'."
            )
        finally:
            registry._tools.pop("load_chrome_tools", None)
            registry._tools_by_id.pop("3dd2eef1-212c-4ca2-a128-ec5c95e086de", None)

    def test_capability_name_first_then_agent_uuid_also_dedups(self) -> None:
        # Reverse order: name-form added first, then the agent's UUID
        # via a subsequent merge call. Both paths must collapse.
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        td = ToolDefinition(
            name="reverse_order_tool",
            tool_id="44444444-4444-4444-4444-444444444444",
            description="x",
            tool_type=ToolType.AGENT,
        )
        registry._tools["reverse_order_tool"] = td
        registry._tools_by_id[td.tool_id] = "reverse_order_tool"
        try:
            config = _make_config()
            ctx = _make_ctx()
            # First merge: capability adds by name.
            ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="reverse_order_tool")])
            # Second merge (e.g. dynamic injection): same tool by UUID.
            ctx = merge_request_tools(
                config,
                ctx,
                [
                    RegisteredToolSpec(
                        name="reverse_order_tool",
                        tool_id="44444444-4444-4444-4444-444444444444",
                    )
                ],
            )
            assert len(config.tools) == 1
        finally:
            registry._tools.pop("reverse_order_tool", None)
            registry._tools_by_id.pop("44444444-4444-4444-4444-444444444444", None)

    def test_smuggled_excluded_uuid_is_coerced_and_excluded(self) -> None:
        # The smuggle shape: an allowed-looking (unresolvable) name carrying an
        # excluded tool's UUID. The spec is coerced to the canonical name
        # BEFORE the exclusion check, so the tool is properly excluded — the
        # security property holds WITHOUT killing the whole request (the old
        # hard reject 400'd real production calls whose name was simply the
        # UUID — 2026-07-18 /v2/ai/manual incident).
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        tool_id = "66666666-6666-4666-8666-666666666666"
        td = ToolDefinition(
            name="excluded_tool",
            tool_id=tool_id,
            description="x",
            tool_type=ToolType.AGENT,
        )
        registry._tools[td.name] = td
        registry._tools_by_id[tool_id] = td.name
        try:
            config = _make_config()
            merge_request_tools(
                config,
                _make_ctx(),
                [RegisteredToolSpec(name="allowed_alias", tool_id=tool_id)],
                excluded=["excluded_tool"],
            )
            assert "excluded_tool" not in config.tools
            assert tool_id not in config.tools
            assert "allowed_alias" not in config.tools
        finally:
            registry._tools.pop(td.name, None)
            registry._tools_by_id.pop(tool_id, None)

    def test_uuid_as_name_is_reconciled_not_rejected(self) -> None:
        # 2026-07-18 regression: a client sent {name: <uuid>, tool_id: <uuid>}
        # (both the SAME uuid — one tool, unambiguous) and the merge raised
        # "identity mismatch", killing the request. It must coerce to the
        # canonical name and merge normally.
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        tool_id = "670a1fd1-081a-41bc-b5ed-36cebef459f5"
        td = ToolDefinition(
            name="kind_create",
            tool_id=tool_id,
            description="x",
            tool_type=ToolType.AGENT,
        )
        registry._tools[td.name] = td
        registry._tools_by_id[tool_id] = td.name
        try:
            config = _make_config()
            merge_request_tools(
                config,
                _make_ctx(),
                [RegisteredToolSpec(name=tool_id, tool_id=tool_id)],
            )
            assert len(config.tools) == 1
        finally:
            registry._tools.pop(td.name, None)
            registry._tools_by_id.pop(tool_id, None)

    def test_two_different_resolvable_tools_in_one_spec_still_rejected(self) -> None:
        # The ONLY genuine mismatch: name resolves to tool A, tool_id to tool B.
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        td_a = ToolDefinition(
            name="tool_alpha",
            tool_id="77777777-7777-4777-8777-777777777777",
            description="x",
            tool_type=ToolType.AGENT,
        )
        td_b = ToolDefinition(
            name="tool_beta",
            tool_id="88888888-8888-4888-8888-888888888888",
            description="x",
            tool_type=ToolType.AGENT,
        )
        for td in (td_a, td_b):
            registry._tools[td.name] = td
            registry._tools_by_id[td.tool_id] = td.name
        try:
            with pytest.raises(ToolMergeError, match="identity mismatch"):
                merge_request_tools(
                    _make_config(),
                    _make_ctx(),
                    [RegisteredToolSpec(name="tool_alpha", tool_id=td_b.tool_id)],
                )
        finally:
            for td in (td_a, td_b):
                registry._tools.pop(td.name, None)
                registry._tools_by_id.pop(td.tool_id, None)

    def test_unknown_uuid_passthrough_no_crash(self) -> None:
        # Defensive: when the registry can't resolve, fall back to literal
        # string comparison. No crash; both entries pass through.
        config = _make_config(tools=["00000000-0000-0000-0000-000000000000"])
        ctx = _make_ctx()
        ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="some_other_tool")])
        assert "some_other_tool" in config.tools
        assert "00000000-0000-0000-0000-000000000000" in config.tools

    def test_synthetic_projection_name_does_not_collapse_to_real_tools(
        self,
    ) -> None:
        # custom_tool_3 (an agent projection) must NOT accidentally dedup
        # against any real registered tool, because resolved_tool_id()
        # returns None for synthetic names — the dedup key is the bare
        # name, which lives in its own namespace.
        config = _make_config(tools=["any_existing_tool"])
        ctx = _make_ctx()
        ctx = merge_request_tools(config, ctx, [RegisteredToolSpec(name="custom_tool_3")])
        assert "any_existing_tool" in config.tools
        assert "custom_tool_3" in config.tools

    def test_inline_spec_merge_registers_for_dispatch(self) -> None:
        """Step 1 of the dispatch fix: when the merge primitive processes
        an InlineToolSpec, it must also synthesize a registry entry so
        the executor's lookup at dispatch time finds the tool. Without
        this hook the model sees the schema (via translator) but the
        executor 404s with ``Tool 'X' not found in registry`` when the
        model invokes it."""
        from matrx_ai.tools import merge as merge_module
        from matrx_ai.tools.registry import ToolRegistry

        if not merge_module.ENABLE_AUTO_REGISTER_INLINE_TOOLS:
            pytest.skip(
                "Step 1 toggle is OFF — auto-registration of inline tools is "
                "disabled. Re-enable in merge.py to verify the dispatch hook."
            )

        registry = ToolRegistry.get_instance()
        # Confirm baseline — the tool we're about to inline-add doesn't
        # already exist in the registry.
        registry.unregister("inline_dispatch_test_tool")

        config = _make_config()
        ctx = _make_ctx()
        spec = InlineToolSpec(
            name="inline_dispatch_test_tool",
            description="An inline tool that should be registered.",
            input_schema=CustomToolInputSchema(
                properties={"x": {"type": "string"}},
                required=["x"],
            ),
        )
        try:
            ctx = merge_request_tools(config, ctx, [spec])
            # The executor looks up via registry.get(name) — which must
            # succeed now or dispatch will fail.
            tool_def = registry.get("inline_dispatch_test_tool")
            assert tool_def is not None, (
                "merge_request_tools must call ensure_registered for inline "
                "specs so the executor can dispatch them"
            )
            assert tool_def.description == "An inline tool that should be registered."
            assert "x" in tool_def.parameters
            # Inline tools are always client-delegated.
            assert "inline_dispatch_test_tool" in ctx.client_tools
        finally:
            registry.unregister("inline_dispatch_test_tool")

    def test_ensure_registered_is_idempotent(self) -> None:
        """Calling merge twice with the same inline spec doesn't create
        duplicate registry entries or fail. Important because the discovery
        flow can re-add tools across iterations."""
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        registry.unregister("idempotence_test")

        spec = InlineToolSpec(
            name="idempotence_test",
            description="d",
            input_schema=CustomToolInputSchema(),
        )
        try:
            config = _make_config()
            ctx = _make_ctx()
            merge_request_tools(config, ctx, [spec])
            first = registry.get("idempotence_test")
            merge_request_tools(_make_config(), _make_ctx(), [spec])
            second = registry.get("idempotence_test")
            # Same registry entry — ensure_registered did NOT replace it.
            assert first is second
        finally:
            registry.unregister("idempotence_test")

    def test_inline_definition_is_request_local_when_name_is_reused(self) -> None:
        """A global first-seen schema must not leak into a later request."""
        from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
        from matrx_ai.tools.models import ToolDefinition
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        registry.unregister("apply_surface_write")
        first = InlineToolSpec(
            name="apply_surface_write",
            input_schema=CustomToolInputSchema(
                properties={"value": {"type": "string"}}, required=["value"]
            ),
        )
        second = InlineToolSpec(
            name="apply_surface_write",
            input_schema=CustomToolInputSchema(
                properties={
                    "value": {"type": ["string", "number", "boolean", "array", "object", "null"]}
                },
                required=["value"],
            ),
        )
        try:
            first_ctx = merge_request_tools(_make_config(), _make_ctx(), [first])
            second_ctx = merge_request_tools(_make_config(), _make_ctx(), [second])

            assert registry.get("apply_surface_write").parameters["value"]["type"] == "string"
            first_dump = first_ctx.metadata[PROJECTED_AGENT_TOOLS_KEY]["apply_surface_write"]
            second_dump = second_ctx.metadata[PROJECTED_AGENT_TOOLS_KEY]["apply_surface_write"]
            assert ToolDefinition.model_validate(first_dump).parameters["value"]["type"] == "string"
            assert ToolDefinition.model_validate(second_dump).parameters["value"]["type"] == [
                "string",
                "number",
                "boolean",
                "array",
                "object",
                "null",
            ]
            from matrx_connect.context.app_context import clear_app_context, set_app_context

            from matrx_ai.tools.agent_projection import lookup_projected_tool

            token = set_app_context(second_ctx)
            try:
                active = lookup_projected_tool("apply_surface_write")
                assert active is not None
                assert active.content_ir_contracts()[0].json_schema["properties"]["value"] == {
                    "description": ""
                }
            finally:
                clear_app_context(token)
        finally:
            registry.unregister("apply_surface_write")

    def test_deduplicated_inline_definition_still_binds_request_contract(self) -> None:
        """A pre-materialized wire tool must not skip executor-local binding."""
        from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
        from matrx_ai.tools.models import CustomTool, CustomToolInputSchema, ToolDefinition

        schema = CustomToolInputSchema(
            properties={
                "target": {"type": "string", "enum": ["variable_values"]},
                "value": {
                    "type": ["string", "number", "boolean", "array", "object", "null"]
                },
            },
            required=["target", "value"],
        )
        spec = InlineToolSpec(
            name="apply_surface_write",
            description="Write the selected surface value.",
            input_schema=schema,
        )
        config = _make_config()
        config.custom_tools = [
            CustomTool(
                name=spec.name,
                description=spec.description,
                input_schema=schema,
            )
        ]

        ctx = merge_request_tools(config, _make_ctx(), [spec])

        assert len(config.custom_tools) == 1
        dumped = ctx.metadata[PROJECTED_AGENT_TOOLS_KEY][spec.name]
        contract = ToolDefinition.model_validate(dumped).content_ir_contracts()[0]
        from matrx_graph.contract_kinds import check_schema

        verdict = check_schema(
            {"target": "variable_values", "value": {}},
            contract.json_schema,
        )
        assert verdict.errors == []

    def test_ensure_registered_does_not_clobber_existing_definition(self) -> None:
        """If a tool with the same name was already loaded from the DB at
        startup (a real registered tool with description, callable,
        function_path, etc.), ensure_registered MUST keep that entry —
        not overwrite it with a synthesized stub."""
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        real_tool = ToolDefinition(
            name="preexisting_real_tool",
            description="Real tool from DB.",
            tool_type=ToolType.AGENT,  # avoids callable resolution
        )
        registry.register(real_tool)
        try:
            inline_spec = InlineToolSpec(
                name="preexisting_real_tool",
                description="DIFFERENT INLINE DESCRIPTION",
                input_schema=CustomToolInputSchema(),
            )
            config = _make_config()
            ctx = _make_ctx()
            merge_request_tools(config, ctx, [inline_spec])
            after = registry.get("preexisting_real_tool")
            # The original DB-loaded definition must survive.
            assert after is real_tool
            assert after.description == "Real tool from DB."
        finally:
            registry.unregister("preexisting_real_tool")

    def test_spec_identity_uses_uuid_when_resolvable(self) -> None:
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        td = ToolDefinition(
            name="identity_test",
            tool_id="55555555-5555-5555-5555-555555555555",
            description="x",
            tool_type=ToolType.AGENT,
        )
        registry._tools["identity_test"] = td
        registry._tools_by_id[td.tool_id] = "identity_test"
        try:
            spec = RegisteredToolSpec(name="identity_test")
            assert spec_identity(spec) == (
                "registered",
                "55555555-5555-5555-5555-555555555555",
            )
        finally:
            registry._tools.pop("identity_test", None)
            registry._tools_by_id.pop("55555555-5555-5555-5555-555555555555", None)
