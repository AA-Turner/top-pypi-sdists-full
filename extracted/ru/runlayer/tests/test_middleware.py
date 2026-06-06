"""Test middleware functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock
import mcp.types as mt
from fastmcp.server.middleware.middleware import MiddlewareContext
from fastmcp.tools.tool import ToolResult
from runlayer_cli.middleware import RunlayerMiddleware
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_mcp import LocalCapabilities, PostRequest, PreRequest


def create_test_server(
    sync_required: bool = False, transport_type: str = "stdio"
) -> ServerDetails:
    """Helper to create test server details."""
    return ServerDetails(
        id="server-123",
        name="Test Server",
        url="http://test.example.com",
        transport_type=transport_type,
        transport_config={},
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
async def test_middleware_sync_required():
    """sync_done=False for non-stdio transports when sync_required=True."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server(sync_required=True, transport_type="streaming-http")

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    assert middleware.sync_done is False


@pytest.mark.asyncio
async def test_middleware_stdio_skips_sync():
    """stdio transports skip middleware sync (handled at startup)."""
    mock_client = MagicMock()
    mock_proxy = MagicMock()
    server = create_test_server(sync_required=True, transport_type="stdio")

    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=mock_proxy, server=server
    )

    assert middleware.sync_done is True


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
    mock_context.message = mt.CallToolRequestParams(name="test_tool", arguments={})

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
    mock_context.message = mt.CallToolRequestParams(name="test_tool", arguments={})

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
    mock_context.message = mt.CallToolRequestParams(name="test_tool", arguments={})

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


async def _call_on_list_tools(middleware: RunlayerMiddleware) -> list:
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

    return await middleware.on_list_tools(mock_context, mock_call_next)  # type: ignore


@pytest.mark.asyncio
async def test_on_list_tools_syncs_capabilities_when_sync_required():
    """Sync fires on first tools/list when sync_required=True."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)

    await _call_on_list_tools(middleware)

    mock_client.update_capabilities.assert_called_once()
    args = mock_client.update_capabilities.call_args[0]
    assert args[0] == "server-123"
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
async def test_on_list_tools_syncs_only_once():
    """Sync fires only on the first tools/list, not subsequent ones."""
    middleware, mock_client, _ = _make_list_tools_middleware(sync_required=True)

    await _call_on_list_tools(middleware)
    await _call_on_list_tools(middleware)

    mock_client.update_capabilities.assert_called_once()
