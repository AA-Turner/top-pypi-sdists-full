from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from pydantic import ValidationError

from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools._generated_declarations import LoadDesktopToolsArgs
from matrx_ai.tools.dynamic_drain import drain_tool_mutations
from matrx_ai.tools.models import ToolContext


@pytest.mark.parametrize("category", ["desktop", "desktop-web"])
def test_load_desktop_tools_accepts_consolidated_categories(category: str) -> None:
    assert LoadDesktopToolsArgs(category=category).category == category


def test_load_desktop_tools_rejects_retired_category() -> None:
    with pytest.raises(ValidationError):
        LoadDesktopToolsArgs(category="desktop-system")  # type: ignore[arg-type]


def test_bundled_local_host_tool_does_not_require_cloud_binding(monkeypatch) -> None:
    from matrx_ai.tools.implementations import desktop_discovery
    from matrx_ai.tools.models import ToolDefinition, ToolType
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry()
    tool = ToolDefinition(
        name="local_system",
        category="desktop",
        source_kind="matrx_local",
        tool_type=ToolType.EXTERNAL_HANDLER,
    )
    registry.load_from_definitions([tool])
    monkeypatch.setattr(
        ToolRegistry,
        "get_instance",
        classmethod(lambda cls: registry),
    )

    assert desktop_discovery._is_matrx_local_tool(tool) is True


def test_discovery_queues_registry_references(monkeypatch) -> None:
    from matrx_ai.tools.implementations import desktop_discovery
    from matrx_ai.tools.models import ToolDefinition, ToolType
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry()
    tool = ToolDefinition(
        name="local_system",
        description="Inspect the local system",
        parameters={"action": {"type": "string", "required": True}},
        category="desktop",
        source_kind="matrx_local",
        tool_type=ToolType.EXTERNAL_HANDLER,
    )
    registry.load_from_definitions([tool])
    monkeypatch.setattr(
        ToolRegistry,
        "get_instance",
        classmethod(lambda cls: registry),
    )
    queued: dict[str, object] = {}

    def queue_tool_changes(*, add, remove):
        queued["add"] = add
        queued["remove"] = remove

    ctx = SimpleNamespace(
        call_id="call-1",
        queue_tool_changes=queue_tool_changes,
    )
    result = asyncio.run(desktop_discovery.load_desktop_tools({"category": "desktop"}, ctx))

    assert result.success is True
    assert [spec.kind for spec in queued["add"]] == ["registered"]
    assert [spec.name for spec in queued["add"]] == ["local_system"]
    assert queued["remove"] == ["load_desktop_tools"]


@pytest.mark.asyncio
async def test_surface_defaults_survive_desktop_discovery_and_dynamic_drain(
    monkeypatch,
) -> None:
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.implementations import desktop_discovery
    from matrx_ai.tools.merge import ACTIVE_TOOL_EXECUTORS_KEY
    from matrx_ai.tools.models import ToolDefinition, ToolResult, ToolType
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry()
    registry.load_from_definitions(
        [
            ToolDefinition(
                name="local_file",
                description="Work with local files",
                parameters={"action": {"type": "string", "required": True}},
                category="desktop",
                source_kind="matrx_local",
                tool_type=ToolType.EXTERNAL_HANDLER,
            ),
            ToolDefinition(
                name="local_system",
                description="Inspect the local system",
                parameters={"action": {"type": "string", "required": True}},
                category="desktop",
                source_kind="matrx_local",
                tool_type=ToolType.EXTERNAL_HANDLER,
            ),
            ToolDefinition(
                name="local_shell",
                description="Run local shell commands",
                parameters={"command": {"type": "string", "required": True}},
                category="desktop",
                source_kind="matrx_local",
                tool_type=ToolType.EXTERNAL_HANDLER,
            ),
        ]
    )
    registry._bindings_by_tool = {
        "local_file": {"matrx-local"},
        "local_system": {"matrx-local"},
        "local_shell": {"matrx-local"},
    }
    monkeypatch.setattr(
        ToolRegistry,
        "get_instance",
        classmethod(lambda cls: registry),
    )
    desktop_discovery.clear_caches()

    config = UnifiedConfig(
        model="test-model",
        messages=MessageList(_messages=[]),
        tools=["load_desktop_tools", "local_file"],
    )
    app_ctx = AppContext(
        emitter=None,
        # local_system is intentionally ambient delegation state without a
        # matching schema in config. It must not suppress discovery.
        client_tools=["local_file", "local_system"],
        metadata={
            "client_capabilities_payloads": {
                "desktop-native": {"platform": "linux"}
            },
            "hard_excluded_tools": ["local_shell"],
            ACTIVE_TOOL_EXECUTORS_KEY: ["matrx-local"],
        },
    )
    token = set_app_context(app_ctx)
    try:
        result = await desktop_discovery.load_desktop_tools(
            {"category": "desktop"},
            ToolContext(call_id="discover-1", tool_name="load_desktop_tools"),
        )
        app_ctx = await drain_tool_mutations(config, app_ctx)
    finally:
        clear_app_context(token)
        desktop_discovery.clear_caches()

    assert result.success is True
    assert result.output.skipped_policy == ["local_shell"]
    assert result.output.tools_queued == ["local_file", "local_system"]
    assert result.output.queued_count == 2
    assert config.tools == ["local_file", "local_system"]
    assert config.custom_tools == []
    assert app_ctx.client_tools == ["local_file", "local_system"]

    # Pin the final dispatch decision too: the executor must take the delegated
    # path for the newly discovered registry-backed tool.
    delegated: list[str] = []
    executor = ToolExecutor(registry=registry)

    async def fake_delegated(
        tool_def,
        args,
        tool_ctx,
        row_id="",
        *,
        authorization_metadata=None,
    ):
        del authorization_metadata
        delegated.append(tool_def.name)
        return ToolResult(
            success=False,
            delegated_pending=True,
            tool_name=tool_def.name,
            call_id=tool_ctx.call_id,
        )

    monkeypatch.setattr(executor, "_execute_delegated", fake_delegated)
    dispatch_result = await executor._dispatch(
        registry.get("local_system"),
        {},
        ToolContext(call_id="dispatch-1", tool_name="local_system"),
        None,
        frozenset(app_ctx.client_tools),
    )
    assert dispatch_result.delegated_pending is True
    assert delegated == ["local_system"]
