# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Retrieve unmasked connection secrets via vendored connection-retriever.

This module provides a focused utility for enriching connection config with
unmasked secrets from the vendored connection-retriever code. It is designed
to work alongside the existing connection_fetcher module, which handles all
other connection data via the public Cloud API.

The secret retriever requires:
- GCP credentials with appropriate permissions
- Cloud SQL Python Connector access to internal Postgres

Usage:
    from airbyte_ops_mcp.regression_tests.connection_fetcher import fetch_connection_data
    from airbyte_ops_mcp.regression_tests.connection_secret_retriever import (
        enrich_config_with_secrets,
        should_use_secret_retriever,
    )

    # Fetch connection data via public API (config will have masked secrets)
    connection_data = fetch_connection_data(connection_id)

    # Enrich with unmasked secrets if enabled
    if should_use_secret_retriever():
        connection_data = enrich_config_with_secrets(
            connection_data,
            retrieval_reason="MCP live test",
        )
"""

from __future__ import annotations

import logging
import os
from dataclasses import replace
from typing import TYPE_CHECKING, Any

from airbyte_ops_mcp.connection_config_retriever import (
    ConnectionObject,
    retrieve_objects,
)
from airbyte_ops_mcp.regression_tests.connection_fetcher import merge_stream_schemas

if TYPE_CHECKING:
    from airbyte_ops_mcp.regression_tests.connection_fetcher import ConnectionData

logger = logging.getLogger(__name__)

# Environment variable to enable secret retrieval
ENV_USE_SECRET_RETRIEVER = "USE_CONNECTION_SECRET_RETRIEVER"


def is_secret_retriever_enabled() -> bool:
    """Check if secret retrieval is enabled via environment variable.

    Returns:
        True if USE_CONNECTION_SECRET_RETRIEVER is set to a truthy value.
    """
    value = os.getenv(ENV_USE_SECRET_RETRIEVER, "").lower()
    return value in ("true", "1", "yes")


def should_use_secret_retriever() -> bool:
    """Check if secret retrieval should be used.

    Returns:
        True if USE_CONNECTION_SECRET_RETRIEVER env var is set to a truthy value.
    """
    return is_secret_retriever_enabled()


def retrieve_unmasked_config(
    connection_id: str,
    retrieval_reason: str = "MCP live tests",
) -> dict | None:
    """Retrieve unmasked source config from vendored connection-retriever.

    This function directly queries the internal Postgres database to get
    the source configuration with unmasked secrets.

    Args:
        connection_id: The Airbyte Cloud connection ID.
        retrieval_reason: Reason for retrieval (for audit logging).

    Returns:
        The unmasked source config dict, or None if retrieval fails.
    """
    # Only request the source config - that's all we need for secrets
    requested_objects = [ConnectionObject.SOURCE_CONFIG]

    candidates = retrieve_objects(
        connection_objects=requested_objects,
        retrieval_reason=retrieval_reason,
        connection_id=connection_id,
    )

    if not candidates:
        logger.warning(
            f"No connection data found for connection ID {connection_id} "
            "via connection-retriever"
        )
        return None

    candidate = candidates[0]
    if candidate.source_config:
        return dict(candidate.source_config)

    return None


def retrieve_configured_catalog(
    connection_id: str,
    retrieval_reason: str = "MCP live tests",
) -> dict[str, Any] | None:
    """Retrieve the connection's configured catalog from the internal database.

    The platform-stored catalog contains the full per-stream `jsonSchema`,
    which is not available via the public Cloud API.

    Args:
        connection_id: The Airbyte Cloud connection ID.
        retrieval_reason: Reason for retrieval (for audit logging).

    Returns:
        The configured catalog dict (platform format), or None if unavailable.
    """
    candidates = retrieve_objects(
        connection_objects=[ConnectionObject.CONFIGURED_CATALOG],
        retrieval_reason=retrieval_reason,
        connection_id=connection_id,
    )

    if not candidates:
        logger.warning(
            f"No connection data found for connection ID {connection_id} "
            "via connection-retriever"
        )
        return None

    candidate = candidates[0]
    if candidate.configured_catalog:
        return dict(candidate.configured_catalog)

    return None


def enrich_catalog_schemas_from_platform_db(
    connection_data: ConnectionData,
    retrieval_reason: str = "MCP live tests",
) -> tuple[ConnectionData, int]:
    """Fill in per-stream `json_schema` from the internal-Postgres catalog.

    Fallback path for when the Cloud API catalog
    (`enrich_catalog_schemas_from_cloud`) leaves streams without schemas.
    Reads the platform-stored configured catalog from the internal database
    (audit-logged, gated by `USE_CONNECTION_SECRET_RETRIEVER`) and merges
    each stream's `jsonSchema` into the configured catalog by stream name.

    Args:
        connection_data: The connection data to enrich.
        retrieval_reason: Reason for retrieval (for audit logging).

    Returns:
        Tuple of `(connection_data, merged_stream_count)`. If the stored
        catalog cannot be retrieved or no schemas were merged, the original
        data is returned with a count of 0.
    """
    db_catalog = retrieve_configured_catalog(
        connection_id=connection_data.connection_id,
        retrieval_reason=retrieval_reason,
    )
    if not db_catalog:
        logger.warning(
            "Could not retrieve stored catalog for connection "
            f"{connection_data.connection_id}; leaving stream schemas empty"
        )
        return connection_data, 0

    catalog, merged_count = merge_stream_schemas(connection_data.catalog, db_catalog)
    if merged_count == 0:
        logger.warning(
            "Stored catalog for connection "
            f"{connection_data.connection_id} yielded no stream schemas to merge"
        )
        return connection_data, 0

    logger.info(
        f"Merged stored schemas into {merged_count} stream(s) for connection "
        f"{connection_data.connection_id}"
    )
    return replace(connection_data, catalog=catalog), merged_count


class SecretRetrievalError(Exception):
    """Raised when secret retrieval fails.

    This exception is raised when USE_CONNECTION_SECRET_RETRIEVER is enabled
    but secrets cannot be retrieved (e.g., EU data residency restrictions).
    """


def enrich_config_with_secrets(
    connection_data: ConnectionData,
    retrieval_reason: str = "MCP live tests",
    raise_on_failure: bool = True,
) -> ConnectionData:
    """Enrich connection data with unmasked secrets from internal retriever.

    This function takes a ConnectionData object (typically from the public
    Cloud API with masked secrets) and replaces the config with unmasked
    secrets from the internal connection-retriever.

    Args:
        connection_data: The connection data to enrich.
        retrieval_reason: Reason for retrieval (for audit logging).
        raise_on_failure: If True (default), raise SecretRetrievalError when
            secrets cannot be retrieved. If False, return the original
            connection_data with masked secrets (legacy behavior).

    Returns:
        A new ConnectionData with unmasked config.

    Raises:
        SecretRetrievalError: If raise_on_failure is True and secrets cannot
            be retrieved (e.g., due to EU data residency restrictions).
    """
    unmasked_config = retrieve_unmasked_config(
        connection_id=connection_data.connection_id,
        retrieval_reason=retrieval_reason,
    )

    if unmasked_config is None:
        error_msg = (
            "Could not retrieve unmasked secrets for connection "
            f"{connection_data.connection_id}. This may be due to EU data "
            "residency restrictions or database connectivity issues. "
            "The connection's credentials cannot be used for regression testing."
        )
        logger.warning(error_msg)
        if raise_on_failure:
            raise SecretRetrievalError(error_msg)
        return connection_data

    logger.info(
        f"Successfully enriched config with unmasked secrets for "
        f"{connection_data.connection_id}"
    )

    # Return a new ConnectionData with the unmasked config
    return replace(connection_data, config=unmasked_config)
