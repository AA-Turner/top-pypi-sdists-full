"""MCP Configuration models for Settings > MCPs management."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class MCPServerConfigData(BaseModel):
    """MCP server configuration data (mirrors the catalog config format)."""

    model_config = ConfigDict(extra="ignore")

    command: str | None = None
    url: str | None = None
    args: list[str] = Field(default_factory=list)
    headers: dict[str, str] = Field(default_factory=dict)
    env: dict[str, Any] = Field(default_factory=dict)
    type: str | None = None
    auth_token: str | None = None
    single_usage: bool = False
    tools: list[str] | None = None
    audience: str | None = None
    auth_config: dict[str, Any] | None = None
    allow_issuer_prefix_match: bool = False


class MCPConfigCreateRequest(BaseModel):
    """Request model for creating a global MCP configuration entry."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    server_home_url: str | None = None
    source_url: str | None = None
    logo_url: str | None = None
    categories: list[str] = Field(default_factory=list)
    config: MCPServerConfigData
    is_public: bool = False


class MCPConfigResponse(BaseModel):
    """Response model for a global MCP configuration entry."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    description: str | None = None
    server_home_url: str | None = None
    source_url: str | None = None
    logo_url: str | None = None
    categories: list[str] = Field(default_factory=list)
    config: MCPServerConfigData | None = None
    user_id: str | None = None
    is_public: bool = False
    is_system: bool = False
    usage_count: int = 0
    is_active: bool = True
    date: datetime | None = None
    update_date: datetime | None = None


class MCPConfigListResponse(BaseModel):
    """Response model for listing global MCP configurations."""

    model_config = ConfigDict(extra="ignore")

    data: list[MCPConfigResponse] = Field(default_factory=list)
    total: int = 0
    page: int = 0
    per_page: int = 20
