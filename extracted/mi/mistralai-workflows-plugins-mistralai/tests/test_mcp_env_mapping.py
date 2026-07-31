"""Tests for MCPStdioConfig.env_mapping secure credential forwarding (WFL-2091).

The critical invariant: env_mapping lets a stdio MCP subprocess receive secret
credentials (e.g. a Notion bot token) while ONLY the mapping names, never the
secret values, are serialized into Temporal activity params and event history.
The secret is read from the worker's os.environ inside the activity body.
"""

import logging
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai.mcp import (
    CollectMCPToolsParams,
    ExecuteMCPToolParams,
    MCPStdioConfig,
    _resolve_env,
    collect_mcp_tools,
    collect_tools_stdio,
    execute_mcp_tool,
)
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker_with_events,
)
from mistralai.workflows.testing.fixtures import (
    clear_dependency_cache,  # noqa: F401
    event_loop,  # noqa: F401
    mock_upsert_search_attributes,  # noqa: F401
    setup_test_config,  # noqa: F401
    temporal_env,  # noqa: F401
)

SECRET_VALUE = "ntn_super_secret_do_not_leak"
WORKER_VAR = "NOTION_TOKEN_BOT_A"
SUBPROCESS_VAR = "NOTION_TOKEN"


class TestResolveEnv:
    def test_none_mapping_returns_none(self) -> None:
        assert _resolve_env(None) is None

    def test_merges_with_default_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(WORKER_VAR, SECRET_VALUE)
        resolved = _resolve_env({SUBPROCESS_VAR: WORKER_VAR})
        assert resolved is not None
        assert resolved[SUBPROCESS_VAR] == SECRET_VALUE
        # default environment is preserved so the executable still resolves
        assert "PATH" in resolved

    def test_missing_worker_var_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(WORKER_VAR, raising=False)
        with pytest.raises(RuntimeError, match=WORKER_VAR):
            _resolve_env({SUBPROCESS_VAR: WORKER_VAR})

    def test_maps_worker_name_to_subprocess_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("SOURCE_VAR", "value-123")
        resolved = _resolve_env({"TARGET_VAR": "SOURCE_VAR"})
        assert resolved is not None
        assert resolved["TARGET_VAR"] == "value-123"
        # only the subprocess-facing name is injected, not the worker-side name
        assert "SOURCE_VAR" not in resolved


@workflow.define(name="mcp_env_mapping_workflow")
class MCPEnvMappingWorkflow:
    @workflow.entrypoint
    async def run(self) -> int:
        config = MCPStdioConfig(
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            name="notion_bot_a",
            env_mapping={SUBPROCESS_VAR: WORKER_VAR},
        )
        result = await collect_mcp_tools(CollectMCPToolsParams(configs=[config]))
        return len(result.tools)


@pytest.mark.asyncio
async def test_env_mapping_resolves_but_never_leaks_to_temporal(
    temporal_env: WorkflowEnvironment,  # noqa: F811
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The secret reaches the subprocess env but never the Temporal event payload."""
    monkeypatch.setenv(WORKER_VAR, SECRET_VALUE)

    captured_stdio_env: dict[str, Any] = {}

    def make_stdio_client(stdio_params: Any, name: str) -> MagicMock:
        captured_stdio_env["env"] = stdio_params.env
        instance = MagicMock()
        instance.initialize = AsyncMock()
        instance.get_tools = AsyncMock(return_value=[{"function": {"name": "search"}}])
        instance.aclose = AsyncMock()
        return instance

    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientSTDIO",
        side_effect=make_stdio_client,
    ):
        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[MCPEnvMappingWorkflow],
                activities=[collect_mcp_tools],
            ):
                handle = await temporal_env.client.start_workflow(
                    "mcp_env_mapping_workflow",
                    id="test-mcp-env-mapping",
                    task_queue="test-task-queue",
                )
                tool_count = await handle.result()

    # the entrypoint returned len(result.tools) == 1; the SDK wraps scalar returns under "result"
    assert tool_count in (1, {"result": 1})

    # Resolution happened inside the activity: the real secret reached the subprocess env.
    assert captured_stdio_env["env"][SUBPROCESS_VAR] == SECRET_VALUE

    started = [
        e
        for e in captured_events
        if e.event_type.value == "ACTIVITY_TASK_STARTED" and e.attributes.activity_name == "collect_mcp_tools"
    ]
    assert started, "collect_mcp_tools ActivityTaskStarted event was not captured"

    serialized_input = str(started[0].attributes.input.value)
    # Mapping names are safe and expected to appear in the serialized activity params.
    assert SUBPROCESS_VAR in serialized_input
    assert WORKER_VAR in serialized_input
    # The critical assertion: the secret value must never touch Temporal params / history.
    assert SECRET_VALUE not in serialized_input


def _mock_stdio_client(captured_env: dict[str, Any]) -> Any:
    def make(stdio_params: Any, name: str) -> MagicMock:
        captured_env["env"] = stdio_params.env
        instance = MagicMock()
        instance.initialize = AsyncMock()
        instance.get_tools = AsyncMock(return_value=[{"function": {"name": "search"}}])
        instance.execute_tool = AsyncMock(return_value="ok")
        instance.aclose = AsyncMock()
        return instance

    return make


@pytest.mark.asyncio
async def test_resolved_secret_reaches_subprocess_but_is_never_logged(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """collect_tools_stdio injects the secret into the subprocess env without logging it."""
    monkeypatch.setenv(WORKER_VAR, SECRET_VALUE)
    captured_env: dict[str, Any] = {}
    config = MCPStdioConfig(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        name="notion",
        env_mapping={SUBPROCESS_VAR: WORKER_VAR},
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientSTDIO",
        side_effect=_mock_stdio_client(captured_env),
    ):
        with caplog.at_level(logging.DEBUG):
            await collect_tools_stdio(config)

    assert captured_env["env"][SUBPROCESS_VAR] == SECRET_VALUE
    # The secret must not appear in structured logs (stdlib records) or console output.
    assert SECRET_VALUE not in caplog.text
    assert SECRET_VALUE not in capsys.readouterr().err


@pytest.mark.asyncio
async def test_execute_mcp_tool_resolves_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """execute_mcp_tool forwards the resolved secret to the stdio subprocess env too."""
    monkeypatch.setenv(WORKER_VAR, SECRET_VALUE)
    captured_env: dict[str, Any] = {}
    config = MCPStdioConfig(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        name="notion",
        env_mapping={SUBPROCESS_VAR: WORKER_VAR},
    )
    params = ExecuteMCPToolParams(
        configs=[config],
        tool_name="notion_search",
        tool_arguments={},
        config_index=0,
    )
    with patch(
        "mistralai.workflows.plugins.mistralai.mcp.MCPClientSTDIO",
        side_effect=_mock_stdio_client(captured_env),
    ):
        result = await execute_mcp_tool(params)

    assert result.result == "ok"
    assert captured_env["env"][SUBPROCESS_VAR] == SECRET_VALUE
