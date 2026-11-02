"""Query class for handling bidirectional control protocol."""

import json
import logging
import os
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable
from contextlib import suppress
from typing import TYPE_CHECKING, Any

import anyio
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    ListToolsRequest,
)

from ..types import (
    CanUseToolControlRequest,
    ControlRequest,
    ControlResponse,
    HookCallbackControlRequest,
    McpSetServersConfig,
    McpToolCallControlRequest,
    PermissionResultAllow,
    PermissionResultDeny,
    PermissionUpdate,
    ToolPermissionContext,
)
from .transport import Transport

if TYPE_CHECKING:
    from mcp.server import Server as McpServer

logger = logging.getLogger(__name__)


def _convert_hook_output_for_cli(hook_output: dict[str, Any]) -> dict[str, Any]:
    """Convert Python-safe field names to CLI-expected field names.

    The Python SDK uses `async_` and `continue_` to avoid keyword conflicts,
    but the CLI expects `async` and `continue`. This function performs the
    necessary conversion.
    """
    converted = {}
    for key, value in hook_output.items():
        if key == "async_":
            converted["async"] = value
        elif key == "continue_":
            converted["continue"] = value
        else:
            converted[key] = value
    return converted


class Query:
    """Handles bidirectional control protocol on top of Transport.

    This class manages:
    - Control request/response routing
    - Hook callbacks
    - Tool permission callbacks
    - Message streaming
    - Initialization handshake
    """

    def __init__(
        self,
        transport: Transport,
        is_streaming_mode: bool,
        can_use_tool: Callable[
            [str, dict[str, Any], ToolPermissionContext],
            Awaitable[PermissionResultAllow | PermissionResultDeny],
        ]
        | None = None,
        hooks: dict[str, list[dict[str, Any]]] | None = None,
        sdk_mcp_servers: dict[str, "McpServer"] | None = None,
        initialize_timeout: float = 60.0,
        agents: dict[str, dict[str, Any]] | None = None,
        system_prompt: str | None = None,
        append_system_prompt: str | None = None,
        setting_sources: list[str] | None = None,
    ):
        self._initialize_timeout = initialize_timeout
        self.transport = transport
        self.is_streaming_mode = is_streaming_mode
        self.can_use_tool = can_use_tool
        self.hooks = hooks or {}
        self.sdk_mcp_servers = sdk_mcp_servers or {}
        self._agents = agents
        self._system_prompt = system_prompt
        self._append_system_prompt = append_system_prompt
        self._setting_sources = setting_sources

        # Control protocol state
        self.pending_control_responses: dict[str, anyio.Event] = {}
        self.pending_control_results: dict[str, dict[str, Any] | Exception] = {}
        self.hook_callbacks: dict[str, Callable[..., Any]] = {}
        self.next_callback_id = 0
        self._request_counter = 0

        # Message stream
        self._message_send, self._message_receive = anyio.create_memory_object_stream[
            dict[str, Any]
        ](max_buffer_size=100)
        self._tg: anyio.abc.TaskGroup | None = None
        self._initialized = False
        self._closed = False
        self._initialization_result: dict[str, Any] | None = None

        # Track first result for proper stream closure with SDK MCP servers
        self._first_result_event = anyio.Event()
        self._stream_close_timeout = (
            float(os.environ.get("CORTEX_CODE_STREAM_CLOSE_TIMEOUT", "60000")) / 1000.0
        )  # Convert ms to seconds

    async def initialize(self) -> dict[str, Any] | None:
        """Initialize control protocol if in streaming mode.

        Returns:
            Initialize response with supported commands, or None if not streaming
        """
        if not self.is_streaming_mode:
            return None

        # Build hooks configuration for initialization
        hooks_config: dict[str, Any] = {}
        if self.hooks:
            for event, matchers in self.hooks.items():
                if matchers:
                    hooks_config[event] = []
                    for matcher in matchers:
                        callback_ids = []
                        for callback in matcher.get("hooks", []):
                            callback_id = f"hook_{self.next_callback_id}"
                            self.next_callback_id += 1
                            self.hook_callbacks[callback_id] = callback
                            callback_ids.append(callback_id)
                        hook_matcher_config: dict[str, Any] = {
                            "matcher": matcher.get("matcher"),
                            "hookCallbackIds": callback_ids,
                        }
                        if matcher.get("timeout") is not None:
                            hook_matcher_config["timeout"] = matcher.get("timeout")
                        hooks_config[event].append(hook_matcher_config)

        # Send initialize request
        request: dict[str, Any] = {
            "subtype": "initialize",
            "hooks": hooks_config if hooks_config else None,
        }
        mcp_servers_for_transport: dict[str, dict[str, Any]] = {}
        sdk_mcp_tool_definitions: dict[str, list[dict[str, Any]]] = {}
        if self.sdk_mcp_servers:
            request["sdkMcpServers"] = list(self.sdk_mcp_servers.keys())
            for name, server in self.sdk_mcp_servers.items():
                mcp_servers_for_transport[name] = {
                    "type": "sdk",
                    "name": server.name,
                }
                tool_defs = getattr(server, "_sdk_tool_definitions", [])
                if tool_defs:
                    from .. import _convert_input_schema
                    sdk_mcp_tool_definitions[name] = [
                        {
                            "name": tool_def.name,
                            "description": tool_def.description,
                            "inputSchema": _convert_input_schema(
                                tool_def.input_schema
                            ),
                        }
                        for tool_def in tool_defs
                    ]
        if self._agents:
            request["agents"] = self._agents
        if self._system_prompt is not None:
            request["systemPrompt"] = self._system_prompt
        if self._append_system_prompt is not None:
            request["appendSystemPrompt"] = self._append_system_prompt
        if self._setting_sources is not None:
            request["settingSources"] = self._setting_sources
        if self.can_use_tool is not None:
            request["sdkManagedPermissions"] = True
        if sdk_mcp_tool_definitions:
            request["sdkMcpToolDefinitions"] = sdk_mcp_tool_definitions
        if mcp_servers_for_transport:
            request["mcpServers"] = mcp_servers_for_transport

        response = await self._send_control_request(
            request, timeout=self._initialize_timeout
        )
        self._initialized = True
        self._initialization_result = response
        return response

    async def start(self) -> None:
        """Start reading messages from transport."""
        if self._tg is None:
            self._tg = anyio.create_task_group()
            await self._tg.__aenter__()
            self._tg.start_soon(self._read_messages)

    async def _read_messages(self) -> None:
        """Read messages from transport and route them."""
        try:
            async for message in self.transport.read_messages():
                if self._closed:
                    break

                msg_type = message.get("type")

                # Route control messages
                if msg_type == "control_response":
                    response = message.get("response", {})
                    request_id = response.get("request_id")
                    if request_id in self.pending_control_responses:
                        event = self.pending_control_responses[request_id]
                        if response.get("subtype") == "error":
                            self.pending_control_results[request_id] = Exception(
                                response.get("error", "Unknown error")
                            )
                        else:
                            self.pending_control_results[request_id] = response
                        event.set()
                    continue

                elif msg_type == "control_request":
                    request: ControlRequest = message  # type: ignore[assignment]
                    if self._tg:
                        self._tg.start_soon(self._handle_control_request, request)
                    continue

                elif msg_type == "control_cancel_request":
                    continue

                # Track results for proper stream closure
                if msg_type == "result":
                    self._first_result_event.set()

                # Regular SDK messages go to the stream
                await self._message_send.send(message)

        except anyio.get_cancelled_exc_class():
            logger.debug("Read task cancelled")
            raise
        except Exception as e:
            logger.error(f"Fatal error in message reader: {e}")
            for request_id, event in list(self.pending_control_responses.items()):
                if request_id not in self.pending_control_results:
                    self.pending_control_results[request_id] = e
                    event.set()
            await self._message_send.send({"type": "error", "error": str(e)})
        finally:
            # Unblock any waiters (e.g. string-prompt path waiting for first
            # result) so they don't stall for the full timeout on early exit.
            self._first_result_event.set()
            # Always signal end of stream
            await self._message_send.send({"type": "end"})

    async def _handle_control_request(self, request: ControlRequest) -> None:
        """Handle incoming control request from CLI."""
        request_id = request["request_id"]
        request_data = request["request"]
        subtype = request_data["subtype"]

        try:
            response_data: dict[str, Any] = {}

            if subtype == "can_use_tool":
                permission_request: CanUseToolControlRequest = request_data  # type: ignore[assignment]
                original_input = permission_request["input"]
                if not self.can_use_tool:
                    raise Exception("canUseTool callback is not provided")
                else:
                    context = ToolPermissionContext(
                        signal=None,
                        suggestions=[
                            PermissionUpdate.from_dict(permission)
                            for permission in (
                                permission_request.get("permission_suggestions", [])
                                or []
                            )
                            if isinstance(permission, dict)
                        ],
                        blocked_path=permission_request.get("blocked_path"),
                        decision_reason=permission_request.get("decision_reason"),
                        tool_use_id=permission_request.get("tool_use_id", ""),
                        agent_id=permission_request.get("agent_id"),
                    )

                    response = await self.can_use_tool(
                        permission_request["tool_name"],
                        permission_request["input"],
                        context,
                    )

                    if isinstance(response, PermissionResultAllow):
                        response_data = {
                            "behavior": "allow",
                            "updatedInput": (
                                response.updated_input
                                if response.updated_input is not None
                                else original_input
                            ),
                        }
                        if response.updated_permissions is not None:
                            response_data["updatedPermissions"] = [
                                permission.to_dict()
                                for permission in response.updated_permissions
                            ]
                        if response.tool_use_id is not None:
                            response_data["toolUseID"] = response.tool_use_id
                    elif isinstance(response, PermissionResultDeny):
                        response_data = {"behavior": "deny", "message": response.message}
                        if response.interrupt:
                            response_data["interrupt"] = response.interrupt
                        if response.tool_use_id is not None:
                            response_data["toolUseID"] = response.tool_use_id
                    else:
                        raise TypeError(
                            f"Tool permission callback must return PermissionResult "
                            f"(PermissionResultAllow or PermissionResultDeny), got {type(response)}"
                        )

            elif subtype == "hook_callback":
                hook_callback_request: HookCallbackControlRequest = request_data  # type: ignore[assignment]
                callback_id = hook_callback_request["callback_id"]
                callback = self.hook_callbacks.get(callback_id)
                if not callback:
                    raise Exception(f"No hook callback found for ID: {callback_id}")

                hook_output = await callback(
                    request_data.get("input"),
                    request_data.get("tool_use_id"),
                    {"signal": None},
                )
                response_data = _convert_hook_output_for_cli(hook_output)

            elif subtype == "mcp_message":
                server_name = request_data.get("server_name")
                mcp_message = request_data.get("message")

                if not server_name or not mcp_message:
                    raise Exception("Missing server_name or message for MCP request")

                assert isinstance(server_name, str)
                assert isinstance(mcp_message, dict)
                mcp_response = await self._handle_sdk_mcp_request(
                    server_name, mcp_message
                )
                response_data = {"mcp_response": mcp_response}

            elif subtype == "mcp_tool_call":
                mcp_tool_call_request: McpToolCallControlRequest = request_data  # type: ignore[assignment]
                server_name = mcp_tool_call_request.get("server_name")
                tool_name = mcp_tool_call_request.get("tool_name")
                arguments = mcp_tool_call_request.get("arguments", {})

                if not server_name or not tool_name:
                    raise Exception(
                        "Missing server_name or tool_name for MCP tool call"
                    )

                assert isinstance(server_name, str)
                assert isinstance(tool_name, str)
                assert isinstance(arguments, dict)
                response_data = {
                    "result": await self._handle_sdk_mcp_tool_call(
                        server_name, tool_name, arguments
                    )
                }

            else:
                raise Exception(f"Unsupported control request subtype: {subtype}")

            success_response: ControlResponse = {
                "type": "control_response",
                "response": {
                    "subtype": "success",
                    "request_id": request_id,
                    "response": response_data,
                },
            }
            await self.transport.write(json.dumps(success_response) + "\n")

        except Exception as e:
            error_response: ControlResponse = {
                "type": "control_response",
                "response": {
                    "subtype": "error",
                    "request_id": request_id,
                    "error": str(e),
                },
            }
            await self.transport.write(json.dumps(error_response) + "\n")

    async def _send_control_request(
        self, request: dict[str, Any], timeout: float = 60.0
    ) -> dict[str, Any]:
        """Send control request to CLI and wait for response."""
        if not self.is_streaming_mode:
            raise Exception("Control requests require streaming mode")

        self._request_counter += 1
        request_id = f"req_{self._request_counter}_{os.urandom(4).hex()}"

        event = anyio.Event()
        self.pending_control_responses[request_id] = event

        control_request = {
            "type": "control_request",
            "request_id": request_id,
            "request": request,
        }

        await self.transport.write(json.dumps(control_request) + "\n")

        try:
            with anyio.fail_after(timeout):
                await event.wait()

            result = self.pending_control_results.pop(request_id)
            self.pending_control_responses.pop(request_id, None)

            if isinstance(result, Exception):
                raise result

            response_data = result.get("response", {})
            return response_data if isinstance(response_data, dict) else {}
        except TimeoutError as e:
            self.pending_control_responses.pop(request_id, None)
            self.pending_control_results.pop(request_id, None)
            raise Exception(f"Control request timeout: {request.get('subtype')}") from e

    async def _handle_sdk_mcp_request(
        self, server_name: str, message: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle an MCP request for an SDK server."""
        if server_name not in self.sdk_mcp_servers:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Server '{server_name}' not found",
                },
            }

        server = self.sdk_mcp_servers[server_name]
        method = message.get("method")
        params = message.get("params", {})

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": server.name,
                            "version": server.version or "1.0.0",
                        },
                    },
                }

            elif method == "tools/list":
                request = ListToolsRequest(method=method)
                handler = server.request_handlers.get(ListToolsRequest)
                if handler:
                    result = await handler(request)
                    tools_data = []
                    for tool in result.root.tools:  # type: ignore[union-attr]
                        tool_data: dict[str, Any] = {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": (
                                tool.inputSchema.model_dump()
                                if hasattr(tool.inputSchema, "model_dump")
                                else tool.inputSchema
                            )
                            if tool.inputSchema
                            else {},
                        }
                        if tool.annotations:
                            tool_data["annotations"] = tool.annotations.model_dump(
                                exclude_none=True
                            )
                        tools_data.append(tool_data)
                    return {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {"tools": tools_data},
                    }

            elif method == "tools/call":
                call_request = CallToolRequest(
                    method=method,
                    params=CallToolRequestParams(
                        name=params.get("name"), arguments=params.get("arguments", {})
                    ),
                )
                handler = server.request_handlers.get(CallToolRequest)
                if handler:
                    result = await handler(call_request)
                    content = []
                    for item in result.root.content:  # type: ignore[union-attr]
                        if hasattr(item, "text"):
                            content.append({"type": "text", "text": item.text})
                        elif hasattr(item, "data") and hasattr(item, "mimeType"):
                            content.append(
                                {
                                    "type": "image",
                                    "data": item.data,
                                    "mimeType": item.mimeType,
                                }
                            )

                    response_data = {"content": content}
                    if hasattr(result.root, "is_error") and result.root.is_error:
                        response_data["is_error"] = True  # type: ignore[assignment]

                    return {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": response_data,
                    }

            elif method == "notifications/initialized":
                return {"jsonrpc": "2.0", "result": {}}

            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32601, "message": f"Method '{method}' not found"},
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32603, "message": str(e)},
            }

    async def _handle_sdk_mcp_tool_call(
        self, server_name: str, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle a direct MCP tool call request from the CLI."""
        if server_name not in self.sdk_mcp_servers:
            raise Exception(f'SDK MCP server "{server_name}" not found')

        server = self.sdk_mcp_servers[server_name]
        tool_defs = getattr(server, "_sdk_tool_definitions", [])
        for tool_def in tool_defs:
            if tool_def.name == tool_name:
                result: dict[str, Any] = await tool_def.handler(arguments)
                return result

        raise Exception(
            f'Tool "{tool_name}" not found on server "{server_name}"'
        )

    async def get_mcp_status(self) -> dict[str, Any]:
        """Get current MCP server connection status."""
        return await self._send_control_request({"subtype": "mcp_status"})

    async def set_mcp_servers(
        self, servers: dict[str, McpSetServersConfig]
    ) -> dict[str, Any]:
        """Replace the session-scoped external MCP server configuration."""
        return await self._send_control_request(
            {"subtype": "mcp_set_servers", "servers": servers}
        )

    async def interrupt(self) -> None:
        """Send interrupt control request."""
        await self._send_control_request({"subtype": "interrupt"})

    async def set_permission_mode(self, mode: str) -> None:
        """Change permission mode."""
        await self._send_control_request({"subtype": "set_permission_mode", "mode": mode})

    async def set_model(self, model: str | None) -> None:
        """Change the AI model."""
        await self._send_control_request({"subtype": "set_model", "model": model})

    async def reconnect_mcp_server(self, server_name: str) -> None:
        """Reconnect a disconnected or failed MCP server."""
        await self._send_control_request(
            {"subtype": "mcp_reconnect", "serverName": server_name}
        )

    async def authenticate_mcp_server(self, server_name: str) -> None:
        """Authenticate an OAuth-backed MCP server."""
        await self._send_control_request(
            {"subtype": "mcp_authenticate", "serverName": server_name}
        )

    async def toggle_mcp_server(self, server_name: str, enabled: bool) -> None:
        """Enable or disable an MCP server."""
        await self._send_control_request(
            {"subtype": "mcp_toggle", "serverName": server_name, "enabled": enabled}
        )

    async def stop_task(self, task_id: str) -> None:
        """Stop a running task."""
        await self._send_control_request({"subtype": "stop_task", "task_id": task_id})

    async def wait_for_result_and_end_input(self) -> None:
        """Wait for the first result then close stdin.

        Keeps stdin open until the first result arrives (or timeout) to allow
        bidirectional control protocol communication (can_use_tool permission
        requests, hook callbacks, SDK MCP tool calls, etc.).
        """
        logger.debug(
            "Waiting for first result before closing stdin "
            f"(sdk_mcp_servers={len(self.sdk_mcp_servers)}, "
            f"has_hooks={bool(self.hooks)}, "
            f"has_can_use_tool={self.can_use_tool is not None})"
        )
        with anyio.move_on_after(self._stream_close_timeout):
            await self._first_result_event.wait()

        await self.transport.end_input()

    async def stream_input(self, stream: AsyncIterable[dict[str, Any]]) -> None:
        """Stream input messages to transport.

        Waits for the first result before closing stdin to allow
        bidirectional control protocol communication.
        """
        try:
            async for message in stream:
                if self._closed:
                    break
                await self.transport.write(json.dumps(message) + "\n")

            await self.wait_for_result_and_end_input()
        except Exception as e:
            logger.debug(f"Error streaming input: {e}")

    async def receive_messages(self) -> AsyncIterator[dict[str, Any]]:
        """Receive SDK messages (not control messages)."""
        async for message in self._message_receive:
            if message.get("type") == "end":
                break
            elif message.get("type") == "error":
                raise Exception(message.get("error", "Unknown error"))
            yield message

    async def close(self) -> None:
        """Close the query and transport."""
        self._closed = True
        if self._tg:
            self._tg.cancel_scope.cancel()
        with anyio.CancelScope(shield=True):
            await self.transport.close()
        if self._tg:
            with suppress(anyio.get_cancelled_exc_class()):
                await self._tg.__aexit__(None, None, None)

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        """Return async iterator for messages."""
        return self.receive_messages()

    async def __anext__(self) -> dict[str, Any]:
        """Get next message."""
        async for message in self.receive_messages():
            return message
        raise StopAsyncIteration
