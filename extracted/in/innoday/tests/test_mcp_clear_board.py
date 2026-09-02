"""
Tests for the MCP `clear_board` tool and `register_board(sync=...)` param.
Uses httpx mocking -- no real API needed.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp import server


def _mock_async_client(response):
    """Build a mocked httpx.AsyncClient whose get/post return `response`."""
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=response)
    return mock_client


@pytest.mark.asyncio
async def test_clear_board_tool_calls_clear_endpoint():
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"cleared": 7}

    mock_client = _mock_async_client(resp)

    with (
        patch.object(server, "httpx") as mock_httpx,
        patch.object(server._api, "resolve_org", return_value="org-1"),
    ):
        mock_httpx.AsyncClient.return_value = mock_client
        # dry_run passed explicitly: under FastMCP v3 @app.tool() returns the
        # bare function, so calling it directly bypasses the framework's own
        # argument binding -- an omitted Field(default=False) param would
        # resolve to the truthy FieldInfo object itself rather than False.
        result = await server.clear_board(board_id="board-1", dry_run=False)

    assert result.get("cleared") == 7
    called_url = mock_client.post.call_args[0][0]
    assert called_url.endswith("/boards/board-1/clear")


@pytest.mark.asyncio
async def test_clear_board_tool_dry_run_appends_query_param():
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"cleared": 3}

    mock_client = _mock_async_client(resp)

    with (
        patch.object(server, "httpx") as mock_httpx,
        patch.object(server._api, "resolve_org", return_value="org-1"),
    ):
        mock_httpx.AsyncClient.return_value = mock_client
        result = await server.clear_board(board_id="board-1", dry_run=True)

    assert result.get("cleared") == 3
    called_url = mock_client.post.call_args[0][0]
    assert "/boards/board-1/clear?dry_run=true" in called_url


@pytest.mark.asyncio
async def test_clear_board_tool_returns_error_when_no_org():
    with patch.object(server._api, "resolve_org", return_value=None):
        result = await server.clear_board(board_id="board-1", dry_run=False)

    assert "error" in result


@pytest.mark.asyncio
async def test_clear_board_tool_returns_error_on_failure_status():
    resp = MagicMock()
    resp.status_code = 404
    resp.text = "not found"

    mock_client = _mock_async_client(resp)

    with (
        patch.object(server, "httpx") as mock_httpx,
        patch.object(server._api, "resolve_org", return_value="org-1"),
    ):
        mock_httpx.AsyncClient.return_value = mock_client
        result = await server.clear_board(board_id="board-1", dry_run=False)

    assert "error" in result


@pytest.mark.asyncio
async def test_register_board_with_sync_chains_sync_board():
    register_resp = MagicMock()
    register_resp.status_code = 201
    register_resp.json.return_value = {"id": "board-1", "board_name": "My Board"}

    mock_client = _mock_async_client(register_resp)

    sync_result = {"synced": 5}

    # In FastMCP v3 register_board calls the bare sync_board(...) function, so
    # patch that name directly with an AsyncMock (v2 wrapped it and the code
    # called sync_board.fn(...)). Assert inside the `with` block -- the patch
    # is reverted on exit, restoring the real function.
    mock_sync_board = AsyncMock(return_value=sync_result)
    with (
        patch.object(server, "httpx") as mock_httpx,
        patch.object(server._api, "resolve_org", return_value="org-1"),
        patch.object(server, "sync_board", new=mock_sync_board),
    ):
        mock_httpx.AsyncClient.return_value = mock_client

        result = await server.register_board(
            board_url="https://trello.com/b/abc/my-board",
            board_name="My Board",
            board_type="trello",
            integration_token="tok-123",
            user_id="user-abc",
            sync=True,
        )

        mock_sync_board.assert_awaited_once_with(
            board_id="board-1", organization_id="org-1"
        )

    assert result["registered"] is True
    assert result["board"]["sync"] == sync_result


@pytest.mark.asyncio
async def test_register_board_without_sync_does_not_call_sync_board():
    register_resp = MagicMock()
    register_resp.status_code = 201
    register_resp.json.return_value = {"id": "board-1", "board_name": "My Board"}

    mock_client = _mock_async_client(register_resp)

    mock_sync_board = AsyncMock()
    with (
        patch.object(server, "httpx") as mock_httpx,
        patch.object(server._api, "resolve_org", return_value="org-1"),
        patch.object(server, "sync_board", new=mock_sync_board),
    ):
        mock_httpx.AsyncClient.return_value = mock_client

        result = await server.register_board(
            board_url="https://trello.com/b/abc/my-board",
            board_name="My Board",
            board_type="trello",
            integration_token="tok-123",
            user_id="user-abc",
            sync=False,
        )

        mock_sync_board.assert_not_awaited()

    assert result["registered"] is True
    assert "sync" not in result["board"]
