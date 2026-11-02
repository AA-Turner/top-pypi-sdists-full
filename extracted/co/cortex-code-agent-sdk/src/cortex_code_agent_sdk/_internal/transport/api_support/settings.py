"""Environment and prompt helpers for direct Agent API transport."""

from __future__ import annotations

import os

from ....types import CortexCodeAgentOptions


def _resolve_system_prompts(options: CortexCodeAgentOptions) -> tuple[str, str | None]:
    system_prompt = options.system_prompt if isinstance(options.system_prompt, str) else ""
    append_parts: list[str] = []
    if isinstance(options.system_prompt, dict) and options.system_prompt.get("type") == "preset":
        append = options.system_prompt.get("append")
        if isinstance(append, str) and append:
            append_parts.append(append)
    if options.append_system_prompt:
        append_parts.append(options.append_system_prompt)
    return system_prompt, "\n".join(append_parts) if append_parts else None

def _sandbox_enabled(options: CortexCodeAgentOptions) -> bool:
    return bool(options.snowflake_sandbox and options.snowflake_sandbox.enabled)

def _merged_env(options: CortexCodeAgentOptions) -> dict[str, str]:
    return {**os.environ, **options.env}

def _is_truthy(value: str | None) -> bool:
    return value is not None and value.lower() in {"1", "true", "yes", "on"}
