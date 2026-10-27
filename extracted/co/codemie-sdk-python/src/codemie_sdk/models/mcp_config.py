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


class MCPVariableDefinition(BaseModel):
    """Definition of an environment variable required by an MCP server."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str
    required: bool = True


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


class MCPConfigCloneRequest(BaseModel):
    """Request model for cloning a global MCP configuration from a submitted form payload.

    ``is_public`` and ``is_system`` are not part of the request: the clone always
    inherits them from the source configuration.
    """

    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    server_home_url: str | None = None
    source_url: str | None = None
    logo_url: str | None = None
    categories: list[str] = Field(default_factory=list)
    config: MCPServerConfigData
    required_env_vars: list[MCPVariableDefinition] = Field(default_factory=list)


class MCPConfigUpdateRequest(BaseModel):
    """Request model for updating a global MCP configuration; only provided fields are sent."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    server_home_url: str | None = None
    source_url: str | None = None
    logo_url: str | None = None
    categories: list[str] | None = None
    config: MCPServerConfigData | None = None
    required_env_vars: list[MCPVariableDefinition] | None = None
    is_public: bool | None = None
    is_active: bool | None = None


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
    required_env_vars: list[MCPVariableDefinition] = Field(default_factory=list)
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

    configs: list[MCPConfigResponse] = Field(default_factory=list)
    total: int = 0
    page: int = 0
    per_page: int = 20
