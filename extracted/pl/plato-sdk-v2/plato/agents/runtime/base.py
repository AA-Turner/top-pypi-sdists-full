"""Base runtime class for agent execution."""

from __future__ import annotations

import base64
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from opentelemetry import trace
from pydantic import BaseModel, computed_field


class AgentContext(BaseModel):
    """Context for running an agent."""

    image: str
    config: dict
    instruction: str
    display_name: str | None = None
    # Runtime config (VM resource specs) — passed to agent as env var
    runtime: dict | None = None
    # Path on world VM to agent code (for syncing to agent VM in dev mode)
    agent_code_path: Path | None = None

    @computed_field
    @property
    def config_b64(self) -> str:
        """Base64 encoded config for passing via environment."""
        return base64.b64encode(json.dumps(self.config).encode()).decode()

    @computed_field
    @property
    def runtime_b64(self) -> str | None:
        """Base64 encoded runtime config for passing via environment."""
        if self.runtime is None:
            return None
        return base64.b64encode(json.dumps(self.runtime).encode()).decode()

    @computed_field
    @property
    def instruction_b64(self) -> str:
        """Base64 encoded instruction for passing via environment."""
        return base64.b64encode(self.instruction.encode()).decode()


class PreparedAgent(BaseModel):
    """A prepared agent environment ready for task execution.

    Returned by Runtime.prepare() after the agent environment (container/VM)
    is started but before the agent task runs. This allows the world to
    interact with the environment (e.g., login via CDP) before execution.
    """

    model_config = {"arbitrary_types_allowed": True}

    agent_id: str  # container name or VM job_id
    hostname: str  # for networking (localhost or alias.plato.internal)
    runtime: Any  # reference to the Runtime instance for execute/cleanup


class OTelContext(BaseModel):
    """OpenTelemetry context from environment."""

    session_id: str | None = None
    otel_url: str | None = None
    upload_url: str | None = None
    traceparent: str | None = None
    trace_id: str | None = None
    parent_span_id: str | None = None

    @classmethod
    def from_env(cls) -> OTelContext:
        """Load OTel context from environment variables."""
        session_id = os.environ.get("SESSION_ID")
        otel_url = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
        upload_url = os.environ.get("UPLOAD_URL")

        # Get trace context from current span
        traceparent = None
        trace_id = None
        parent_span_id = None

        current_span = trace.get_current_span()
        span_context = current_span.get_span_context()
        if span_context.is_valid:
            trace_id = format(span_context.trace_id, "032x")
            parent_span_id = format(span_context.span_id, "016x")
            traceparent = f"00-{trace_id}-{parent_span_id}-01"

        return cls(
            session_id=session_id,
            otel_url=otel_url,
            upload_url=upload_url,
            traceparent=traceparent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
        )

    def to_env_vars(self) -> list[str]:
        """Convert to environment variable assignments."""
        env_vars = []

        if self.otel_url:
            env_vars.append(f"OTEL_EXPORTER_OTLP_ENDPOINT={self.otel_url}")
            env_vars.append(f"OTEL_EXPORTER_OTLP_TRACES_ENDPOINT={self.otel_url.rstrip('/')}/v1/traces")
            env_vars.append("OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf")
        if self.session_id:
            env_vars.append(f"SESSION_ID={self.session_id}")
        if self.upload_url:
            env_vars.append(f"UPLOAD_URL={self.upload_url}")
        if self.traceparent:
            env_vars.append(f"TRACEPARENT={self.traceparent}")
        if self.trace_id:
            env_vars.append(f"OTEL_TRACE_ID={self.trace_id}")
        if self.parent_span_id:
            env_vars.append(f"OTEL_PARENT_SPAN_ID={self.parent_span_id}")

        return env_vars


class Runtime(ABC):
    """Abstract base class for agent runtimes."""

    @abstractmethod
    async def run(self, ctx: AgentContext) -> str:
        """Run an agent and return its identifier (one-shot).

        Args:
            ctx: Agent execution context

        Returns:
            Identifier for the running agent (container name, job ID, etc.)
        """
        pass

    async def prepare(self, ctx: AgentContext) -> PreparedAgent:
        """Start agent environment without running the task.

        Starts the container/VM with desktop and Chrome ready but does NOT
        execute the agent instruction. Returns a PreparedAgent that can be
        used to interact with the environment before calling execute().

        Args:
            ctx: Agent execution context (instruction is ignored at this stage)

        Returns:
            PreparedAgent with hostname for networking and agent_id for cleanup.
        """
        raise NotImplementedError(f"{type(self).__name__} does not support two-phase execution")

    async def execute(self, prepared: PreparedAgent, ctx: AgentContext) -> None:
        """Execute agent task in a prepared environment.

        Runs the agent instruction inside an environment previously started
        by prepare(). Streams output and raises on failure.

        Args:
            prepared: The PreparedAgent returned from prepare()
            ctx: Agent execution context (uses instruction from this context)
        """
        raise NotImplementedError(f"{type(self).__name__} does not support two-phase execution")

    @abstractmethod
    async def cleanup(self, agent_id: str, error: bool = False) -> None:
        """Clean up resources for an agent.

        Args:
            agent_id: The identifier returned from run() or PreparedAgent.agent_id
            error: Whether cleanup is due to an error.
        """
        pass
