"""Regression tests for the single delegation authority + name-only merge identity.

Pins the bug class fixed by the delegation-authority refactor:
  - The same tool arriving from two sources with different ``delegate`` intents
    must NOT raise ToolMergeError (delegate left tool identity; identity = kind).
  - server-vs-client routing is decided ONCE by
    ``ToolRegistry.resolve_executor_binding`` from the request's active
    executor set — empty set (no-client / server run) => everything server-side.

The new schema stores bindings in ``tool_binding`` rows (tool_name →
{executor_name, ...}) and the registry exposes them via
``ToolRegistry.bindings_for_tool``. ``resolve_executor_binding`` returns
``"surface"`` when one of the tool's bindings is a CLIENT executor that's
in the request's ``active_executors`` set.
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.merge import ToolMergeError, merge_request_tools
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.specs import InlineToolSpec, RegisteredToolSpec

UPDATE_PLAN_ID = "11111111-1111-1111-1111-111111111111"

# matrx-user is a canonical CLIENT executor; matrx-ai-core is a SERVER one.
WEB_EXECUTOR = "matrx-user"
SERVER_EXECUTOR = "matrx-ai-core"
EXTENSION_EXECUTOR = "chrome-extension"


def _registry_with_update_plan() -> ToolRegistry:
    reg = ToolRegistry.get_instance()
    reg.clear()
    reg.load_from_definitions(
        [
            ToolDefinition(
                name="update_plan",
                description="x",
                parameters={},
                tool_type=ToolType.EXTERNAL_HANDLER,
                tool_id=UPDATE_PLAN_ID,
            ),
            ToolDefinition(
                name="memory",
                description="x",
                parameters={},
                tool_type=ToolType.EXTERNAL_HANDLER,
                tool_id="22222222-2222-2222-2222-222222222222",
            ),
        ]
    )
    # update_plan is bound to the matrx-user web client; memory has only a
    # server binding (no client delegation possible).
    reg._bindings_by_tool = {
        "update_plan": {WEB_EXECUTOR, SERVER_EXECUTOR},
        "memory": {SERVER_EXECUTOR},
    }
    return reg


def _ctx() -> AppContext:
    return AppContext(emitter=None, client_tools=[])


def test_resolve_executor_binding_is_the_single_authority() -> None:
    reg = _registry_with_update_plan()

    # No connecting client => everything server-side (no hang on workflow runs).
    assert reg.resolve_executor_binding("update_plan", set()) == "server"
    # Web client is active → update_plan routes client-side.
    assert reg.resolve_executor_binding("update_plan", {WEB_EXECUTOR}) == "surface"
    # A different client executor that's NOT in update_plan's bindings →
    # falls back to server.
    assert reg.resolve_executor_binding("update_plan", {EXTENSION_EXECUTOR}) == "server"
    # memory has no client binding — always server.
    assert reg.resolve_executor_binding("memory", {WEB_EXECUTOR}) == "server"


def test_two_sources_with_conflicting_delegate_do_not_raise() -> None:
    """The exact repro: update_plan pre-loaded on the agent (delegate=False) AND
    arriving as a surface default (delegate=True). Old code raised
    ToolMergeError; now identity is name-only so it dedups."""
    _registry_with_update_plan()
    config = UnifiedConfig(
        model="gpt-4.1-mini", messages=[], tools=[UPDATE_PLAN_ID], custom_tools=[]
    )
    ctx = _ctx()

    ctx = merge_request_tools(
        config,
        ctx,
        [
            RegisteredToolSpec(name="update_plan", delegate=True),
            RegisteredToolSpec(name="update_plan", delegate=False),
        ],
        active_executors=frozenset({WEB_EXECUTOR}),
    )

    # No conflict, and the single pass delegated it to the web client.
    assert "update_plan" in (ctx.client_tools or [])
    # config.tools still references the one tool (deduped).
    assert config.tools.count(UPDATE_PLAN_ID) <= 1


def test_no_active_client_means_no_delegation() -> None:
    _registry_with_update_plan()
    config = UnifiedConfig(
        model="gpt-4.1-mini", messages=[], tools=[UPDATE_PLAN_ID], custom_tools=[]
    )
    ctx = _ctx()

    ctx = merge_request_tools(
        config,
        ctx,
        [RegisteredToolSpec(name="update_plan", delegate=True)],
        active_executors=frozenset(),
    )

    # Empty active executors => server-side => NOT in client_tools.
    assert "update_plan" not in (ctx.client_tools or [])


def test_followup_merges_inherit_request_active_executors_from_context() -> None:
    """A later context/structured-input merge must not detach live client tools."""
    _registry_with_update_plan()
    config = UnifiedConfig(
        model="gpt-4.1-mini", messages=[], tools=[UPDATE_PLAN_ID], custom_tools=[]
    )
    ctx = AppContext(
        emitter=None,
        client_tools=["update_plan"],
        metadata={"active_tool_executors": [WEB_EXECUTOR]},
    )

    inherited = merge_request_tools(config, ctx, [])
    assert inherited.client_tools == ["update_plan"]

    detached = merge_request_tools(
        config,
        inherited,
        [],
        active_executors=frozenset(),
    )
    assert detached.client_tools == []


def test_executor_viability_filter_restores_only_when_executor_policy_changes() -> None:
    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="desktop_only",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            ),
            ToolDefinition(
                name="server_tool",
                description="fixture",
                parameters={},
                tool_type=ToolType.EXTERNAL_HANDLER,
            ),
        ]
    )
    registry._bindings_by_tool = {"desktop_only": {"matrx-local"}}
    config = UnifiedConfig(
        model="test-model",
        messages=[],
        tools=["desktop_only", "server_tool"],
    )

    detached = merge_request_tools(config, _ctx(), [], active_executors=frozenset())
    assert config.tools == ["server_tool"]
    assert config.tool_delegation_filtered is True
    assert config.tool_delegation_executors == []

    # Same request/policy: a dynamic removal remains removed rather than being
    # resurrected from the authored declaration on every merge call.
    config.tools.remove("server_tool")
    merge_request_tools(config, detached, [], active_executors=frozenset())
    assert config.tools == []

    stored = config.to_storage_dict()
    restored = UnifiedConfig.from_dict(
        {
            "model": stored["model"],
            "system_instruction": stored["system_instruction"],
            "messages": stored["messages"],
            **stored["config"],
        }
    )
    reattached = merge_request_tools(
        restored,
        _ctx(),
        [],
        active_executors=frozenset({"matrx-local"}),
    )
    assert restored.tools == ["desktop_only", "server_tool"]
    assert reattached.client_tools == ["desktop_only"]
    assert restored.tool_delegation_filtered is False


def test_executor_viability_filter_rechecks_registry_binding_changes() -> None:
    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="desktop_only",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
        ]
    )
    registry._bindings_by_tool = {}
    config = UnifiedConfig(model="test-model", messages=[], tools=["desktop_only"])
    active = frozenset({"matrx-local"})

    merge_request_tools(config, _ctx(), [], active_executors=active)
    assert config.tools == []

    # Cache-bust/deploy adds the viable binding while the same desktop remains
    # attached. The registry fingerprint change must re-evaluate authored tools.
    registry._bindings_by_tool = {"desktop_only": {"matrx-local"}}
    rebound = merge_request_tools(config, _ctx(), [], active_executors=active)

    assert config.tools == ["desktop_only"]
    assert rebound.client_tools == ["desktop_only"]


def test_genuine_kind_clash_still_raises() -> None:
    """A name registered as both 'registered' and 'inline' is a real definition
    clash and must still raise (the only remaining ToolMergeError case)."""
    _registry_with_update_plan()
    config = UnifiedConfig(model="gpt-4.1-mini", messages=[], tools=[], custom_tools=[])
    ctx = _ctx()

    # Same name, two kinds, in one merge call: a registered spec and an inline
    # spec for an ad-hoc (unregistered) name both key by name → genuine clash.
    with pytest.raises(ToolMergeError):
        merge_request_tools(
            config,
            ctx,
            [
                RegisteredToolSpec(name="ad_hoc_tool"),
                InlineToolSpec(
                    name="ad_hoc_tool", description="x", input_schema={"type": "object"}
                ),
            ],
        )


def test_tool_merge_error_carries_classified_error_info() -> None:
    err = ToolMergeError("boom")
    assert getattr(err.error_info, "error_type", None) == "tool_merge_error"
    assert err.error_info.user_message  # human-facing, non-empty


@pytest.mark.asyncio
async def test_programmatic_agent_reconciles_policy_before_provider(monkeypatch) -> None:
    from matrx_connect.context.app_context import (
        clear_app_context,
        set_app_context,
        try_get_app_context,
    )

    from matrx_ai.agents import definition
    from matrx_ai.agents.definition import Agent
    from matrx_ai.tools.merge import HARD_EXCLUDED_TOOLS_KEY

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="cloud_file",
                description="x",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="fixture.cloud_file",
            ),
            ToolDefinition(
                name="safe_tool",
                description="x",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="fixture.safe_tool",
            ),
        ]
    )
    captured: dict[str, object] = {}

    async def stop_at_provider(config, **_kwargs):
        captured["tools"] = list(config.tools)
        captured["client_tools"] = list(try_get_app_context().client_tools or [])
        raise RuntimeError("provider-boundary")

    monkeypatch.setattr(definition, "execute_ai_request", stop_at_provider)
    config = UnifiedConfig(
        model="test-model",
        messages=[{"role": "user", "content": "go"}],
        tools=["cloud_file", "safe_tool"],
    )
    ctx = AppContext(
        emitter=None,
        client_tools=["cloud_file", "safe_tool", "stale_tool"],
        metadata={HARD_EXCLUDED_TOOLS_KEY: ["cloud_file"]},
    )
    token = set_app_context(ctx)
    try:
        with pytest.raises(RuntimeError, match="provider-boundary"):
            await Agent(config).execute()
    finally:
        clear_app_context(token)

    assert captured == {"tools": ["safe_tool"], "client_tools": []}


@pytest.mark.asyncio
async def test_programmatic_agent_restores_on_direct_nonempty_policy_transition(
    monkeypatch,
) -> None:
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.agents import definition
    from matrx_ai.agents.definition import Agent
    from matrx_ai.tools.merge import HARD_EXCLUDED_TOOLS_KEY

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name=name,
                description="fixture",
                parameters={},
                tool_type=ToolType.EXTERNAL_HANDLER,
            )
            for name in ("cloud_file", "local_file", "safe_tool")
        ]
    )
    seen: list[list[str]] = []

    async def stop_at_provider(config, **_kwargs):
        seen.append(list(config.tools))
        raise RuntimeError("provider-boundary")

    monkeypatch.setattr(definition, "execute_ai_request", stop_at_provider)
    agent = Agent(
        UnifiedConfig(
            model="test-model",
            messages=[{"role": "user", "content": "go"}],
            tools=["cloud_file", "local_file", "safe_tool"],
        )
    )

    for exclusions in (["cloud_file", "local_file"], ["cloud_file"]):
        token = set_app_context(
            AppContext(
                emitter=None,
                metadata={HARD_EXCLUDED_TOOLS_KEY: exclusions},
            )
        )
        try:
            with pytest.raises(RuntimeError, match="provider-boundary"):
                await agent.execute()
        finally:
            clear_app_context(token)

    assert seen == [["safe_tool"], ["local_file", "safe_tool"]]


@pytest.mark.asyncio
async def test_programmatic_agent_disabled_delegation_wins_over_inherited_executor(
    monkeypatch,
) -> None:
    from matrx_connect.context.app_context import (
        clear_app_context,
        set_app_context,
        try_get_app_context,
    )

    from matrx_ai.agents import definition
    from matrx_ai.agents.definition import Agent
    from matrx_ai.tools.merge import (
        ACTIVE_TOOL_EXECUTORS_KEY,
        CLIENT_DELEGATION_DISABLED_KEY,
    )

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="desktop_only",
                description="fixture",
                parameters={},
                tool_type=ToolType.LOCAL,
                function_path="",
            )
        ]
    )
    registry._bindings_by_tool = {"desktop_only": {"matrx-local"}}
    captured: dict[str, object] = {}

    async def stop_at_provider(config, **_kwargs):
        ctx = try_get_app_context()
        captured["tools"] = list(config.tools)
        captured["custom_tools"] = [tool.name for tool in config.custom_tools]
        captured["client_tools"] = list(ctx.client_tools or [])
        raise RuntimeError("provider-boundary")

    monkeypatch.setattr(definition, "execute_ai_request", stop_at_provider)
    config = UnifiedConfig(
        model="test-model",
        messages=[{"role": "user", "content": "go"}],
        tools=["desktop_only"],
        custom_tools=[
            {
                "name": "inline_only",
                "description": "fixture",
                "input_schema": {"type": "object", "properties": {}},
            }
        ],
    )
    token = set_app_context(
        AppContext(
            emitter=None,
            client_tools=[],
            metadata={
                ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-local"],
                CLIENT_DELEGATION_DISABLED_KEY: True,
            },
        )
    )
    try:
        with pytest.raises(RuntimeError, match="provider-boundary"):
            await Agent(config).execute()
    finally:
        clear_app_context(token)

    assert captured == {"tools": [], "custom_tools": [], "client_tools": []}
    assert config.tool_delegation_filtered is True
