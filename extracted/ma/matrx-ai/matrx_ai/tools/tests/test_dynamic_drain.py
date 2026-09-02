"""Phase D-loop tests — dynamic mid-loop tool injection.

Covers ``ToolContext.queue_tool_changes`` (queues mutations on the
AppContext) and ``drain_tool_mutations`` (the orchestrator's
between-turns drain that applies mutations through the merge primitive
and emits a RESOURCE_CHANGED event).
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.dynamic_drain import drain_tool_mutations
from matrx_ai.tools.models import _PENDING_TOOL_MUTATIONS_KEY, ToolContext
from matrx_ai.tools.specs import InlineToolSpec, RegisteredToolSpec


class _RecordingEmitter:
    """Records every send_resource_changed call so tests can assert events."""

    def __init__(self) -> None:
        self.resource_changed_events: list[dict[str, Any]] = []

    async def send_resource_changed(
        self, *, kind: str, action: str, resource_id: str, **metadata
    ) -> None:
        self.resource_changed_events.append(
            {"kind": kind, "action": action, "resource_id": resource_id, **metadata}
        )

    async def send_chunk(self, *_a, **_kw): ...
    async def send_reasoning_chunk(self, *_a, **_kw): ...
    async def send_data(self, *_a, **_kw): ...
    async def send_phase(self, *_a, **_kw): ...
    async def send_warning(self, *_a, **_kw): ...
    async def send_error(self, *_a, **_kw): ...
    async def send_tool_event(self, *_a, **_kw): ...
    async def fatal_error(self, *_a, **_kw): ...
    async def send_end(self, *_a, **_kw): ...


def _make_config(tools: list[str] | None = None, custom_tools: list | None = None):
    return UnifiedConfig(
        model="test-model",
        messages=MessageList(_messages=[]),
        tools=list(tools or []),
        custom_tools=list(custom_tools or []),
    )


def _make_ctx(emitter=None, conversation_id="conv-123", request_id="req-1"):
    from matrx_connect import AppContext

    return AppContext(
        emitter=emitter or _RecordingEmitter(),
        conversation_id=conversation_id,
        request_id=request_id,
    )


# ---------------------------------------------------------------------------
# ToolContext.queue_tool_changes
# ---------------------------------------------------------------------------

class TestQueueToolChanges:
    def test_queue_add_writes_to_metadata(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        ctx = _make_ctx()
        token = set_app_context(ctx)
        try:
            tc = ToolContext(call_id="call-1", tool_name="discovery")
            tc.queue_tool_changes(
                add=[
                    RegisteredToolSpec(name="dom_query"),
                    InlineToolSpec(name="custom_thing", description="x"),
                ]
            )
            current = get_app_context()
            pending = current.metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending is not None
            assert pending[0]["action"] == "add"
            assert len(pending[0]["specs"]) == 2
            assert pending[0]["by"] == "discovery"
        finally:
            clear_app_context(token)

    def test_queue_remove_writes_to_metadata(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        ctx = _make_ctx()
        token = set_app_context(ctx)
        try:
            tc = ToolContext(call_id="call-1", tool_name="discovery")
            tc.queue_tool_changes(remove=["self_destruct", "old_tool"])
            current = get_app_context()
            pending = current.metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending is not None
            assert pending[0]["action"] == "remove"
            assert pending[0]["names"] == ["self_destruct", "old_tool"]
        finally:
            clear_app_context(token)

    def test_queue_empty_is_noop(self) -> None:
        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        ctx = _make_ctx()
        token = set_app_context(ctx)
        try:
            tc = ToolContext(call_id="call-1", tool_name="t")
            tc.queue_tool_changes()
            assert _PENDING_TOOL_MUTATIONS_KEY not in get_app_context().metadata
        finally:
            clear_app_context(token)

    def test_queue_without_app_context_is_safe(self) -> None:
        # Tool runs outside any request scope (test path) — must not crash.
        tc = ToolContext(call_id="call-1", tool_name="t")
        tc.queue_tool_changes(add=[RegisteredToolSpec(name="foo")])  # no exception

    async def test_queue_propagates_across_asyncio_gather_child_task(self) -> None:
        """Regression: ToolExecutor runs tools inside asyncio.gather, which
        creates child Tasks. Each Task gets its own contextvars snapshot at
        creation, so calling set_app_context from inside a tool would only
        update the child's snapshot — the parent (orchestrator) wouldn't see
        the queue when drain runs on the next iteration. queue_tool_changes
        MUST mutate the shared metadata dict in place.

        Symptom of the regression: Chrome extension's load_chrome_tools
        called repeatedly because the model never sees loaded tools.
        Diagnosed 2026-05-03 from a 34-iteration trace.
        """
        import asyncio

        from matrx_connect.context.app_context import (
            clear_app_context,
            get_app_context,
            set_app_context,
        )

        ctx = _make_ctx()
        token = set_app_context(ctx)
        try:
            async def _child_tool() -> None:
                # Mirrors what asyncio.gather does in ToolExecutor: each
                # tool call runs in a Task with its own contextvars snapshot.
                tc = ToolContext(call_id="child-call", tool_name="child_discovery")
                tc.queue_tool_changes(
                    add=[RegisteredToolSpec(name="child_loaded_tool")]
                )

            # Spawn as an actual Task (not just an awaitable) so the contextvar
            # snapshot semantics kick in — same shape as asyncio.gather.
            await asyncio.gather(asyncio.create_task(_child_tool()))

            # Parent reads its OWN AppContext. queue_tool_changes mutated the
            # shared metadata dict in place, so the queue must be visible here.
            parent_ctx = get_app_context()
            pending = parent_ctx.metadata.get(_PENDING_TOOL_MUTATIONS_KEY)
            assert pending is not None, (
                "Parent task did not see the queue — queue_tool_changes "
                "regressed to building a new metadata dict via with_overrides, "
                "which only updates the child's snapshot."
            )
            assert pending[0]["action"] == "add"
            assert pending[0]["specs"][0]["name"] == "child_loaded_tool"
        finally:
            clear_app_context(token)


# ---------------------------------------------------------------------------
# drain_tool_mutations
# ---------------------------------------------------------------------------

class TestDrainToolMutations:
    async def test_no_pending_is_noop(self) -> None:
        config = _make_config()
        ctx = _make_ctx()
        new_ctx = await drain_tool_mutations(config, ctx)
        assert new_ctx is ctx
        assert config.tools == []

    async def test_drain_adds_via_merge_primitive(self) -> None:
        emitter = _RecordingEmitter()
        ctx = _make_ctx(emitter=emitter)
        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {
                    "action": "add",
                    "specs": [{"kind": "registered", "name": "dom_query"}],
                    "by": "discovery",
                },
            ],
        })

        config = _make_config()
        new_ctx = await drain_tool_mutations(config, ctx)

        # Tool added.
        assert config.tools == ["dom_query"]
        assert config.dynamic_tools == ["dom_query"]
        # Queue cleared.
        assert _PENDING_TOOL_MUTATIONS_KEY not in (new_ctx.metadata or {})
        # RESOURCE_CHANGED event emitted with kind=active_tools.
        assert len(emitter.resource_changed_events) == 1
        evt = emitter.resource_changed_events[0]
        assert evt["kind"] == "active_tools"
        assert evt["action"] == "invalidated"
        # New enriched payload: actual tool names + active_count post-drain.
        assert evt["metadata"]["added_tools"] == ["dom_query"]
        assert evt["metadata"]["removed_tools"] == []
        assert evt["metadata"]["active_count"] == 1
        # Back-compat scalars retained for older consumers.
        assert evt["metadata"]["added"] == 1
        assert evt["metadata"]["removed"] == 0

    async def test_drain_preserves_host_resolved_executor_routing(self) -> None:
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        saved_tools = dict(registry._tools)
        saved_bindings = dict(registry._bindings_by_tool)
        try:
            registry._tools["dynamic_client_tool"] = ToolDefinition(
                name="dynamic_client_tool",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
            registry._bindings_by_tool["dynamic_client_tool"] = {"matrx-local"}
            ctx = _make_ctx().with_overrides(
                metadata={
                    ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-local"],
                    _PENDING_TOOL_MUTATIONS_KEY: [
                        {
                            "action": "add",
                            "specs": [
                                {"kind": "registered", "name": "dynamic_client_tool"}
                            ],
                            "by": "discovery",
                        }
                    ],
                }
            )

            config = _make_config()
            new_ctx = await drain_tool_mutations(config, ctx)

            assert config.tools == ["dynamic_client_tool"]
            assert config.dynamic_tools == ["dynamic_client_tool"]
            assert new_ctx.client_tools == ["dynamic_client_tool"]
        finally:
            registry._tools = saved_tools
            registry._bindings_by_tool = saved_bindings

    async def test_drain_event_reports_applied_changes_not_queued_dedup(self) -> None:
        emitter = _RecordingEmitter()
        ctx = _make_ctx(emitter=emitter).with_overrides(
            metadata={
                _PENDING_TOOL_MUTATIONS_KEY: [
                    {
                        "action": "add",
                        "specs": [
                            {"kind": "registered", "name": "already_active"},
                            {"kind": "registered", "name": "newly_active"},
                        ],
                        "by": "discovery",
                    }
                ]
            }
        )
        config = _make_config(tools=["already_active"])

        await drain_tool_mutations(config, ctx)

        metadata = emitter.resource_changed_events[0]["metadata"]
        assert metadata["added_tools"] == ["newly_active"]
        assert metadata["added"] == 1
        assert metadata["active_count"] == 2

    async def test_drain_payload_carries_remove_names(self) -> None:
        emitter = _RecordingEmitter()
        ctx = _make_ctx(emitter=emitter)
        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {
                    "action": "add",
                    "specs": [
                        {"kind": "registered", "name": "click_element"},
                        {"kind": "registered", "name": "type_into_element"},
                    ],
                    "by": "load_chrome_tools",
                },
                {
                    "action": "remove",
                    "names": ["load_chrome_tools"],
                    "by": "load_chrome_tools",
                },
            ],
        })

        config = _make_config(tools=["load_chrome_tools", "fs_read"])
        await drain_tool_mutations(config, ctx)

        assert len(emitter.resource_changed_events) == 1
        meta = emitter.resource_changed_events[0]["metadata"]
        assert meta["added_tools"] == ["click_element", "type_into_element"]
        assert meta["removed_tools"] == ["load_chrome_tools"]
        # Active count: fs_read kept + 2 added = 3.
        assert meta["active_count"] == 3

    async def test_consecutive_drains_emit_one_event_each(self) -> None:
        # Two distinct drain calls in the same request — each non-empty drain
        # produces exactly one event, never coalesced.
        emitter = _RecordingEmitter()
        ctx = _make_ctx(emitter=emitter)
        config = _make_config()

        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {"action": "add", "specs": [{"kind": "registered", "name": "tool_a"}]},
            ],
        })
        ctx = await drain_tool_mutations(config, ctx)

        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {"action": "add", "specs": [{"kind": "registered", "name": "tool_b"}]},
            ],
        })
        await drain_tool_mutations(config, ctx)

        assert len(emitter.resource_changed_events) == 2
        assert emitter.resource_changed_events[0]["metadata"]["added_tools"] == ["tool_a"]
        assert emitter.resource_changed_events[1]["metadata"]["added_tools"] == ["tool_b"]
        # Active_count is cumulative across drains because config persists.
        assert emitter.resource_changed_events[0]["metadata"]["active_count"] == 1
        assert emitter.resource_changed_events[1]["metadata"]["active_count"] == 2

    async def test_drain_removes_first_then_adds(self) -> None:
        # Remove + add of the same name in one drain → end state has the new
        # spec, no merge conflict (because remove cleared the slot first).
        ctx = _make_ctx()
        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {"action": "add", "specs": [{"kind": "registered", "name": "swap_me"}]},
                {"action": "remove", "names": ["swap_me"]},
            ],
        })

        config = _make_config(tools=["swap_me"])
        await drain_tool_mutations(config, ctx)

        # Removal happens first; then the add re-introduces it.
        assert config.tools == ["swap_me"]

    async def test_drain_self_removing_discovery_tool(self) -> None:
        # The Chrome-extension pattern: discovery tool adds 5 tools and
        # removes itself in one mutation.
        ctx = _make_ctx()
        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {
                    "action": "add",
                    "specs": [
                        {"kind": "registered", "name": "dom_query"},
                        {"kind": "registered", "name": "dom_click"},
                        {"kind": "registered", "name": "dom_fill"},
                    ],
                    "by": "load_chrome_tools",
                },
                {"action": "remove", "names": ["load_chrome_tools"], "by": "load_chrome_tools"},
            ],
        })

        config = _make_config(tools=["load_chrome_tools", "fs_read"])
        await drain_tool_mutations(config, ctx)

        # Discovery tool removed; relevant tools loaded; unrelated tools kept.
        assert "load_chrome_tools" not in config.tools
        assert "dom_query" in config.tools
        assert "dom_click" in config.tools
        assert "dom_fill" in config.tools
        assert "fs_read" in config.tools

    async def test_drain_emits_no_event_when_nothing_changed(self) -> None:
        # Empty pending list: no event.
        emitter = _RecordingEmitter()
        ctx = _make_ctx(emitter=emitter)
        config = _make_config()
        await drain_tool_mutations(config, ctx)
        assert emitter.resource_changed_events == []

    async def test_drain_invalid_spec_kind_raises(self) -> None:
        from matrx_ai.tools.merge import ToolMergeError

        ctx = _make_ctx()
        ctx = ctx.with_overrides(metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {"action": "add", "specs": [{"kind": "magic", "name": "?"}]},
            ],
        })
        config = _make_config()
        with pytest.raises(ToolMergeError, match="unknown ToolSpec kind"):
            await drain_tool_mutations(config, ctx)


class TestExecutorViabilityOnDynamicAdds:
    """Regression tests for the 2026-08-21 stuck-'delegated' incident: a
    matrx-user/chat request loaded chrome-extension-only tools (queued as
    inline specs by a discovery tool) and `navigate` delegated to a client
    that could never answer, pausing the user request until the 30-day
    abandonment sweep."""

    async def test_inline_spec_shadowing_bound_client_tool_is_dropped(self) -> None:
        """An inline spec whose name matches a registry row bound to a
        client executor that is NOT live must be dropped, not delegated."""
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        saved_tools = dict(registry._tools)
        saved_bindings = dict(registry._bindings_by_tool)
        try:
            registry._tools["ext_navigate"] = ToolDefinition(
                name="ext_navigate",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
            registry._bindings_by_tool["ext_navigate"] = {"chrome-extension"}
            ctx = _make_ctx().with_overrides(
                metadata={
                    ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-user"],
                    _PENDING_TOOL_MUTATIONS_KEY: [
                        {
                            "action": "add",
                            "specs": [
                                {
                                    "kind": "inline",
                                    "name": "ext_navigate",
                                    "description": "navigate somewhere",
                                    "input_schema": {
                                        "type": "object",
                                        "properties": {},
                                    },
                                }
                            ],
                            "by": "load_chrome_tools",
                        }
                    ],
                }
            )

            config = _make_config()
            new_ctx = await drain_tool_mutations(config, ctx)

            assert "ext_navigate" not in [ct.name for ct in config.custom_tools]
            assert "ext_navigate" not in list(new_ctx.client_tools or [])
        finally:
            registry._tools = saved_tools
            registry._bindings_by_tool = saved_bindings

    async def test_inline_spec_with_live_client_executor_still_delegates(self) -> None:
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY
        from matrx_ai.tools.models import ToolDefinition, ToolType
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        saved_tools = dict(registry._tools)
        saved_bindings = dict(registry._bindings_by_tool)
        try:
            registry._tools["ext_navigate2"] = ToolDefinition(
                name="ext_navigate2",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
            registry._bindings_by_tool["ext_navigate2"] = {"chrome-extension"}
            ctx = _make_ctx().with_overrides(
                metadata={
                    ACTIVE_TOOL_EXECUTORS_KEY: ["chrome-extension"],
                    _PENDING_TOOL_MUTATIONS_KEY: [
                        {
                            "action": "add",
                            "specs": [
                                {
                                    "kind": "inline",
                                    "name": "ext_navigate2",
                                    "description": "navigate somewhere",
                                    "input_schema": {
                                        "type": "object",
                                        "properties": {},
                                    },
                                }
                            ],
                            "by": "load_chrome_tools",
                        }
                    ],
                }
            )

            config = _make_config()
            new_ctx = await drain_tool_mutations(config, ctx)

            assert "ext_navigate2" in list(new_ctx.client_tools or [])
        finally:
            registry._tools = saved_tools
            registry._bindings_by_tool = saved_bindings

    async def test_ad_hoc_inline_spec_without_registry_row_still_delegates(self) -> None:
        """Genuinely caller-authored inline tools (no registry bindings) keep
        the historical unconditional-delegate behavior."""
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY

        ctx = _make_ctx().with_overrides(
            metadata={
                ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-user"],
                _PENDING_TOOL_MUTATIONS_KEY: [
                    {
                        "action": "add",
                        "specs": [
                            {
                                "kind": "inline",
                                "name": "my_custom_widget",
                                "description": "caller-authored",
                                "input_schema": {"type": "object", "properties": {}},
                            }
                        ],
                        "by": "request",
                    }
                ],
            }
        )
        config = _make_config()
        new_ctx = await drain_tool_mutations(config, ctx)
        assert "my_custom_widget" in list(new_ctx.client_tools or [])


class TestRequiresClientExecutorGate:
    """The `requires_client_executor` gating entry drops a server-implemented
    loader tool whose payload is client-only (load_chrome_tools) on requests
    where that client executor isn't live."""

    def _fixture_tool(self, registry, name: str) -> None:
        from matrx_ai.tools.models import ToolDefinition, ToolType

        registry._tools[name] = ToolDefinition(
            name=name,
            description="loader fixture",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path="pkg.mod.fn",
            gating=[
                {
                    "gate": "requires_client_executor",
                    "args": {"executor": "chrome-extension"},
                }
            ],
        )
        registry._bindings_by_tool[name] = {"matrx-ai-core"}

    async def test_dropped_when_required_executor_not_live(self) -> None:
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY, merge_request_tools
        from matrx_ai.tools.registry import ToolRegistry
        from matrx_ai.tools.specs import RegisteredToolSpec

        registry = ToolRegistry.get_instance()
        saved_tools = dict(registry._tools)
        saved_bindings = dict(registry._bindings_by_tool)
        try:
            self._fixture_tool(registry, "loader_gated")
            ctx = _make_ctx().with_overrides(
                metadata={ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-user"]}
            )
            config = _make_config()
            merge_request_tools(config, ctx, [RegisteredToolSpec(name="loader_gated")])
            assert "loader_gated" not in config.tools
        finally:
            registry._tools = saved_tools
            registry._bindings_by_tool = saved_bindings

    async def test_kept_when_required_executor_live(self) -> None:
        from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY, merge_request_tools
        from matrx_ai.tools.registry import ToolRegistry
        from matrx_ai.tools.specs import RegisteredToolSpec

        registry = ToolRegistry.get_instance()
        saved_tools = dict(registry._tools)
        saved_bindings = dict(registry._bindings_by_tool)
        try:
            self._fixture_tool(registry, "loader_gated2")
            ctx = _make_ctx().with_overrides(
                metadata={ACTIVE_TOOL_EXECUTORS_KEY: ["chrome-extension.pilot"]}
            )
            config = _make_config()
            merge_request_tools(config, ctx, [RegisteredToolSpec(name="loader_gated2")])
            assert "loader_gated2" in config.tools
        finally:
            registry._tools = saved_tools
            registry._bindings_by_tool = saved_bindings
