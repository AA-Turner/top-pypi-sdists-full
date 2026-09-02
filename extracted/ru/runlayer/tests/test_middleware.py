"""Test middleware functionality."""

import sys

import anyio
import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import mcp.types as mt
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from runlayer_cli.middleware import RunlayerMiddleware
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_mcp import LocalCapabilities, PostRequest, PreRequest


def create_test_server(
    sync_required: bool = False,
    transport_type: str = "stdio",
    version: int | None = 7,
) -> ServerDetails:
    """Helper to create test server details."""
    return ServerDetails(
        id="server-123",
        name="Test Server",
        url="http://test.example.com",
        transport_type=transport_type,
        transport_config={},
        deployment_mode="local",
        version=version,
        sync_required=sync_required,
    )


def test_server_details_allows_missing_transport_config():
    """Ensure transport_config can be missing for certain transports."""
    server = ServerDetails(
        id="server-456",
        name="SSE Server",
        url="http://sse.example.com",
        transport_type="sse",
        transport_config=None,
    )
    assert server.transport_config is None


@pytest.mark.asyncio
async def test_middleware_initialization():
    """Test that middleware initializes correctly."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server()

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    assert middleware.runlayer_api_client == mock_client
    assert middleware.proxy == mock_proxy
    assert middleware.server == server
    assert middleware.sync_done is True


@pytest.mark.asyncio
@pytest.mark.parametrize("transport_type", ["stdio", "sse", "streaming-http"])
async def test_middleware_sync_required(transport_type: str):
    """sync_done=False for every transport when sync_required=True."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server(sync_required=True, transport_type=transport_type)

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    assert middleware.sync_done is False


@pytest.mark.asyncio
async def test_on_call_tool_calls_pre_and_post():
    """Test that on_call_tool calls pre and post with correct data."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server()

    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-123"}
    )
    mock_client.post.return_value = MagicMock(status_code=200)

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"arg": "value"}
    )

    mock_result = MagicMock(spec=ToolResult)
    mock_result.to_mcp_result.return_value = [
        mt.TextContent(type="text", text="result")
    ]

    async def mock_call_next(context):
        return mock_result

    result = await middleware.on_call_tool(mock_context, mock_call_next)

    mock_client.pre.assert_called_once()
    pre_call_args = mock_client.pre.call_args
    assert pre_call_args[0][0] == "server-123"
    assert isinstance(pre_call_args[0][1], PreRequest)
    assert pre_call_args[0][1].method == "tools/call"

    mock_client.post.assert_called_once()
    post_call_args = mock_client.post.call_args
    assert post_call_args[0][0] == "server-123"
    assert isinstance(post_call_args[0][1], PostRequest)
    assert post_call_args[0][1].correlation_id == "corr-123"
    assert post_call_args[0][1].method == "tools/call"

    assert result == mock_result


@pytest.mark.asyncio
async def test_on_call_tool_applies_modified_args_to_upstream():
    """Input masking: modified_args from pre are sent to the upstream call."""
    mock_client = MagicMock()
    server = create_test_server()

    masked_args = {"token": "[MASKED]"}
    mock_client.pre.return_value = MagicMock(
        status_code=200,
        json=lambda: {"correlation_id": "corr-in", "modified_args": masked_args},
    )
    mock_client.post.return_value = MagicMock(status_code=200, json=lambda: {})

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"token": "sk-secret-1234"}
    )

    seen = {}
    mock_result = MagicMock(spec=ToolResult)
    mock_result.to_mcp_result.return_value = [mt.TextContent(type="text", text="ok")]

    async def mock_call_next(context):
        seen["arguments"] = dict(context.message.arguments)
        return mock_result

    await middleware.on_call_tool(mock_context, mock_call_next)

    # Upstream received the masked arguments, not the raw secret.
    assert seen["arguments"] == masked_args
    # Post audit payload also carries the masked arguments.
    post_payload = mock_client.post.call_args[0][1]
    assert post_payload.params["arguments"] == masked_args


@pytest.mark.asyncio
async def test_on_call_tool_applies_modified_output():
    """Output masking: modified_output from post replaces the client result."""
    mock_client = MagicMock()
    server = create_test_server()

    masked = mt.CallToolResult(
        content=[mt.TextContent(type="text", text="server ip [IP_ADDRESS]")],
        isError=False,
    )
    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-out"}
    )
    mock_client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"modified_output": masked.model_dump(mode="json")},
    )

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"_runlayer_session_id": "sess-123"}
    )

    result = ToolResult(
        content=[mt.TextContent(type="text", text="server ip 192.168.1.1")]
    )

    async def mock_call_next(context):
        return result

    out = await middleware.on_call_tool(mock_context, mock_call_next)

    text = out.content[0].text  # type: ignore[union-attr]
    assert "192.168.1.1" not in text
    assert "[IP_ADDRESS]" in text


@pytest.mark.asyncio
async def test_on_call_tool_applies_modified_output_to_structured_content():
    """Output masking also rewrites structured_content (e.g. BigQuery rows),
    not just text blocks."""
    mock_client = MagicMock()
    server = create_test_server()

    masked = mt.CallToolResult(
        content=[mt.TextContent(type="text", text="see structured")],
        structuredContent={"rows": [{"ssn": "[SSN]"}]},
        isError=False,
    )
    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-struct"}
    )
    mock_client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"modified_output": masked.model_dump(mode="json")},
    )

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"_runlayer_session_id": "sess-123"}
    )

    result = ToolResult(
        content=[mt.TextContent(type="text", text="see structured")],
        structured_content={"rows": [{"ssn": "123-45-6789"}]},
    )

    async def mock_call_next(context):
        return result

    out = await middleware.on_call_tool(mock_context, mock_call_next)

    assert out.structured_content == {"rows": [{"ssn": "[SSN]"}]}
    assert "123-45-6789" not in str(out.structured_content)


@pytest.mark.asyncio
async def test_on_call_tool_no_modified_output_returns_original():
    """No modified_output: the original upstream result is returned untouched."""
    mock_client = MagicMock()
    server = create_test_server()

    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-noop"}
    )
    mock_client.post.return_value = MagicMock(status_code=200, json=lambda: {})

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"_runlayer_session_id": "sess-123"}
    )

    result = ToolResult(content=[mt.TextContent(type="text", text="clean output")])

    async def mock_call_next(context):
        return result

    out = await middleware.on_call_tool(mock_context, mock_call_next)

    assert out is result
    assert out.content[0].text == "clean output"  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_on_list_tools_calls_pre_and_post():
    """Test that on_list_tools calls pre and post with correct data."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server()

    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-456"}
    )
    mock_client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {
                "name": "test_tool",
                "description": "A test tool",
                "inputSchema": {"type": "object"},
            }
        ],
    )

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.ListToolsRequest(method="tools/list")

    mock_tool = MagicMock()
    mock_tool.to_mcp_tool.return_value = {
        "name": "test_tool",
        "description": "A test tool",
        "inputSchema": {"type": "object", "properties": {}},
    }

    async def mock_call_next(context):
        return [mock_tool]

    result = await middleware.on_list_tools(mock_context, mock_call_next)  # type: ignore

    mock_client.pre.assert_called_once()
    pre_call_args = mock_client.pre.call_args
    assert pre_call_args[0][0] == "server-123"
    assert isinstance(pre_call_args[0][1], PreRequest)
    assert pre_call_args[0][1].method == "tools/list"
    assert pre_call_args[0][1].params is None

    mock_client.post.assert_called_once()
    post_call_args = mock_client.post.call_args
    assert post_call_args[0][0] == "server-123"
    assert isinstance(post_call_args[0][1], PostRequest)
    assert post_call_args[0][1].correlation_id == "corr-456"
    assert post_call_args[0][1].method == "tools/list"

    mock_tool.to_mcp_tool.assert_called_once()

    assert isinstance(result, list)


def _make_list_tools_middleware(
    *, sync_required: bool, transport_type: str = "streaming-http"
) -> tuple[RunlayerMiddleware, MagicMock, MagicMock]:
    """Helper: create middleware wired for on_list_tools with async proxy mocks."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()

    # Proxy async methods for _sync_capabilities
    mock_tool_obj = MagicMock()
    mock_tool_obj.to_mcp_tool.return_value = mt.Tool(
        name="test_tool",
        description="A test tool",
        inputSchema={"type": "object"},
    )
    mock_proxy.get_tools = AsyncMock(return_value={"test_tool": mock_tool_obj})
    mock_proxy.get_resources = AsyncMock(return_value={})
    mock_proxy.get_prompts = AsyncMock(return_value={})

    # Pre/post responses
    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-sync"}
    )
    mock_client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {
                "name": "test_tool",
                "description": "A test tool",
                "inputSchema": {"type": "object"},
            }
        ],
    )

    server = create_test_server(
        sync_required=sync_required, transport_type=transport_type
    )
    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )
    return middleware, mock_client, mock_proxy


async def _call_on_list_tools(middleware: RunlayerMiddleware, call_next=None) -> list:
    """Helper: invoke on_list_tools with a mock tool result."""
    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.ListToolsRequest(method="tools/list")

    mock_tool = MagicMock()
    mock_tool.to_mcp_tool.return_value = {
        "name": "test_tool",
        "description": "A test tool",
        "inputSchema": {"type": "object", "properties": {}},
    }

    async def mock_call_next(context):
        return [mock_tool]

    return await middleware.on_list_tools(  # type: ignore
        mock_context, call_next or mock_call_next
    )


@pytest.mark.asyncio
async def test_on_list_tools_syncs_capabilities_when_sync_required():
    """Sync fires on first tools/list when sync_required=True."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)

    await _call_on_list_tools(middleware)

    mock_client.update_capabilities.assert_called_once()
    args = mock_client.update_capabilities.call_args[0]
    assert args[0] == "server-123"
    assert mock_client.update_capabilities.call_args.kwargs == {"server_version": 7}
    caps = args[1]
    assert isinstance(caps, LocalCapabilities)
    assert "test_tool" in caps.tools
    assert middleware.sync_done is True


@pytest.mark.asyncio
async def test_on_list_tools_skips_sync_when_already_done():
    """No sync when sync_required=False (sync_done starts True)."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)

    await _call_on_list_tools(middleware)

    mock_client.update_capabilities.assert_not_called()


@pytest.mark.asyncio
async def test_on_list_tools_sync_failure_does_not_break_tools_list():
    """Sync error is swallowed; tools/list still returns normally."""
    middleware, mock_client, mock_proxy = _make_list_tools_middleware(
        sync_required=True
    )
    mock_proxy.get_tools = AsyncMock(side_effect=RuntimeError("connection failed"))

    result = await _call_on_list_tools(middleware)

    assert isinstance(result, list)
    assert len(result) > 0
    mock_client.update_capabilities.assert_not_called()
    assert middleware.sync_done is False


@pytest.mark.asyncio
async def test_on_list_tools_cosmetic_edit_refreshes_version_and_retries_immediately():
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)
    mock_client.update_capabilities.side_effect = [
        httpx.HTTPStatusError(
            "409 Conflict",
            request=httpx.Request("POST", "https://example.com/capabilities"),
            response=httpx.Response(409),
        ),
        None,
    ]
    mock_client.get_server_details.return_value = create_test_server(
        sync_required=True,
        transport_type=middleware.server.transport_type,
        version=8,
    )

    await _call_on_list_tools(middleware)

    assert mock_client.update_capabilities.call_count == 2
    assert mock_client.update_capabilities.call_args.kwargs == {"server_version": 8}
    assert middleware.server.version == 8
    assert middleware.sync_done is True


@pytest.mark.asyncio
async def test_on_list_tools_empty_transport_config_reshaping_retries():
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)
    middleware.server.transport_config = {"env": {}, "headers": {}}
    mock_client.update_capabilities.side_effect = httpx.HTTPStatusError(
        "409 Conflict",
        request=httpx.Request("POST", "https://example.com/capabilities"),
        response=httpx.Response(409),
    )
    mock_client.get_server_details.return_value = create_test_server(
        sync_required=True,
        transport_type=middleware.server.transport_type,
        version=8,
    )

    await _call_on_list_tools(middleware)

    assert middleware.sync_done is False
    assert middleware.server.version == 8


@pytest.mark.asyncio
async def test_on_list_tools_source_change_stops_stale_sync_retries():
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)
    mock_client.update_capabilities.side_effect = httpx.HTTPStatusError(
        "409 Conflict",
        request=httpx.Request("POST", "https://example.com/capabilities"),
        response=httpx.Response(409),
    )
    changed_server = create_test_server(sync_required=True, version=8)
    changed_server.url = "http://changed.example.com"
    mock_client.get_server_details.return_value = changed_server

    result = await _call_on_list_tools(middleware)

    assert isinstance(result, list)
    assert len(result) > 0
    assert middleware.sync_done is True

    await _call_on_list_tools(middleware)
    assert mock_client.update_capabilities.call_count == 1


@pytest.mark.asyncio
async def test_on_list_tools_syncs_only_once():
    """Sync fires only on the first tools/list, not subsequent ones."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)

    await _call_on_list_tools(middleware)
    await _call_on_list_tools(middleware)

    mock_client.update_capabilities.assert_called_once()


@pytest.mark.asyncio
async def test_on_list_tools_background_sync_does_not_block_response():
    """With background_tasks set, tools/list returns before sync completes.

    Regression: servers that never answer resources/prompts (Xcode mcpbridge)
    hang introspection ~30s per call; inline sync delayed the tools/list
    response until clients killed the connection.
    """
    middleware, mock_client, mock_proxy = _make_list_tools_middleware(
        sync_required=True
    )
    release = anyio.Event()

    async def slow_get_resources():
        await release.wait()
        return {}

    mock_proxy.get_resources = slow_get_resources

    async with anyio.create_task_group() as tg:
        middleware.background_tasks = tg

        result = await _call_on_list_tools(middleware)

        # tools/list answered while sync is still in flight
        assert len(result) > 0
        assert middleware.sync_done is False
        mock_client.update_capabilities.assert_not_called()

        # a second list while sync is in flight must not spawn another sync
        await _call_on_list_tools(middleware)

        release.set()

    assert middleware.sync_done is True
    mock_client.update_capabilities.assert_called_once()


@pytest.mark.asyncio
async def test_background_sync_timeout_resets_in_flight_for_retry():
    """A wedged background sync must time out and allow a later retry."""
    middleware, mock_client, mock_proxy = _make_list_tools_middleware(
        sync_required=True
    )

    async def never_answers():
        await anyio.sleep(60)

    mock_proxy.get_resources = never_answers

    with patch("runlayer_cli.middleware._BACKGROUND_SYNC_TIMEOUT_SECONDS", 0.05):
        async with anyio.create_task_group() as tg:
            middleware.background_tasks = tg
            await _call_on_list_tools(middleware)
        # task group exit waits for the sync task, which times out

    assert middleware.sync_done is False
    assert middleware._sync_in_flight is False
    mock_client.update_capabilities.assert_not_called()


# --- Flow tracing integration (runlayer_cli.flow_trace) ---


@pytest.fixture
def flow_sink():
    """Enable flow tracing into a list for the duration of a test."""
    from runlayer_cli import flow_trace

    summaries: list[dict] = []
    flow_trace.enable_flow_tracing(summaries.append)
    yield summaries
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def _call_tool_middleware(pre_json: dict | None = None):
    mock_client = MagicMock()
    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: pre_json or {"correlation_id": "corr-ft"}
    )
    mock_client.post.return_value = MagicMock(status_code=200)
    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=create_test_server()
    )
    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(name="test_tool", arguments={})
    return middleware, mock_context


@pytest.mark.asyncio
async def test_on_call_tool_emits_flow_with_steps(flow_sink):
    middleware, mock_context = _call_tool_middleware()

    mock_result = MagicMock(spec=ToolResult)
    mock_result.to_mcp_result.return_value = []

    async def mock_call_next(context):
        return mock_result

    await middleware.on_call_tool(mock_context, mock_call_next)

    assert len(flow_sink) == 1
    summary = flow_sink[0]
    assert summary["operation"] == "cli.call_tool"
    assert summary["status"] == "ok"
    assert [s["name"] for s in summary["steps"]] == ["pre", "upstream", "post"]
    assert {s["kind"] for s in summary["steps"]} == {"http", "remote"}


@pytest.mark.asyncio
async def test_on_call_tool_upstream_unreachable_marks_error(flow_sink):
    import httpx

    middleware, mock_context = _call_tool_middleware()

    async def mock_call_next(context):
        raise httpx.ConnectError("refused")

    result = await middleware.on_call_tool(mock_context, mock_call_next)

    assert isinstance(result, ToolResult)
    summary = flow_sink[0]
    assert summary["status"] == "error"
    assert summary["error_type"] == "ConnectError"
    # In-band errors are classified at the catch site (no classifier install
    # needed): category only, never the exception message.
    assert summary["error_category"] == "connect"
    assert "error_http_status" not in summary
    assert "refused" not in str(summary)
    # The error-path post audit is still timed.
    assert [s["name"] for s in summary["steps"]] == ["pre", "upstream", "post"]


@pytest.mark.asyncio
async def test_on_list_tools_raised_error_is_classified(flow_sink):
    """A propagating exception gets a category via the installed classifier
    (wired by the ``runlayer run`` entrypoint alongside the sink)."""
    from runlayer_cli import flow_trace
    from runlayer_cli.error_classification import classify_exception

    flow_trace.set_error_classifier(classify_exception)
    try:
        middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)
        request = httpx.Request("GET", "http://test.example.com/mcp")
        response = httpx.Response(403, request=request, text="Forbidden secret body")

        async def mock_call_next(context):
            raise httpx.HTTPStatusError("denied", request=request, response=response)

        with pytest.raises(httpx.HTTPStatusError):
            await _call_on_list_tools(middleware, call_next=mock_call_next)
    finally:
        flow_trace.set_error_classifier(None)

    summary = flow_sink[0]
    assert summary["status"] == "error"
    assert summary["error_type"] == "HTTPStatusError"
    assert summary["error_category"] == "http_403"
    assert summary["error_http_status"] == 403
    assert "Forbidden" not in str(summary)


@pytest.mark.asyncio
async def test_on_call_tool_quick_result_still_emits_flow(flow_sink):
    middleware, mock_context = _call_tool_middleware(
        pre_json={"correlation_id": "c", "quick_tool_result": "blocked"}
    )

    async def mock_call_next(context):  # pragma: no cover - must not be reached
        raise AssertionError("upstream must not be called on quick_tool_result")

    await middleware.on_call_tool(mock_context, mock_call_next)

    summary = flow_sink[0]
    assert summary["operation"] == "cli.call_tool"
    assert [s["name"] for s in summary["steps"]] == ["pre"]


@pytest.mark.asyncio
async def test_on_list_tools_emits_flow_with_nested_sync_steps(flow_sink):
    """Lazy capability sync nests its steps under the cli.list_tools flow."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)

    await _call_on_list_tools(middleware)

    assert len(flow_sink) == 1
    summary = flow_sink[0]
    assert summary["operation"] == "cli.list_tools"
    names = [s["name"] for s in summary["steps"]]
    assert names == ["pre", "upstream", "introspect", "upload", "post"]


@pytest.mark.asyncio
async def test_background_sync_emits_its_own_flow(flow_sink):
    """Background sync must emit a cli.sync_capabilities flow of its own, not
    append steps to the (already emitted) cli.list_tools flow it was spawned
    from — start_soon inherits contextvars and operation() is re-entrant.
    """
    middleware, _, _ = _make_list_tools_middleware(sync_required=True)

    async with anyio.create_task_group() as tg:
        middleware.background_tasks = tg
        await _call_on_list_tools(middleware)

    ops = [s["operation"] for s in flow_sink]
    assert ops.count("cli.list_tools") == 1
    assert ops.count("cli.sync_capabilities") == 1
    list_flow = next(s for s in flow_sink if s["operation"] == "cli.list_tools")
    assert [s["name"] for s in list_flow["steps"]] == ["pre", "upstream", "post"]
    sync_flow = next(s for s in flow_sink if s["operation"] == "cli.sync_capabilities")
    assert [s["name"] for s in sync_flow["steps"]] == ["introspect", "upload"]


@pytest.mark.asyncio
async def test_lag_one_delivery_second_call_carries_first_flow(flow_sink):
    """End-to-end lag-one: flow N rides request N+1's body."""
    from unittest.mock import patch

    from runlayer_cli.api import RunlayerClient
    from runlayer_cli.flow_delivery import FlowDeliveryQueue
    from runlayer_cli import flow_trace

    queue = FlowDeliveryQueue()
    flow_trace.enable_flow_tracing(queue.enqueue)

    api_client = RunlayerClient(
        hostname="https://example.com", secret="k", flow_queue=queue
    )
    middleware = RunlayerMiddleware(
        runlayer_api_client=api_client, proxy=MagicMock(), server=create_test_server()
    )
    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.CallToolRequestParams(
        name="test_tool", arguments={"_runlayer_session_id": "sess-123"}
    )

    mock_result = MagicMock(spec=ToolResult)
    mock_result.to_mcp_result.return_value = []

    async def mock_call_next(context):
        return mock_result

    mock_post = MagicMock(
        return_value=MagicMock(
            status_code=200, json=lambda: {"correlation_id": "corr-1"}
        )
    )
    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(post=mock_post)
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        await middleware.on_call_tool(mock_context, mock_call_next)
        first_bodies = [c.kwargs["json"] for c in mock_post.call_args_list]
        assert all("client_flows" not in b for b in first_bodies)

        await middleware.on_call_tool(mock_context, mock_call_next)
        second_pre_body = mock_post.call_args_list[2].kwargs["json"]
        assert second_pre_body["client_flows"]["flows"][0]["operation"] == (
            "cli.call_tool"
        )
        assert second_pre_body["client_flows"]["flows"][0]["session_id"] == "sess-123"


# --- Unreachable upstream: hangs and wrapped/timeout errors ---
#
# fastmcp/anyio task groups can surface transport failures as (nested)
# ExceptionGroups or read timeouts rather than the bare httpx connect errors,
# e.g. when the upstream URL blackholes (VPN down, internal-only DNS). These
# must take the same graceful branch as a plain ConnectError: friendly result /
# empty list, and a /post that reports the failure.

if sys.version_info < (3, 11):  # pragma: no cover - py3.10 backport
    from exceptiongroup import ExceptionGroup


def _raising_call_next(exc: BaseException):
    async def call_next(context):
        raise exc

    return call_next


def _assert_list_unreachable_post(mock_client) -> None:
    """The unreachable branch posts an empty result with an error description."""
    mock_client.post.assert_called_once()
    post_payload = mock_client.post.call_args[0][1]
    assert isinstance(post_payload, PostRequest)
    assert post_payload.result == []
    assert post_payload.upstream_error is not None
    assert post_payload.upstream_error.type
    assert post_payload.upstream_error.message is not None


async def _list_tools_with(middleware, call_next) -> list:
    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.ListToolsRequest(method="tools/list")
    return await middleware.on_list_tools(mock_context, call_next)  # type: ignore


@pytest.mark.asyncio
async def test_on_list_tools_upstream_exception_group_returns_empty():
    """ExceptionGroup-wrapped connect error takes the graceful branch."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)
    exc = ExceptionGroup("unhandled", [httpx.ConnectError("refused")])

    result = await _list_tools_with(middleware, _raising_call_next(exc))

    assert result == []
    _assert_list_unreachable_post(mock_client)


@pytest.mark.asyncio
async def test_on_list_tools_upstream_nested_exception_group_returns_empty():
    """Nested groups (task group in task group) are unwrapped recursively."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)
    inner = ExceptionGroup("inner", [httpx.ConnectTimeout("timed out")])
    exc = ExceptionGroup("outer", [inner])

    result = await _list_tools_with(middleware, _raising_call_next(exc))

    assert result == []
    _assert_list_unreachable_post(mock_client)


@pytest.mark.asyncio
async def test_on_list_tools_upstream_read_timeout_returns_empty():
    """A hung-then-timed-out upstream read takes the graceful branch."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)

    result = await _list_tools_with(
        middleware, _raising_call_next(httpx.ReadTimeout("timed out"))
    )

    assert result == []
    _assert_list_unreachable_post(mock_client)


@pytest.mark.asyncio
async def test_on_list_tools_upstream_hang_returns_empty(monkeypatch):
    """A pure hang (no exception at all) is bounded by the list timeout."""
    from runlayer_cli import middleware as middleware_module

    monkeypatch.setattr(middleware_module, "_LIST_TOOLS_UPSTREAM_TIMEOUT_SECONDS", 0.05)
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=False)

    async def hanging_call_next(context):
        await anyio.sleep(5)

    result = await _list_tools_with(middleware, hanging_call_next)

    assert result == []
    _assert_list_unreachable_post(mock_client)


@pytest.mark.asyncio
async def test_on_list_tools_unrelated_error_still_raises():
    """Non-connection errors must propagate, bare or group-wrapped."""
    middleware, _, _ = _make_list_tools_middleware(sync_required=False)

    with pytest.raises(ValueError):
        await _list_tools_with(middleware, _raising_call_next(ValueError("boom")))

    middleware2, _, _ = _make_list_tools_middleware(sync_required=False)
    grouped = ExceptionGroup("unhandled", [ValueError("boom")])
    with pytest.raises(ExceptionGroup):
        await _list_tools_with(middleware2, _raising_call_next(grouped))


@pytest.mark.asyncio
async def test_on_call_tool_upstream_exception_group_returns_friendly_result():
    middleware, mock_context = _call_tool_middleware()
    exc = ExceptionGroup("unhandled", [httpx.ConnectError("refused")])

    result = await middleware.on_call_tool(mock_context, _raising_call_next(exc))

    assert isinstance(result, ToolResult)
    assert "is not running" in str(result.content)


@pytest.mark.asyncio
async def test_on_call_tool_upstream_read_timeout_returns_friendly_result():
    middleware, mock_context = _call_tool_middleware()

    result = await middleware.on_call_tool(
        mock_context, _raising_call_next(httpx.ReadTimeout("timed out"))
    )

    assert isinstance(result, ToolResult)
    assert "is not running" in str(result.content)


@pytest.mark.asyncio
async def test_on_call_tool_unrelated_error_still_raises():
    middleware, mock_context = _call_tool_middleware()

    with pytest.raises(ValueError):
        await middleware.on_call_tool(
            mock_context, _raising_call_next(ValueError("boom"))
        )
