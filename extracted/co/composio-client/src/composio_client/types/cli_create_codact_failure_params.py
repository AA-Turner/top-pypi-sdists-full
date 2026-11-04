# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli_create_codact_failure_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, Required, TypedDict


class ToolInfoTool(TypedDict, total=False):
    slug: Required[str]
    version: Required[str]


class ToolInfo(TypedDict, total=False):
    "Optional tool metadata when the failure can be tied to a toolkit or concrete tool version."

    toolkit: NotRequired[str]
    tool: NotRequired[ToolInfoTool]


class CliCreateCodactFailureParams(TypedDict, total=False):
    failure_type: Required[Literal["wrong_tool_slug", "wrong_tool_input_param"]]
    tool_info: NotRequired[ToolInfo]
    ctx: Required[dict[str, object | None]]
    session: Required[dict[str, object | None]]
    request_id: NotRequired[str]
    x_user_api_key: Required[str]


__all__ = [
    "CliCreateCodactFailureParams",
    "ToolInfoTool",
    "ToolInfo",
]
