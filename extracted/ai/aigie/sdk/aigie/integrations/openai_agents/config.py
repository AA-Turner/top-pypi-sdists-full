"""Configuration for OpenAI Agents SDK tracing."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Any

from aigie.tracing.config_base import FrameworkConfigBase


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class OpenAIAgentsConfig(FrameworkConfigBase):
    """Controls captured OpenAI Agents SDK trace content."""

    capture_inputs: bool = True
    capture_outputs: bool = True

    @classmethod
    def from_env(cls) -> OpenAIAgentsConfig:
        return cls(
            capture_inputs=_env_bool("AIGIE_OPENAI_AGENTS_CAPTURE_INPUTS", True),
            capture_outputs=_env_bool("AIGIE_OPENAI_AGENTS_CAPTURE_OUTPUTS", True),
            zero_retention=_env_bool("AIGIE_OPENAI_AGENTS_ZERO_RETENTION", False),
        )

    def merge(self, **overrides: Any) -> OpenAIAgentsConfig:
        return replace(self, **overrides)
