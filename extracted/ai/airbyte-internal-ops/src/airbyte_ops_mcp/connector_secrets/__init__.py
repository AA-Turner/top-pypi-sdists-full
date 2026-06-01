# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Connector integration-test secrets stored in Google Secret Manager (GSM).

This package owns the logic for listing, fetching, and CI-masking connector
integration-test secrets. The CLI entrypoints (`airbyte-ops secrets ...`) are
thin wrappers that call into this package.

See [`airbyte_ops_mcp.cli.secrets`](../cli/secrets.py) for the CLI layer.
"""

from __future__ import annotations

from airbyte_ops_mcp.connector_secrets.exceptions import (
    ConnectorSecretWithNoValidVersionsError,
)
from airbyte_ops_mcp.connector_secrets.gsm import (
    CONNECTOR_LABEL,
    DEFAULT_GCP_PROJECT_ID,
    extract_gcp_secret_name,
    fetch_secret_handles,
    get_gcp_secret_url,
    get_gsm_secrets_client,
    get_secret_filepath,
    get_secrets_dir,
    write_secret_file,
)

__all__ = [
    "CONNECTOR_LABEL",
    "DEFAULT_GCP_PROJECT_ID",
    "ConnectorSecretWithNoValidVersionsError",
    "extract_gcp_secret_name",
    "fetch_secret_handles",
    "get_gcp_secret_url",
    "get_gsm_secrets_client",
    "get_secret_filepath",
    "get_secrets_dir",
    "write_secret_file",
]
