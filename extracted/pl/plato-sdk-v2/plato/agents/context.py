"""Agent execution context models."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from opentelemetry import trace
from pydantic import BaseModel, computed_field


class AgentContext(BaseModel):
    """Context for running an agent."""

    image: str
    package: str | None = None
    config: dict[str, object]
    instruction: str
    display_name: str | None = None
    ssh_probe_timeout: int = 30
    ssh_probe_retries: int = 3
    # Runtime config (VM resource specs) — passed to agent as env var
    runtime: dict[str, object] | None = None
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
