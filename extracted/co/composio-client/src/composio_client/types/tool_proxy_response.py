# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_proxy_response."""

from __future__ import annotations

from typing import Dict, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class BinaryData(BaseModel):
    "Binary body response data. Present when the response is a binary file."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    content_type: str
    "Content-Type of the binary data"
    expires_at: Optional[str] = None
    "ISO 8601 timestamp when the URL expires"
    size: float
    "File size in bytes"
    url: str
    "URL to download binary content"


class ToolProxyResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    binary_data: Optional[BinaryData] = None
    "Binary body response data. Present when the response is a binary file."
    data: Optional[object] = None
    "The response data returned from the proxied API"
    headers: Optional[Dict[str, str]] = None
    "The HTTP headers returned from the proxied API"
    status: float
    "The HTTP status code returned from the proxied API"


__all__ = [
    "ToolProxyResponse",
    "BinaryData",
]
