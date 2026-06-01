# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Exceptions for connector-secret operations."""

from __future__ import annotations

from dataclasses import dataclass

from airbyte_ops_mcp.connector_secrets._gcp_urls import get_gcp_secret_url


@dataclass(kw_only=True)
class ConnectorSecretWithNoValidVersionsError(Exception):
    """Raised when a connector secret has no enabled versions in GSM."""

    connector_name: str
    secret_name: str
    gcp_project_id: str

    def __str__(self) -> str:
        """Render a human-readable message including a console link to the secret."""
        url = get_gcp_secret_url(self.secret_name, self.gcp_project_id)
        return (
            f"No valid versions found for secret '{self.secret_name}' in connector "
            f"'{self.connector_name}'. Please check the following URL for more "
            f"information:\n- {url}"
        )
