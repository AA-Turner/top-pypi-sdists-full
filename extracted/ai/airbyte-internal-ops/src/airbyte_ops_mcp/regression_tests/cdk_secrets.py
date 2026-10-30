# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Compatibility wrapper for integration-test secrets selected by `connector_secrets`."""

from __future__ import annotations

from airbyte_ops_mcp.connector_secrets import (
    DEFAULT_GCP_PROJECT_ID,
    ConnectorSecretConfig,
    ConnectorSecretsUnavailableError,
    find_usable_connector_config,
    get_gsm_secrets_client,
)


def get_integration_test_config_from_secrets(
    connector_name: str,
    project: str = DEFAULT_GCP_PROJECT_ID,
) -> ConnectorSecretConfig | None:
    """Return `None` when no usable secret exists.

    Raises `ConnectorSecretsUnavailableError` when GSM cannot be read.
    """
    try:
        client = get_gsm_secrets_client()
        return find_usable_connector_config(
            connector_name,
            project,
            client=client,
        )
    except ConnectorSecretsUnavailableError:
        raise
    except Exception as exc:
        raise ConnectorSecretsUnavailableError(
            connector_name=connector_name,
            gcp_project_id=project,
            error_types=[type(exc).__name__],
        ) from exc
