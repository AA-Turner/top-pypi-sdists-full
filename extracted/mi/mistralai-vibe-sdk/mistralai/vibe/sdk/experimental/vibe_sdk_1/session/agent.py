"""Ergonomic Agent API for the Agent Session API."""

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass

from pydantic import JsonValue

from mistralai.vibe.sdk.providers.completion.config import (
    CompletionConfig,
    MistralCompletionConfig,
)

from .client import Session
from .hooks import SessionHooks
from .host import SessionHost
from .models import (
    AgentConfig,
    SandboxConfig,
    SessionForkParams,
    SessionResumeParams,
    SessionStartParams,
    ToolDefinition,
)

type ToolHandler = Callable[[JsonValue], JsonValue | Awaitable[JsonValue]]


@dataclass(frozen=True, slots=True)
class AgentBindings:
    """Live Python bindings held by the ergonomic client."""

    tools: Mapping[str, ToolHandler]
    hooks: SessionHooks


class Agent:
    """Ergonomic public object for configuring and starting sessions."""

    def __init__(
        self,
        *,
        session_host: SessionHost | None = None,
        completion: CompletionConfig | None = None,
        sandbox: SandboxConfig | None = None,
        instructions: str = "",
        workdir: str | None = None,
        tools: Mapping[str, ToolHandler] | None = None,
        hooks: SessionHooks | None = None,
        config: AgentConfig | None = None,
    ) -> None:
        self.session_host = session_host
        self.bindings = AgentBindings(
            tools=dict(tools or {}),
            hooks=hooks or SessionHooks(),
        )
        self.config = config or AgentConfig(
            completion=completion or MistralCompletionConfig(),
            sandbox=sandbox,
            instructions=instructions,
            workdir=workdir,
            tools=[ToolDefinition(name=name) for name in self.bindings.tools],
            hooks=list(self.bindings.hooks.definitions()),
        )

    async def start_session(self) -> Session:
        host = self._require_session_host()
        channel = await host.start(SessionStartParams(agent_config=self.config))
        return self._wrap(channel)

    async def resume_session(self, session_id: str) -> Session:
        host = self._require_session_host()
        channel = await host.resume(
            SessionResumeParams(session_id=session_id, agent_config=self.config)
        )
        return self._wrap(channel)

    async def fork_session(
        self,
        source_session_id: str,
        *,
        after_turn_id: str | None = None,
    ) -> Session:
        host = self._require_session_host()
        channel = await host.fork(
            SessionForkParams(
                source_session_id=source_session_id,
                agent_config=self.config,
                after_turn_id=after_turn_id,
            )
        )
        return self._wrap(channel)

    async def run(self, message: str) -> Session:
        session = await self.start_session()
        await session.start_turn(message)
        return session

    def _wrap(self, channel) -> Session:
        return Session(
            channel=channel,
            tools=self.bindings.tools,
            hooks=self.bindings.hooks,
        )

    def _require_session_host(self) -> SessionHost:
        if self.session_host is None:
            msg = "Agent.start_session requires a session_host in the current scaffold."
            raise RuntimeError(msg)
        return self.session_host
