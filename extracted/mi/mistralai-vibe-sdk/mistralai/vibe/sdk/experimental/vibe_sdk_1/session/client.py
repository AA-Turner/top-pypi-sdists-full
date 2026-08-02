"""Ergonomic session wrapper over the raw SessionChannel."""

from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from dataclasses import dataclass
from inspect import isawaitable

from pydantic import JsonValue

from .events import (
    ClientHookCallback,
    ClientToolCallback,
    SessionCallbackEvent,
    SessionClientEvent,
)
from .hooks import SessionHooks
from .host import SessionChannel
from .models import (
    AgentConfig,
    CallbackResult,
    CommandAccepted,
    ContentBlock,
    PluginInfo,
    ProtocolError,
    SessionState,
    TextContentBlock,
    TurnRef,
)

type ToolHandler = Callable[[JsonValue], JsonValue | Awaitable[JsonValue]]


@dataclass(slots=True)
class Session:
    """Ergonomic public live session.

    It wraps a raw ``SessionChannel`` and dispatches callbacks before
    yielding client-facing session events.
    """

    channel: SessionChannel
    tools: Mapping[str, ToolHandler]
    hooks: SessionHooks

    async def start_turn(
        self,
        message: str | list[ContentBlock],
    ) -> TurnRef:
        return await self.channel.start_turn(_content_blocks(message))

    async def steer_turn(
        self,
        expected_turn_id: str,
        message: str | list[ContentBlock],
    ) -> CommandAccepted:
        return await self.channel.steer_turn(expected_turn_id, _content_blocks(message))

    async def interrupt_turn(self, expected_turn_id: str) -> CommandAccepted:
        return await self.channel.interrupt_turn(expected_turn_id)

    async def read(self) -> SessionState:
        return await self.channel.read()

    async def rename(self, title: str) -> CommandAccepted:
        return await self.channel.rename(title)

    async def delete(self) -> CommandAccepted:
        return await self.channel.delete()

    async def compact(self, instructions: str | None = None) -> CommandAccepted:
        return await self.channel.compact(instructions)

    async def shell_command(
        self,
        command: str,
        *,
        cwd: str | None = None,
        timeout_seconds: int | None = None,
    ) -> CommandAccepted:
        return await self.channel.shell_command(
            command,
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )

    async def read_config(self) -> AgentConfig:
        return await self.channel.read_config()

    async def write_config(self, config: AgentConfig) -> AgentConfig:
        return await self.channel.write_config(config)

    async def plugin_info(self) -> PluginInfo:
        return await self.channel.plugin_info()

    async def plugin_reload(self) -> PluginInfo:
        return await self.channel.plugin_reload()

    def events(self) -> AsyncIterator[SessionClientEvent]:
        return self._iter_client_events()

    async def close(self) -> None:
        await self.channel.close()

    async def _iter_client_events(self) -> AsyncIterator[SessionClientEvent]:
        async for event in self.channel.events():
            if isinstance(event, SessionCallbackEvent):
                await self._handle_callback(event)
                continue
            yield event

    async def _handle_callback(self, event: SessionCallbackEvent) -> None:
        callback = event.callback
        if isinstance(callback, ClientToolCallback):
            await self._handle_client_tool(callback)
            return
        if isinstance(callback, ClientHookCallback):
            await self._handle_client_hook(callback)
            return
        await self.channel.send_callback_result(
            CallbackResult(
                callback_id=callback.id,
                error=ProtocolError(
                    code="handler_not_found",
                    message=f"No ergonomic handler registered for callback kind {callback.kind!r}.",
                ),
            )
        )

    async def _handle_client_tool(self, callback: ClientToolCallback) -> None:
        handler = self.tools.get(callback.name)
        if handler is None:
            await self.channel.send_callback_result(
                CallbackResult(
                    callback_id=callback.id,
                    error=ProtocolError(
                        code="handler_not_found",
                        message=f"No handler registered for client tool {callback.name!r}.",
                    ),
                )
            )
            return

        try:
            output = handler(callback.input)
            if isawaitable(output):
                output = await output
            result = CallbackResult(callback_id=callback.id, output=output)
        except Exception as exc:
            result = CallbackResult(
                callback_id=callback.id,
                error=ProtocolError(code="handler_error", message=str(exc)),
            )

        await self.channel.send_callback_result(result)

    async def _handle_client_hook(self, callback: ClientHookCallback) -> None:
        handler = self.hooks.handler_for(callback)
        if handler is None:
            await self.channel.send_callback_result(
                CallbackResult(
                    callback_id=callback.id,
                    error=ProtocolError(
                        code="handler_not_found",
                        message=f"No handler registered for client hook {callback.name!r}.",
                    ),
                )
            )
            return

        try:
            output = handler(callback.input)
            if isawaitable(output):
                output = await output
            result = CallbackResult(callback_id=callback.id, output=output)
        except Exception as exc:
            result = CallbackResult(
                callback_id=callback.id,
                error=ProtocolError(code="handler_error", message=str(exc)),
            )

        await self.channel.send_callback_result(result)


def _content_blocks(message: str | list[ContentBlock]) -> list[ContentBlock]:
    if isinstance(message, str):
        return [TextContentBlock(text=message)]
    return message
