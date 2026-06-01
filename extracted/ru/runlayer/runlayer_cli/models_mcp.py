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
