"""SDK-owned harness agent for integration tests."""

from __future__ import annotations

import inspect
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import ClassVar

import cloudpickle
from pydantic import Field

from plato.agents import AgentConfig, BaseAgent, register_agent
from plato.agents.mounts import AgentWorkspaceMountPayload
from plato.agents.testing.spec import (
    call_agent_test_hook,
    load_agent_test_spec,
)
from plato.otel import emit_step, get_tracer, session_span

logger = logging.getLogger(__name__)
tracer = get_tracer("test-harness-agent")


class TestHarnessAgentConfig(AgentConfig):
    """Config for the SDK-owned harness agent."""

    test_spec_path: str = Field(
        default="",
        description="Path to a serialized AgentTestSpec bundle.",
    )
    payload_path: str = Field(
        default="",
        description="Path to a cloudpickled callable to execute inside the agent workspace.",
    )
    workspace_dir: str = Field(
        default="",
        description="Legacy single-workspace directory visible to the agent.",
    )
    plato_mounts: list[AgentWorkspaceMountPayload] = Field(
        default_factory=list,
        description="Runtime mount metadata injected by AgentTask.",
    )
    mcp_server_url: str = Field(
        default="",
        description="World-hosted MCP server URL. When set, the agent can call MCP tools.",
    )
    mcp_server_name: str = Field(
        default="webclone-service-tools",
        description="MCP server name key.",
    )


@dataclass(slots=True)
class _HarnessAgentContext:
    config: TestHarnessAgentConfig
    workspace: Path
    instruction: str
    mounts: list[AgentWorkspaceMountPayload]
    call_mcp_tool: Callable[..., object] | None = None


def _tool_result_payload(result: object) -> dict[str, object]:
    """Extract a JSON-serializable payload from an MCP tool result."""
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        return structured
    content = getattr(result, "content", None) or []
    for block in content:
        text = getattr(block, "text", None)
        if isinstance(text, str):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue
    return {"raw": str(result)}


@register_agent("test-harness-agent")
class TestHarnessAgent(BaseAgent[TestHarnessAgentConfig]):
    """Execute a serialized callable inside the agent VM."""

    name: ClassVar[str] = "test-harness-agent"
    description: ClassVar[str] = "SDK-owned harness agent for integration tests"

    async def run(self, instruction: str) -> None:
        context = self._context(instruction)
        if not context.mounts:
            context.workspace.mkdir(parents=True, exist_ok=True)

        if self.config.test_spec_path:
            await self._run_spec(Path(self.config.test_spec_path), context)
            return

        payload = self._load_payload(Path(self.config.payload_path))
        await self._invoke_payload(payload, context)

    def _context(self, instruction: str) -> _HarnessAgentContext:
        mounts = list(self.config.plato_mounts)
        if mounts:
            primary = Path(mounts[0].agent_path)
        elif self.config.workspace_dir:
            primary = Path(self.config.workspace_dir)
        else:
            primary = Path("/workspace")

        return _HarnessAgentContext(
            config=self.config,
            workspace=primary,
            instruction=instruction,
            mounts=mounts,
            call_mcp_tool=self.call_mcp_tool,
        )

    async def _run_spec(self, spec_path: Path, context: _HarnessAgentContext) -> None:
        spec = load_agent_test_spec(spec_path)

        with session_span(
            tracer,
            agent_name="test-harness-agent",
            agent_version="0.1.0",
            model_name="test-harness-no-llm",
        ):
            emit_step(tracer, step_id=1, source="system", message=f"Test harness agent spec={spec.name}")
            emit_step(tracer, step_id=2, source="user", message=context.instruction)
            emit_step(
                tracer,
                step_id=3,
                source="agent",
                message=f"Execute test payload from {spec_path}",
                model_name="test-harness-no-llm",
            )

            try:
                await call_agent_test_hook(spec.run, context)
            except Exception as exc:
                import traceback

                emit_step(
                    tracer,
                    step_id=4,
                    source="agent",
                    message=f"Test payload FAILED for {spec.name}: {exc}\n{traceback.format_exc()}",
                    observation={
                        "workspace": str(context.workspace),
                        "status": "error",
                        "error": str(exc),
                    },
                )
                raise

            emit_step(
                tracer,
                step_id=4,
                source="agent",
                message=f"Test payload finished for {spec.name}",
                observation={
                    "workspace": str(context.workspace),
                    "mount_paths": [mount.agent_path for mount in context.mounts],
                    "status": "ok",
                },
            )

    async def call_mcp_tool(
        self,
        tool_name: str,
        arguments: dict[str, object],
        *,
        step_id: int = 10,
    ) -> dict[str, object]:
        """Call a world-hosted MCP tool with proper OTel spans.

        Connects to the MCP server URL from config, calls the tool, emits
        tool_call + observation spans exactly like claude-code / test-agent.

        Returns the tool result payload as a dict.
        """
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client

        mcp_url = self.config.mcp_server_url
        if not mcp_url:
            raise RuntimeError("call_mcp_tool requires mcp_server_url in agent config")

        # Emit tool call span
        emit_step(
            tracer,
            step_id=step_id,
            source="agent",
            message=f"Call MCP tool {tool_name}",
            model_name="test-harness-no-llm",
            tool_calls=[
                {
                    "function_name": tool_name,
                    "tool_call_id": f"mcp_tool_{step_id}",
                    "arguments": arguments,
                }
            ],
        )

        logger.info("Calling MCP tool %s at %s", tool_name, mcp_url)
        async with streamable_http_client(mcp_url) as (read_stream, write_stream, _):
            async with ClientSession(
                read_stream,
                write_stream,
                read_timeout_seconds=timedelta(seconds=120),
            ) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)

        payload = _tool_result_payload(result)
        is_error = getattr(result, "isError", False)

        # Emit observation span
        emit_step(
            tracer,
            step_id=step_id + 1,
            source="system",
            message=json.dumps(payload, default=str)[:2000],
            observation={
                "tool_name": tool_name,
                "is_error": is_error,
                "payload": payload,
            },
        )

        logger.info(
            "MCP tool %s returned: error=%s payload_keys=%s",
            tool_name,
            is_error,
            list(payload.keys()),
        )
        return payload

    def _load_payload(self, payload_path: Path) -> Callable[..., object]:
        if not payload_path.exists():
            raise FileNotFoundError(f"Payload file does not exist: {payload_path}")
        payload = cloudpickle.loads(payload_path.read_bytes())
        if not callable(payload):
            raise TypeError(f"Payload at {payload_path} is not callable")
        return payload

    async def _invoke_payload(self, payload: Callable[..., object], context: _HarnessAgentContext) -> None:
        signature = inspect.signature(payload)
        kwargs: dict[str, object] = {}
        if "workspace" in signature.parameters:
            kwargs["workspace"] = context.workspace
        if "instruction" in signature.parameters:
            kwargs["instruction"] = context.instruction
        if "config" in signature.parameters:
            kwargs["config"] = context.config
        if "mounts" in signature.parameters:
            kwargs["mounts"] = context.mounts

        result = payload(**kwargs)
        if inspect.isawaitable(result):
            await result
