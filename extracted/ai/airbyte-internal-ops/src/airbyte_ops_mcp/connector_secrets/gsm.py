# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Google Secret Manager access for connector integration-test secrets.

Core, presentation-agnostic building blocks used by both the
`airbyte-ops secrets` CLI and any future MCP tools.

## Authentication

The helpers here obtain a `SecretManagerServiceClient` via `get_gsm_secrets_client()`,
which tries (in order):

1. `GCP_GSM_CREDENTIALS` — JSON-encoded service account key.
2. Application Default Credentials (e.g. `gcloud auth application-default login`).

## GSM conventions

Connector secrets in GSM must be labeled with `connector=<connector-name>`. An
optional `filename=<basename>` label controls the output filename in the local
`secrets/` directory; when absent, secrets land at `secrets/config.json`.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import cast

import google.auth.exceptions
from google.cloud import secretmanager_v1 as secretmanager
from google.cloud.secretmanager_v1 import Secret

from airbyte_ops_mcp.connector_secrets._gcp_urls import (
    extract_gcp_secret_name,
    get_gcp_secret_url,
)
from airbyte_ops_mcp.connector_secrets.exceptions import (
    ConnectorSecretWithNoValidVersionsError,
)

__all__ = [
    "CONNECTOR_LABEL",
    "DEFAULT_GCP_PROJECT_ID",
    "extract_gcp_secret_name",
    "fetch_secret_handles",
    "get_gcp_secret_url",
    "get_gsm_secrets_client",
    "get_secret_filepath",
    "get_secrets_dir",
    "write_secret_file",
]

logger = logging.getLogger(__name__)

DEFAULT_GCP_PROJECT_ID: str = (
    os.environ.get("GCP_PROJECT_ID", "") or "dataline-integration-testing"
)
"""Default GCP project for integration-test secrets.

`GCP_PROJECT_ID` overrides the default; empty strings are ignored so that a CI
runner which sets `GCP_PROJECT_ID=""` still falls back to the hard-coded default.
"""

CONNECTOR_LABEL = "connector"
"""GSM label used to associate a secret with a connector."""


def fetch_secret_handles(
    connector_name: str,
    gcp_project_id: str = DEFAULT_GCP_PROJECT_ID,
    *,
    client: secretmanager.SecretManagerServiceClient | None = None,
) -> list[Secret]:
    """List all GSM secret handles labeled `connector=<connector_name>`.

    Returns a list of GSM `Secret` metadata objects; no secret *values* are
    fetched. Use `write_secret_file` to materialize a secret's latest enabled
    version.

    Pass `client` to reuse an already-authenticated GSM client; otherwise a
    fresh one is obtained via `get_gsm_secrets_client()`.
    """
    if client is None:
        client = get_gsm_secrets_client()
    parent = f"projects/{gcp_project_id}"
    filter_string = f"labels.{CONNECTOR_LABEL}={connector_name}"
    secrets = client.list_secrets(
        request=secretmanager.ListSecretsRequest(
            parent=parent,
            filter=filter_string,
        )
    )
    return list(secrets)


def write_secret_file(
    secret: Secret,
    client: secretmanager.SecretManagerServiceClient,
    file_path: Path,
    connector_name: str,
    gcp_project_id: str,
) -> None:
    """Write the latest enabled version of `secret` to `file_path` (mode 0o600).

    Raises `ConnectorSecretWithNoValidVersionsError` if the secret has no
    enabled versions.
    """
    response = client.list_secret_versions(
        request={"parent": secret.name, "filter": "state:ENABLED"}
    )
    versions = list(response)
    if not versions:
        raise ConnectorSecretWithNoValidVersionsError(
            connector_name=connector_name,
            secret_name=extract_gcp_secret_name(secret.name),
            gcp_project_id=gcp_project_id,
        )
    enabled_version = versions[0]
    payload = client.access_secret_version(name=enabled_version.name)
    file_path.write_text(payload.payload.data.decode("UTF-8"))
    file_path.chmod(0o600)


def get_secrets_dir(
    connector_directory: Path,
    *,
    ensure_exists: bool = True,
) -> Path:
    """Return the `secrets/` directory for a connector.

    When `ensure_exists` is true, creates the directory (with a `*` `.gitignore`)
    if it does not already exist.
    """
    secrets_dir = connector_directory / "secrets"
    if ensure_exists:
        secrets_dir.mkdir(parents=True, exist_ok=True)
        gitignore_path = secrets_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("*")
    return secrets_dir


def get_secret_filepath(secrets_dir: Path, secret: Secret) -> Path:
    """Resolve the destination file for a secret based on its `filename` label.

    A secret labeled `filename=oauth_config` lands at
    `<secrets_dir>/oauth_config.json`. Secrets without the label default to
    `<secrets_dir>/config.json`.
    """
    if secret.labels and "filename" in secret.labels:
        return secrets_dir / f"{secret.labels['filename']}.json"
    return secrets_dir / "config.json"


def get_gsm_secrets_client() -> secretmanager.SecretManagerServiceClient:
    """Return an authenticated GSM client.

    Honors `GCP_GSM_CREDENTIALS` (service-account JSON) and otherwise falls
    back to Application Default Credentials. Raises `ValueError` when no
    credentials can be resolved.
    """
    credentials_json = os.environ.get("GCP_GSM_CREDENTIALS")
    if credentials_json:
        logger.info(
            "Using GCP service account credentials from GCP_GSM_CREDENTIALS env var."
        )
        return cast(
            "secretmanager.SecretManagerServiceClient",
            secretmanager.SecretManagerServiceClient.from_service_account_info(
                json.loads(credentials_json)
            ),
        )

    logger.info(
        "GCP_GSM_CREDENTIALS not set. Using Application Default Credentials (ADC)."
    )
    try:
        return secretmanager.SecretManagerServiceClient()
    except google.auth.exceptions.DefaultCredentialsError:
        raise ValueError(
            "No Google Cloud credentials found. Set `GCP_GSM_CREDENTIALS` with "
            "a service-account JSON key, or run "
            "`gcloud auth application-default login` to authenticate with a "
            "user account."
        ) from None
