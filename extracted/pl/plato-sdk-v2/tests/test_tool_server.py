"""Tests for plato.tools.server.ToolServer."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel, Field

from plato.tools import ToolDefinition, get_request_context
from plato.tools.mcp import scoped_mcp_url, write_mcp_config
from plato.tools.request_context import (
    ToolRequestContext,
    register_client_context,
    unregister_client_context,
)
from plato.tools.server import ToolServer

# ---------------------------------------------------------------------------
# ToolServer lifecycle
# ---------------------------------------------------------------------------


class EchoInput(BaseModel):
    msg: str = Field(description="Message to echo")


class AddInput(BaseModel):
    a: int
    b: int


class TestToolServer:
    def test_build_tools_default_empty(self):
        """Default build_tools returns empty list."""
        with patch("plato.tools.server.FastMCP") as mock:
            mock.return_value = MagicMock()
            server = ToolServer(name="Test")
            assert server.port == 8765
            assert server.mcp_path() == "/mcp"

    def test_subclass_build_tools(self):
        """Subclass can define tools via build_tools()."""

        class MyServer(ToolServer):
            def build_tools(self):
                return [
                    ToolDefinition(
                        name="echo",
                        description="Echo",
                        input_model=EchoInput,
                        handler=lambda args: {"echo": args.msg},
                    ),
                ]

        with patch("plato.tools.server.FastMCP") as mock_cls:
            mock_mcp = MagicMock()
            mock_cls.return_value = mock_mcp
            server = MyServer(name="Echo Server", port=9999)
            assert server.port == 9999
            mock_mcp.tool.assert_called_once_with(name="echo", description="Echo")

    def test_custom_host_port(self):
        with patch("plato.tools.server.FastMCP") as mock:
            mock.return_value = MagicMock()
            server = ToolServer(name="Test", host="127.0.0.1", port=3000)
            assert server.port == 3000

    def test_rejects_tools_without_input_model(self):
        """Tools with only input_schema (no input_model) are rejected."""

        class BadServer(ToolServer):
            def build_tools(self):
                return [
                    ToolDefinition(
                        name="old_tool",
                        description="Legacy",
                        input_schema={"type": "object", "properties": {}},
                        handler=lambda args: {},
                    ),
                ]

        with patch("plato.tools.server.FastMCP") as mock:
            mock.return_value = MagicMock()
            with pytest.raises(ValueError, match="must define input_model"):
                BadServer(name="Bad")

    @pytest.mark.asyncio
    async def test_start_and_close(self):
        with patch("plato.tools.server.FastMCP") as mock_cls:
            mock_mcp = MagicMock()
            mock_mcp.run_async = AsyncMock()
            mock_cls.return_value = mock_mcp

            server = ToolServer(name="Test")
            await server.start()
            assert server._task is not None

            await server.close()
            assert server._task is None

    @pytest.mark.asyncio
    async def test_start_idempotent(self):
        with patch("plato.tools.server.FastMCP") as mock_cls:
            mock_mcp = MagicMock()
            mock_mcp.run_async = AsyncMock()
            mock_cls.return_value = mock_mcp

            server = ToolServer(name="Test")
            await server.start()
            task1 = server._task
            await server.start()  # Should not create a second task
            assert server._task is task1
            await server.close()

    @pytest.mark.asyncio
    async def test_close_idempotent(self):
        with patch("plato.tools.server.FastMCP") as mock:
            mock.return_value = MagicMock()
            server = ToolServer(name="Test")
            await server.close()
            await server.close()

    @pytest.mark.asyncio
    async def test_model_tool_registration(self):
        """Tool registered with input_model gets proper schema from FastMCP."""

        class MyServer(ToolServer):
            def build_tools(self):
                return [
                    ToolDefinition(
                        name="add",
                        description="Add two numbers",
                        input_model=AddInput,
                        handler=self._add,
                    ),
                ]

            async def _add(self, args: AddInput) -> dict:
                return {"sum": args.a + args.b}

        with patch("plato.tools.server.FastMCP") as mock_cls:
            mock_mcp = MagicMock()
            mock_cls.return_value = mock_mcp
            MyServer(name="Math")

            # Verify tool was registered
            mock_mcp.tool.assert_called_once_with(name="add", description="Add two numbers")

            # Get the wrapper function that was registered
            wrapper = mock_mcp.tool.return_value.call_args[0][0]

            # Call it with a model instance — should invoke the handler
            result = await wrapper(
                AddInput(a=3, b=4),
                SimpleNamespace(request_context=None),
            )
            assert result == {"sum": 7}

    @pytest.mark.asyncio
    async def test_query_param_context_available_in_handler(self):
        """Handlers can resolve the current caller identity from request metadata."""

        class WhoAmIServer(ToolServer):
            def build_tools(self):
                return [
                    ToolDefinition(
                        name="whoami",
                        description="Expose request context",
                        input_model=EchoInput,
                        handler=self._whoami,
                    ),
                ]

            def _whoami(self, args: EchoInput) -> dict:
                request_context = get_request_context()
                assert request_context is not None
                return {
                    "msg": args.msg,
                    "client_id": request_context.client_id,
                    "instruction": request_context.instruction,
                    "display_name": request_context.display_name,
                    "attempt": request_context.attempt,
                }

        with patch("plato.tools.server.FastMCP") as mock_cls:
            mock_mcp = MagicMock()
            mock_cls.return_value = mock_mcp
            WhoAmIServer(name="WhoAmI")
            register_client_context(
                ToolRequestContext(
                    client_id="agent-123",
                    instruction="build the dashboard",
                    display_name="builder-route-a",
                    attempt=2,
                )
            )

            wrapper = mock_mcp.tool.return_value.call_args[0][0]
            fake_request = SimpleNamespace(
                query_params={
                    "plato_client_id": "agent-123",
                },
                headers={},
            )
            fake_ctx = SimpleNamespace(
                request_context=SimpleNamespace(request=fake_request),
            )

            try:
                result = await wrapper(EchoInput(msg="hello"), fake_ctx)
            finally:
                unregister_client_context("agent-123")

            assert result == {
                "msg": "hello",
                "client_id": "agent-123",
                "instruction": "build the dashboard",
                "display_name": "builder-route-a",
                "attempt": 2,
            }
            assert get_request_context() is None


# ---------------------------------------------------------------------------
# Stdio MCP server helpers (used by save_tools / write_mcp_config path)
# ---------------------------------------------------------------------------


class TestStdioServerHelpers:
    """Test that the inline stdio server script handles both input_schema and input_model."""

    def test_get_schema_from_input_model(self):
        """_get_schema generates JSON schema from input_model when input_schema is None."""
        td = ToolDefinition(
            name="add",
            description="Add",
            input_model=AddInput,
            handler=lambda args: {},
        )
        # Simulate what the stdio script does
        schema = td.input_model.model_json_schema() if td.input_model else td.input_schema
        assert schema["type"] == "object"
        assert "a" in schema["properties"]
        assert "b" in schema["properties"]

    def test_call_handler_with_model(self):
        """Handler receives a model instance when input_model is set."""
        results = []

        def handler(args: AddInput):
            results.append(args)
            return {"sum": args.a + args.b}

        td = ToolDefinition(
            name="add",
            description="Add",
            input_model=AddInput,
            handler=handler,
        )

        # Simulate stdio server: construct model from dict then call handler
        model_instance = td.input_model(**{"a": 5, "b": 3})
        result = td.handler(model_instance)
        assert result == {"sum": 8}
        assert isinstance(results[0], AddInput)
        assert results[0].a == 5

    def test_model_json_schema_has_descriptions(self):
        """Pydantic models generate rich schemas with field descriptions."""
        schema = EchoInput.model_json_schema()
        assert schema["properties"]["msg"]["description"] == "Message to echo"


# ---------------------------------------------------------------------------
# write_mcp_config
# ---------------------------------------------------------------------------


class TestWriteMcpConfig:
    def test_scoped_mcp_url_adds_agent_identity(self):
        result = scoped_mcp_url(
            "http://runtime:8765/mcp",
            client_id="agent-123",
        )

        assert "plato_client_id=agent-123" in result
        assert result == "http://runtime:8765/mcp?plato_client_id=agent-123"

    def test_no_servers_returns_none(self, tmp_path):
        result = write_mcp_config(tmp_path)
        assert result is None
        assert not (tmp_path / ".mcp.json").exists()

    def test_remote_http_server_only(self, tmp_path):
        result = write_mcp_config(tmp_path, remote_url="http://localhost:8765/mcp", remote_name="datagen")
        assert result == tmp_path / ".mcp.json"

        config = json.loads(result.read_text())
        assert "datagen" in config["mcpServers"]
        assert config["mcpServers"]["datagen"]["type"] == "http"
        assert config["mcpServers"]["datagen"]["url"] == "http://localhost:8765/mcp"
        assert len(config["mcpServers"]) == 1

    def test_remote_config_does_not_create_local_tool_artifacts(self, tmp_path):
        result = write_mcp_config(
            tmp_path,
            remote_url="http://runtime:8765/mcp",
            remote_name="world-tools",
        )
        config = json.loads(result.read_text())

        assert len(config["mcpServers"]) == 1
        assert "world-tools" in config["mcpServers"]
        assert config["mcpServers"]["world-tools"]["type"] == "http"
        assert not (tmp_path / ".plato" / "tools.pkl").exists()
        assert not (tmp_path / ".plato" / "mcp_server.py").exists()
