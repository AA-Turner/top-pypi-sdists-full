"""Cortex Code SDK Client.
"""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import asdict, replace
from typing import Any

from ._errors import CLIConnectionError
from ._internal.transport import Transport
from .types import (
    CortexCodeAgentOptions,
    HookEvent,
    HookMatcher,
    McpSetServersConfig,
    McpSetServersResult,
    McpStatusResponse,
    Message,
    ResultMessage,
)


class CortexCodeSDKClient:
    """Client for bidirectional, interactive conversations with Cortex Code.

    This client provides full control over the conversation flow with support
    for streaming, interrupts, and dynamic message sending. For simple one-shot
    queries, consider using the query() function instead.

    Usage:
        async with CortexCodeSDKClient(options) as client:
            await client.query("What is 2+2?")
            async for msg in client.receive_response():
                print(msg)
    """

    def __init__(
        self,
        options: CortexCodeAgentOptions | None = None,
        transport: Transport | None = None,
    ):
        if options is None:
            options = CortexCodeAgentOptions()
        self.options = options
        self._custom_transport = transport
        self._transport: Transport | None = None
        self._query: Any | None = None
        self._abort_task: asyncio.Task[None] | None = None

    @property
    def pid(self) -> int | None:
        """Process ID of the underlying CLI process."""
        if self._transport is not None:
            return self._transport.pid
        return None

    def _convert_hooks_to_internal_format(
        self, hooks: dict[HookEvent, list[HookMatcher]]
    ) -> dict[str, list[dict[str, Any]]]:
        """Convert HookMatcher format to internal Query format."""
        internal_hooks: dict[str, list[dict[str, Any]]] = {}
        for event, matchers in hooks.items():
            internal_hooks[event] = []
            for matcher in matchers:
                internal_matcher: dict[str, Any] = {
                    "matcher": matcher.matcher if hasattr(matcher, "matcher") else None,
                    "hooks": matcher.hooks if hasattr(matcher, "hooks") else [],
                }
                if hasattr(matcher, "timeout") and matcher.timeout is not None:
                    internal_matcher["timeout"] = matcher.timeout
                internal_hooks[event].append(internal_matcher)
        return internal_hooks

    async def connect(self) -> None:
        """Connect to the CLI process.

        Examples:
            client = CortexCodeSDKClient(options)
            await client.connect()
            await client.query("First turn")
            async for message in client.receive_response():
                print(message)
        """
        from ._internal.query import Query
        from ._internal.transport.api import (
            AgentApiTransport,
            should_use_api_mode,
            validate_api_mode_options,
        )
        from ._internal.transport.subprocess_cli import SubprocessCLITransport

        use_api_mode = self._custom_transport is None and should_use_api_mode(self.options)

        # Validate and configure permission settings
        if use_api_mode:
            validate_api_mode_options(self.options)
            options = self.options
        elif self.options.can_use_tool:
            if self.options.permission_prompt_tool_name:
                raise ValueError(
                    "can_use_tool callback cannot be used with permission_prompt_tool_name. "
                    "Please use one or the other."
                )
            options = replace(self.options, permission_prompt_tool_name="stdio")
        else:
            options = self.options

        if self._custom_transport:
            self._transport = self._custom_transport
        elif use_api_mode:
            self._transport = AgentApiTransport(
                options=options,
            )
        else:
            self._transport = SubprocessCLITransport(
                options=options,
            )
        await self._transport.connect()

        # Extract SDK MCP servers from options
        sdk_mcp_servers = {}
        if self.options.mcp_servers and isinstance(self.options.mcp_servers, dict):
            for name, config in self.options.mcp_servers.items():
                if isinstance(config, dict) and config.get("type") == "sdk":
                    sdk_mcp_servers[name] = config["instance"]  # type: ignore[typeddict-item]

        # Calculate initialize timeout from env var if set
        initialize_timeout_ms = int(
            os.environ.get("CORTEX_CODE_STREAM_CLOSE_TIMEOUT", "60000")
        )
        initialize_timeout = max(initialize_timeout_ms / 1000.0, 60.0)

        # Convert agents to dict format for initialize request
        agents_dict: dict[str, dict[str, Any]] | None = None
        if self.options.agents:
            agents_dict = {
                name: {k: v for k, v in asdict(agent_def).items() if v is not None}
                for name, agent_def in self.options.agents.items()
            }

        # Resolve system prompt for initialize
        system_prompt_str: str | None = None
        append_system_prompt_str: str | None = None
        if self.options.system_prompt is not None:
            if isinstance(self.options.system_prompt, str):
                system_prompt_str = self.options.system_prompt
            elif (
                isinstance(self.options.system_prompt, dict)
                and self.options.system_prompt.get("type") == "preset"
            ):
                append_val = self.options.system_prompt.get("append")
                if append_val:
                    append_system_prompt_str = append_val

        # Handle direct append_system_prompt option (like TypeScript SDK)
        if self.options.append_system_prompt is not None:
            if append_system_prompt_str:
                # Combine with preset append value
                append_system_prompt_str = append_system_prompt_str + "\n" + self.options.append_system_prompt
            else:
                append_system_prompt_str = self.options.append_system_prompt

        self._query = Query(
            transport=self._transport,
            is_streaming_mode=True,
            can_use_tool=self.options.can_use_tool,
            hooks=self._convert_hooks_to_internal_format(self.options.hooks)
            if self.options.hooks
            else None,
            sdk_mcp_servers=sdk_mcp_servers,
            initialize_timeout=initialize_timeout,
            agents=agents_dict,
            system_prompt=system_prompt_str,
            append_system_prompt=append_system_prompt_str,
            setting_sources=list(self.options.setting_sources)
            if self.options.setting_sources is not None
            else None,
        )

        await self._query.start()
        # Initialize control protocol (sends hooks, agents, etc.)
        await self._query.initialize()

        # Wire abort_event to send interrupt when set
        if self.options.abort_event is not None:
            self._abort_task = asyncio.create_task(
                self._watch_abort_event(self.options.abort_event)
            )

    async def query(
        self,
        prompt: str | AsyncIterable[dict[str, Any]],
        session_id: str = "default",
    ) -> None:
        """Send a prompt to the agent.

        Args:
            prompt: Either a string message or an async iterable of message dicts.
            session_id: Session identifier for the conversation.
        """
        if not self._query or not self._transport:
            raise CLIConnectionError("Not connected. Call connect() first.")

        if isinstance(prompt, str):
            # Send user message via control protocol (matching TypeScript SDK)
            message = {
                "type": "user",
                "session_id": session_id,
                "message": {"role": "user", "content": [{"type": "text", "text": prompt}]},
                "parent_tool_use_id": None,
            }
            await self._transport.write(json.dumps(message) + "\n")
        else:
            async for msg in prompt:
                # G-052: the streaming-prompt path carries end-user content
                # only. Pin the frame type so a caller-supplied dict cannot
                # smuggle a control_request (e.g. set_permission_mode) over
                # the SDK->CLI stdin channel. Control requests must go via
                # the dedicated client methods.
                msg = {**msg, "type": "user"}
                if "session_id" not in msg:
                    msg["session_id"] = session_id
                await self._transport.write(json.dumps(msg) + "\n")

    async def receive_messages(self) -> AsyncIterator[Message]:
        """Receive all messages from the agent."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")

        from ._internal.message_parser import parse_message

        async for data in self._query.receive_messages():
            message = parse_message(data)
            if message is not None:
                yield message

    async def receive_response(self) -> AsyncIterator[Message]:
        """Receive messages until a ResultMessage (inclusive)."""
        async for message in self.receive_messages():
            yield message
            if isinstance(message, ResultMessage):
                return

    async def interrupt(self) -> None:
        """Send interrupt via control protocol."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.interrupt()

    async def set_model(self, model: str | None = None) -> None:
        """Change the model during conversation."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.set_model(model)

    async def set_permission_mode(self, mode: str) -> None:
        """Change permission mode during conversation."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.set_permission_mode(mode)

    async def reconnect_mcp_server(self, server_name: str) -> None:
        """Reconnect a specific MCP server.

        Args:
            server_name: Name of the MCP server to reconnect.
        """
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.reconnect_mcp_server(server_name)

    async def authenticate_mcp_server(self, server_name: str) -> None:
        """Authenticate an OAuth-backed MCP server.

        Args:
            server_name: Name of the MCP server to authenticate.
        """
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.authenticate_mcp_server(server_name)

    async def toggle_mcp_server(self, server_name: str, enabled: bool) -> None:
        """Enable or disable a specific MCP server.

        Args:
            server_name: Name of the MCP server to toggle.
            enabled: True to enable, False to disable.
        """
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.toggle_mcp_server(server_name, enabled)

    async def set_mcp_servers(
        self, servers: dict[str, McpSetServersConfig]
    ) -> McpSetServersResult:
        """Replace the session-scoped external MCP server configuration.

        Passing an empty dict clears SDK-managed session MCP servers.

        Args:
            servers: Mapping of MCP server name to stdio/http/sse config.
        """
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        result: McpSetServersResult = await self._query.set_mcp_servers(servers)
        return result

    async def stop_task(self, task_id: str) -> None:
        """Stop a running subagent task.

        Args:
            task_id: ID of the task to stop.
        """
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        await self._query.stop_task(task_id)

    async def get_mcp_status(self) -> McpStatusResponse:
        """Get current MCP server connection status."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        result: McpStatusResponse = await self._query.get_mcp_status()
        return result

    async def get_server_info(self) -> dict[str, Any] | None:
        """Get server initialization info including available commands."""
        if not self._query:
            raise CLIConnectionError("Not connected. Call connect() first.")
        return getattr(self._query, "_initialization_result", None)

    async def _watch_abort_event(self, event: asyncio.Event) -> None:
        """Watch an asyncio.Event and send interrupt when it is set."""
        await event.wait()
        if self._query:
            await self._query.interrupt()

    async def disconnect(self) -> None:
        """Disconnect from the CLI process."""
        if self._abort_task is not None:
            self._abort_task.cancel()
            self._abort_task = None
        if self._query:
            await self._query.close()
            self._query = None
        self._transport = None

    async def __aenter__(self) -> CortexCodeSDKClient:
        """Enter async context - connects automatically."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Exit async context - always disconnects."""
        await self.disconnect()
        return False
