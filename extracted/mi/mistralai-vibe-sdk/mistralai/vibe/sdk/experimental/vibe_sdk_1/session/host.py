"""Startup and bound channel protocols for the Agent Session API."""

from collections.abc import AsyncIterator
from typing import Protocol

from .events import SessionEvent
from .models import (
    AgentConfig,
    CallbackResult,
    CommandAccepted,
    ContentBlock,
    PluginInfo,
    SessionForkParams,
    SessionResumeParams,
    SessionStartParams,
    SessionState,
    TurnRef,
)


class SessionChannel(Protocol):
    """Raw bound Layer 1 channel for one loaded session."""

    async def start_turn(self, message: list[ContentBlock]) -> TurnRef: ...

    async def steer_turn(
        self,
        expected_turn_id: str,
        message: list[ContentBlock],
    ) -> CommandAccepted: ...

    async def interrupt_turn(self, expected_turn_id: str) -> CommandAccepted: ...

    async def read(self) -> SessionState: ...

    async def rename(self, title: str) -> CommandAccepted: ...

    async def delete(self) -> CommandAccepted: ...

    async def compact(self, instructions: str | None = None) -> CommandAccepted: ...

    async def shell_command(
        self,
        command: str,
        *,
        cwd: str | None = None,
        timeout_seconds: int | None = None,
    ) -> CommandAccepted: ...

    async def read_config(self) -> AgentConfig: ...

    async def write_config(self, config: AgentConfig) -> AgentConfig: ...

    async def plugin_info(self) -> PluginInfo: ...

    async def plugin_reload(self) -> PluginInfo: ...

    def events(self) -> AsyncIterator[SessionEvent]: ...

    async def send_callback_result(self, result: CallbackResult) -> CommandAccepted: ...

    async def close(self) -> None: ...


class SessionHost(Protocol):
    """Layer 1 startup boundary returning a bound session channel."""

    async def start(self, params: SessionStartParams) -> SessionChannel: ...

    async def resume(self, params: SessionResumeParams) -> SessionChannel: ...

    async def fork(self, params: SessionForkParams) -> SessionChannel: ...
