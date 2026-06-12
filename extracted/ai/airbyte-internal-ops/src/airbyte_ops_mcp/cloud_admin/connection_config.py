# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Fetch connection configuration from Airbyte Cloud.

This module provides utilities for fetching connection configuration
from Airbyte Cloud, optionally including unmasked secrets.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path

from pydantic import BaseModel, Field

from airbyte_ops_mcp.regression_tests.connection_fetcher import fetch_connection_data
from airbyte_ops_mcp.regression_tests.connection_secret_retriever import (
    retrieve_unmasked_config,
)

logger = logging.getLogger(__name__)


class FetchConnectionConfigResult(BaseModel):
    """Result of fetching connection configuration."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable status message")
    connection_id: str = Field(description="The connection ID that was fetched")
    source_id: str | None = Field(
        default=None, description="The source ID for this connection"
    )
    source_name: str | None = Field(default=None, description="The name of the source")
    output_path: str | None = Field(
        default=None, description="Path where the config was written"
    )
    with_secrets: bool = Field(
        default=False, description="Whether secrets were included"
    )


def fetch_connection_config(
    connection_id: str,
    output_path: Path | None = None,
    with_secrets: bool = False,
    oc_issue_url: str | None = None,
) -> FetchConnectionConfigResult:
    """Fetch connection configuration from Airbyte Cloud.

    This function retrieves the source configuration for a given connection ID
    and writes it to a local JSON file. When with_secrets is True, it uses the
    internal connection-retriever to fetch unmasked secrets from the database.

    Args:
        connection_id: The UUID of the Airbyte Cloud connection.
        output_path: Path to output file or directory. If a directory, writes
            `connection-<id>-config.json` inside it. Default: writes to the
            platform temp directory (e.g. `/tmp/connection-<id>-config.json`).
        with_secrets: If True, fetch unmasked secrets from the internal database.
            Requires appropriate GCP credentials and Cloud SQL Connector access.
        oc_issue_url: Required when with_secrets is True. The OC issue URL for
            audit logging purposes.

    Returns:
        FetchConnectionConfigResult with operation status and details.

    Raises:
        ValueError: If with_secrets is True but oc_issue_url is not provided.
    """
    if with_secrets and not oc_issue_url:
        return FetchConnectionConfigResult(
            success=False,
            message="--oc-issue-url is required when using --with-secrets for audit logging",
            connection_id=connection_id,
            with_secrets=with_secrets,
        )

    # Resolve output path
    if output_path is None:
        resolved_path = (
            Path(tempfile.gettempdir()) / f"connection-{connection_id}-config.json"
        )
    elif output_path.is_dir():
        resolved_path = output_path / f"connection-{connection_id}-config.json"
    else:
        resolved_path = output_path

    # Fetch connection data via public Cloud API
    connection_data = fetch_connection_data(connection_id)

    # Get the config - either masked or unmasked
    if with_secrets:
        # Use the internal connection-retriever to get unmasked secrets
        retrieval_reason = f"CLI fetch-connection-config: {oc_issue_url}"
        unmasked_config = retrieve_unmasked_config(
            connection_id=connection_id,
            retrieval_reason=retrieval_reason,
        )

        if unmasked_config is None:
            return FetchConnectionConfigResult(
                success=False,
                message=(
                    f"Failed to retrieve unmasked secrets for connection {connection_id}. "
                    "Ensure you have GCP credentials and Cloud SQL Connector access."
                ),
                connection_id=connection_id,
                source_id=connection_data.source_id,
                source_name=connection_data.source_name,
                with_secrets=True,
            )

        config = unmasked_config
        logger.info(
            f"Retrieved unmasked config for connection {connection_id} "
            f"(reason: {retrieval_reason})"
        )
    else:
        # Use the masked config from the public API
        config = connection_data.config

    # Write config to file
    resolved_path = resolved_path.resolve()
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    config_text = json.dumps(config, indent=2)

    if with_secrets:
        # Create the file atomically with owner-only permissions so that
        # secrets are never world-readable, even briefly.
        fd = os.open(resolved_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(config_text)
    else:
        resolved_path.write_text(config_text)

    return FetchConnectionConfigResult(
        success=True,
        message=f"Successfully wrote config to {resolved_path}",
        connection_id=connection_id,
        source_id=connection_data.source_id,
        source_name=connection_data.source_name,
        output_path=str(resolved_path),
        with_secrets=with_secrets,
    )
