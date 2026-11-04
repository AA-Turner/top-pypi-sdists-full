# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_get_input_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class ToolGetInputParams(TypedDict, total=False):
    text: Required[str]
    "Natural language description of what you want to accomplish with this tool"
    custom_description: str
    "Custom description of the tool to help guide the LLM in generating more accurate\ninputs"
    system_prompt: str
    "System prompt to control and guide the behavior of the LLM when generating\ninputs"
    version: str
    "Tool version to use when generating inputs (defaults to \"latest\" if not\nspecified)"


__all__ = [
    "ToolGetInputParams",
]
