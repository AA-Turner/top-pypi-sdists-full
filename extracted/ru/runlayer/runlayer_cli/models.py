"""Pydantic models with no `mcp.types` dependency.

Kept importable by the `aiwatch` scan-only binary, which excludes `mcp` from
its PyInstaller bundle. mcp-dependent models live in `models_mcp.py`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ServerDetails(BaseModel):
    """Simplified server details model."""

    id: str
    name: str
    url: str
    transport_type: str
    transport_config: dict[str, Any] | None = None
    sync_required: bool = False
    catalog_entry_name: str | None = None

    model_config = ConfigDict(extra="ignore")
