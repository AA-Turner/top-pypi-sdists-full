# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_execute_response."""

from __future__ import annotations

from typing import Dict, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class ToolExecuteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    data: Dict[str, Optional[object]]
    "Tool execution output data that varies based on the specific tool"
    error: Optional[str] = None
    "Error message if the tool execution was not successful (null if successful)"
    log_id: Optional[str] = None
    "Unique identifier for the execution log (useful for debugging and support)"
    session_info: Optional[object] = None
    "Optional session information for tools that return session context"
    successful: bool
    "Indicates if the tool execution was successful"


__all__ = [
    "ToolExecuteResponse",
]
