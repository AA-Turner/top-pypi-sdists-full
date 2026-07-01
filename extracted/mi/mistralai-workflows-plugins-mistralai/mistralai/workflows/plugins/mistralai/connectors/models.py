from __future__ import annotations

from pydantic import BaseModel, Field


class ResolvedConnectorBinding(BaseModel):
    connector_name: str
    connector_id: str | None = None
    authentication_name: str | None = None
    credentials_name: str | None = None
    allow_mcp_ui: bool = False
    mcp_ui_resource_uris: dict[str, str] = Field(default_factory=dict)
    mcp_ui_resource_uris_fetched: bool = False
    status: str = "ready"


class ConnectorDefinition(BaseModel):
    """Shape stored in plugin_metadata by ``@uses_connectors``."""

    connector_name: str
    auto_auth: bool = True
    credentials_name: str | None = None
    allow_mcp_ui: bool = False


class ConnectorExtensionBinding(BaseModel):
    """Runtime binding override from ``context.extensions``."""

    connector_name: str
    connector_id: str | None = None
    credentials_name: str | None = None


class ResolvedConnector(BaseModel):
    """Connector resolved by ID/name via the API."""

    id: str
    name: str
    description: str | None = None
