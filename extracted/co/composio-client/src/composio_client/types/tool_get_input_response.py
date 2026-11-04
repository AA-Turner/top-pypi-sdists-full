# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_get_input_response."""

from __future__ import annotations

from typing import Dict, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class ToolGetInputResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    arguments: Optional[Dict[str, Optional[object]]] = None
    "Key-value pairs of arguments required by the tool to accomplish the described\ntask"
    error: Optional[str] = None
    "Error message if the arguments could not be generated (null if successful)"


__all__ = [
    "ToolGetInputResponse",
]
