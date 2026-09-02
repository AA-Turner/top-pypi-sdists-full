"""Pydantic models with no `mcp.types` dependency.

Kept importable by the `aiwatch` scan-only binary, which excludes `mcp` from
its PyInstaller bundle. mcp-dependent models live in `models_mcp.py`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from runlayer_cli.models_api import IdentityForwardBundle


class ServerDetails(BaseModel):
    """Simplified server details model."""

    id: str
    name: str
    url: str
    transport_type: str
    transport_config: dict[str, Any] | None = None
    deployment_mode: str | None = None
    version: int | None = None
    sync_required: bool = False
    catalog_entry_name: str | None = None
    requires_manual_oauth_setup: bool = False
    manual_oauth_client_id: str | None = None
    manual_oauth_client_secret: str | None = None
    manual_oauth_scopes: str | None = None
    manual_oauth_callback_port: int | None = None
    preferred_token_endpoint_auth_method: str | None = None
    # Identity headers the backend built for this caller. ``None`` =
    # nothing to inject (stdio, toggles off, or an older backend).
    identity_forward: IdentityForwardBundle | None = None

    model_config = ConfigDict(extra="ignore")
