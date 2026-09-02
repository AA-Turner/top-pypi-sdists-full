"""Pydantic models that depend on `mcp.types`.

Kept separate from `models.py` so the `aiwatch` scan-only binary — which
excludes `mcp` from its PyInstaller bundle — can still import `models.py`
without pulling in `mcp`. Only the `runlayer run` / middleware / sync path
imports this module.
"""

from __future__ import annotations

import datetime
from typing import Any, Optional

import mcp.types as mt
from pydantic import BaseModel


class LocalCapabilities(BaseModel):
    tools: dict[str, mt.Tool]
    resources: dict[str, mt.Resource]
    prompts: dict[str, mt.Prompt]
    synced_at: datetime.datetime


class PreRequest(BaseModel):
    method: str
    params: dict[str, Any] | None


class UpstreamError(BaseModel):
    """Why the upstream MCP call failed, as observed by the CLI."""

    type: str  # exception class name, e.g. "ConnectError", "ReadTimeout"
    message: str


class PostRequest(PreRequest):
    result: Optional[
        list[mt.ContentBlock]
        | tuple[list[mt.ContentBlock], dict[str, Any]]
        | list[mt.Tool]
        | list[mt.Resource]
        | mt.CallToolResult
        | None
    ]
    correlation_id: str
    inject_synthetic_tool_on_policy_block: bool | None = False
    # Set when the upstream MCP was unreachable and `result` is an in-band
    # error placeholder; the backend audits a tool_list/tool_call error.
    upstream_error: UpstreamError | None = None
