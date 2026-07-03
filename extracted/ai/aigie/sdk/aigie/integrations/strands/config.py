"""User-facing configuration for the Strands integration."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Any

from aigie.tracing.config_base import FrameworkConfigBase


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


@dataclass
class StrandsConfig(FrameworkConfigBase):
    """Configuration for Strands Agents SDK tracing behavior.

    Inherits ``zero_retention: bool`` from FrameworkConfigBase. When True,
    no spans or traces are emitted for invocations driven through this
    config — Aigie still runs in-process but persistence is suppressed.

    Attributes:
        trace_agents: Whether to trace agent invocations
        trace_tools: Whether to trace tool invocations
        trace_model_calls: Whether to trace underlying model calls
        trace_multi_agent: Whether to trace multi-agent orchestration (Swarm/Graph)
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        max_content_length: Maximum content length to capture
        mask_sensitive_data: Reserved. No masking primitive exists in the SDK
            yet, so this flag is currently a no-op.
    """

    trace_agents: bool = True
    trace_tools: bool = True
    trace_model_calls: bool = True
    trace_multi_agent: bool = True
    capture_inputs: bool = True
    capture_outputs: bool = True
    max_content_length: int = 10000
    mask_sensitive_data: bool = False

    def __post_init__(self) -> None:
        if self.max_content_length < 0:
            raise ValueError("max_content_length must be >= 0")

    @classmethod
    def from_env(cls) -> StrandsConfig:
        """Create configuration from environment variables.

        Environment variables:
            AIGIE_STRANDS_TRACE_AGENTS: Trace agent invocations (default: true)
            AIGIE_STRANDS_TRACE_TOOLS: Trace tool invocations (default: true)
            AIGIE_STRANDS_TRACE_MODEL_CALLS: Trace model calls (default: true)
            AIGIE_STRANDS_TRACE_MULTI_AGENT: Trace Swarm/Graph orchestration (default: true)
            AIGIE_STRANDS_CAPTURE_INPUTS: Capture input data (default: true)
            AIGIE_STRANDS_CAPTURE_OUTPUTS: Capture output data (default: true)
            AIGIE_STRANDS_MAX_CONTENT_LENGTH: Max content length (default: 10000)
            AIGIE_STRANDS_MASK_SENSITIVE_DATA: Mask sensitive data (default: false)
            AIGIE_STRANDS_ZERO_RETENTION: Suppress persistence (default: false)
        """
        return cls(
            trace_agents=_env_bool("AIGIE_STRANDS_TRACE_AGENTS", True),
            trace_tools=_env_bool("AIGIE_STRANDS_TRACE_TOOLS", True),
            trace_model_calls=_env_bool("AIGIE_STRANDS_TRACE_MODEL_CALLS", True),
            trace_multi_agent=_env_bool("AIGIE_STRANDS_TRACE_MULTI_AGENT", True),
            capture_inputs=_env_bool("AIGIE_STRANDS_CAPTURE_INPUTS", True),
            capture_outputs=_env_bool("AIGIE_STRANDS_CAPTURE_OUTPUTS", True),
            max_content_length=_env_int("AIGIE_STRANDS_MAX_CONTENT_LENGTH", 10000),
            mask_sensitive_data=_env_bool("AIGIE_STRANDS_MASK_SENSITIVE_DATA", False),
            zero_retention=_env_bool("AIGIE_STRANDS_ZERO_RETENTION", False),
        )

    def merge(self, **overrides: Any) -> StrandsConfig:
        """Create a new config with overridden values."""
        return replace(self, **overrides)
