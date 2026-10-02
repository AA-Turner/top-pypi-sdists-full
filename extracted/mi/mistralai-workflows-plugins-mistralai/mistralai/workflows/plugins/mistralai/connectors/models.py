from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .run_as import ConnectorRunAs


class ResolvedConnectorBinding(BaseModel):
    connector_name: str
    connector_id: str | None = None
    authentication_name: str | None = None
    credentials_name: str | None = None
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO
    allow_mcp_ui: bool = False
    mcp_ui_resource_uris: dict[str, str] = Field(default_factory=dict)
    mcp_ui_resource_uris_fetched: bool = False
    status: str = "ready"


class _ResolvedConnectorBindings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    bindings: list[ResolvedConnectorBinding] = Field(default_factory=list)


class _ResolvedPluginExtension(BaseModel):
    model_config = ConfigDict(extra="ignore")

    resolved_connectors: _ResolvedConnectorBindings = Field(default_factory=_ResolvedConnectorBindings)


class ConnectorDefinition(BaseModel):
    """Shape stored in plugin_metadata by ``@uses_connectors``."""

    connector_name: str
    auto_auth: bool = True
    credentials_name: str | None = None
    allow_mcp_ui: bool = False
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO


def resolved_connector_bindings_from_extension(raw: Mapping[str, Any]) -> list[ResolvedConnectorBinding]:
    """Parse interceptor-resolved bindings from the worker-only ``trusted_extensions`` channel.

    The channel is not caller-writable, so the bindings are trusted as interceptor-owned;
    only structural validation applies.
    """
    return _ResolvedPluginExtension.model_validate(raw).resolved_connectors.bindings


class ConnectorExtensionBinding(BaseModel):
    """Runtime binding override from ``context.extensions``.

    Extra fields are ignored: identity fields like ``run_as``/``connector_id`` are
    interceptor-owned, so a caller cannot influence them through this channel.
    """

    model_config = ConfigDict(extra="ignore")

    connector_name: str | None = None
    credentials_name: str | None = None

    @field_validator("connector_name", "credentials_name")
    @classmethod
    def _reject_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("connector binding fields must not be blank when provided")
        return value


class ConnectorExtensionPayload(BaseModel):
    """Connector extension payload from ``context.extensions``."""

    model_config = ConfigDict(extra="ignore")

    bindings: list[ConnectorExtensionBinding] = Field(default_factory=list)


class MistralaiExtensionPayload(BaseModel):
    """Mistral plugin extension payload from ``context.extensions``."""

    model_config = ConfigDict(extra="ignore")

    connectors: ConnectorExtensionPayload = Field(default_factory=ConnectorExtensionPayload)


class ResolvedConnector(BaseModel):
    """Connector resolved by ID/name via the API."""

    id: str
    name: str
    description: str | None = None
