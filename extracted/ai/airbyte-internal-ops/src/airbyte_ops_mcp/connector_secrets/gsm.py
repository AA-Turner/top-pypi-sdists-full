# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Google Secret Manager access for connector integration-test secrets.

Core, presentation-agnostic building blocks used by both the
`airbyte-ops secrets` CLI and any future MCP tools.

## Authentication

The helpers here obtain a `SecretManagerServiceClient` via `get_gsm_secrets_client()`,
which tries (in order):

1. `GCP_GSM_CREDENTIALS` — JSON-encoded service account key.
2. Application Default Credentials (e.g. `gcloud auth application-default login`).

Write operations use `get_gsm_writer_client()`, which reads the dedicated
`GCP_GSM_WRITER_CREDENTIALS` key or falls back to Application Default Credentials.

## GSM conventions

Connector secrets in GSM must be labeled with `connector=<connector-name>`. An
optional `filename=<basename>` label controls the output filename in the local
`secrets/` directory; when absent, secrets land at `secrets/config.json`.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import cast

import google.api_core.exceptions
import google.auth.exceptions
from google.cloud import secretmanager_v1 as secretmanager
from google.cloud.secretmanager_v1 import Secret

from airbyte_ops_mcp.connector_secrets._gcp_urls import (
    extract_gcp_secret_name,
    get_gcp_secret_url,
)
from airbyte_ops_mcp.connector_secrets.exceptions import (
    ConnectorSecretAlreadyExistsError,
    ConnectorSecretConnectorMismatchError,
    ConnectorSecretFilenameConflictError,
    ConnectorSecretNotFoundError,
    ConnectorSecretVersionDisableError,
    ConnectorSecretWithNoValidVersionsError,
    InvalidConnectorSecretFilenameError,
    InvalidConnectorSecretNameError,
    InvalidConnectorSecretPayloadError,
)

__all__ = [
    "CONNECTOR_LABEL",
    "DEFAULT_GCP_PROJECT_ID",
    "FILENAME_LABEL",
    "GSM_WRITER_CREDENTIALS_ENV_VAR",
    "create_secret",
    "extract_gcp_secret_name",
    "fetch_secret_handles",
    "get_connector_secret",
    "get_gcp_secret_url",
    "get_gsm_secrets_client",
    "get_gsm_writer_client",
    "get_secret_filepath",
    "get_secrets_dir",
    "update_secret",
    "validate_new_secret_name",
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

FILENAME_LABEL = "filename"
"""GSM label used to select a connector secret's local filename."""

GSM_WRITER_CREDENTIALS_ENV_VAR = "GCP_GSM_WRITER_CREDENTIALS"
"""Environment variable containing the dedicated GSM writer service account key."""


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
    if secret.labels and FILENAME_LABEL in secret.labels:
        return secrets_dir / f"{secret.labels[FILENAME_LABEL]}.json"
    return secrets_dir / "config.json"


def validate_new_secret_name(connector_name: str, secret_name: str) -> None:
    """Validate that a new secret name follows the connector naming convention."""
    pattern = rf"SECRET_{re.escape(connector_name.upper())}__[A-Z0-9_]+"
    if not re.fullmatch(pattern, secret_name):
        raise InvalidConnectorSecretNameError(
            connector_name=connector_name,
            secret_name=secret_name,
        )


def _reject_json_constant(_: str) -> None:
    raise ValueError


def _validate_secret_payload(value: str) -> None:
    """Require a non-empty JSON object without exposing the payload on failure."""
    try:
        parsed_value = json.loads(value, parse_constant=_reject_json_constant)
    except (ValueError, RecursionError):
        raise InvalidConnectorSecretPayloadError(is_valid_json=False) from None
    if not isinstance(parsed_value, dict) or not parsed_value:
        raise InvalidConnectorSecretPayloadError(is_valid_json=True)


def _validate_secret_filename(filename: str) -> None:
    """Require a filename label compatible with Google Secret Manager labels."""
    if not re.fullmatch(r"[a-z0-9_-]{1,63}", filename):
        raise InvalidConnectorSecretFilenameError(filename=filename)


def get_connector_secret(
    connector_name: str,
    secret_name: str,
    *,
    gcp_project_id: str = DEFAULT_GCP_PROJECT_ID,
    client: secretmanager.SecretManagerServiceClient,
) -> Secret:
    """Get a secret after verifying that its connector label matches."""
    try:
        secret = client.get_secret(
            name=f"projects/{gcp_project_id}/secrets/{secret_name}"
        )
    except google.api_core.exceptions.NotFound:
        raise ConnectorSecretNotFoundError(
            connector_name=connector_name,
            secret_name=secret_name,
            gcp_project_id=gcp_project_id,
        ) from None

    actual_connector_label = secret.labels.get(CONNECTOR_LABEL)
    if actual_connector_label != connector_name:
        raise ConnectorSecretConnectorMismatchError(
            connector_name=connector_name,
            secret_name=secret_name,
            actual_connector_label=actual_connector_label,
            gcp_project_id=gcp_project_id,
        )
    return secret


def create_secret(
    connector_name: str,
    value: str,
    *,
    secret_name: str,
    filename: str | None = None,
    gcp_project_id: str = DEFAULT_GCP_PROJECT_ID,
    client: secretmanager.SecretManagerServiceClient,
) -> str:
    """Create a connector secret and its initial version in GSM."""
    validate_new_secret_name(connector_name, secret_name)
    _validate_secret_payload(value)
    if filename is not None:
        _validate_secret_filename(filename)

    target_filename = filename or "config"
    for existing_secret in fetch_secret_handles(
        connector_name=connector_name,
        gcp_project_id=gcp_project_id,
        client=client,
    ):
        existing_filename = existing_secret.labels.get(FILENAME_LABEL, "config")
        if existing_filename == target_filename:
            raise ConnectorSecretFilenameConflictError(
                existing_secret_name=extract_gcp_secret_name(existing_secret.name),
                filename=target_filename,
                gcp_project_id=gcp_project_id,
            )

    labels = {CONNECTOR_LABEL: connector_name}
    if filename is not None:
        labels[FILENAME_LABEL] = filename

    try:
        secret = client.create_secret(
            request={
                "parent": f"projects/{gcp_project_id}",
                "secret_id": secret_name,
                "secret": {
                    "replication": {"automatic": {}},
                    "labels": labels,
                },
            }
        )
    except google.api_core.exceptions.AlreadyExists:
        raise ConnectorSecretAlreadyExistsError(
            secret_name=secret_name,
            gcp_project_id=gcp_project_id,
        ) from None

    version = client.add_secret_version(
        request={
            "parent": secret.name,
            "payload": {"data": value.encode("utf-8")},
        }
    )
    return version.name


def update_secret(
    connector_name: str,
    value: str,
    *,
    secret_name: str,
    gcp_project_id: str = DEFAULT_GCP_PROJECT_ID,
    client: secretmanager.SecretManagerServiceClient,
) -> str:
    """Add a version, then disable versions that were previously enabled.

    If disabling any previous version fails, the new version remains added and
    latest, and the exception lists versions that still need disabling.
    """
    _validate_secret_payload(value)
    secret = get_connector_secret(
        connector_name=connector_name,
        secret_name=secret_name,
        gcp_project_id=gcp_project_id,
        client=client,
    )
    enabled_versions = list(
        client.list_secret_versions(
            request={"parent": secret.name, "filter": "state:ENABLED"}
        )
    )
    version = client.add_secret_version(
        request={
            "parent": secret.name,
            "payload": {"data": value.encode("utf-8")},
        }
    )

    failed_version_names: list[str] = []
    for enabled_version in enabled_versions:
        if enabled_version.name == version.name:
            continue
        try:
            client.disable_secret_version(request={"name": enabled_version.name})
        except (
            google.api_core.exceptions.GoogleAPICallError,
            google.api_core.exceptions.RetryError,
        ):
            failed_version_names.append(enabled_version.name)

    if failed_version_names:
        raise ConnectorSecretVersionDisableError(
            secret_name=extract_gcp_secret_name(secret.name),
            new_version_name=version.name,
            failed_version_names=failed_version_names,
            gcp_project_id=gcp_project_id,
        ) from None

    return version.name


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


def get_gsm_writer_client() -> secretmanager.SecretManagerServiceClient:
    """Return a GSM client using the dedicated writer credential or ADC.

    Honors `GCP_GSM_WRITER_CREDENTIALS` (service-account JSON) and otherwise
    falls back to Application Default Credentials. Raises `ValueError` when no
    credentials can be resolved.
    """
    credentials_json = os.environ.get(GSM_WRITER_CREDENTIALS_ENV_VAR)
    if credentials_json:
        logger.info(
            "Using GCP service account credentials from "
            f"{GSM_WRITER_CREDENTIALS_ENV_VAR} env var."
        )
        return cast(
            "secretmanager.SecretManagerServiceClient",
            secretmanager.SecretManagerServiceClient.from_service_account_info(
                json.loads(credentials_json)
            ),
        )

    logger.info(
        f"{GSM_WRITER_CREDENTIALS_ENV_VAR} not set. "
        "Using Application Default Credentials (ADC)."
    )
    try:
        return secretmanager.SecretManagerServiceClient()
    except google.auth.exceptions.DefaultCredentialsError:
        raise ValueError(
            "No Google Cloud credentials found. Set "
            "`GCP_GSM_WRITER_CREDENTIALS` (agents: request it via the "
            "`request_devin_secret` tool with alias `GCP_GSM_WRITER_CREDENTIALS`), "
            "or run `gcloud auth application-default login` with an account "
            "that can write secrets."
        ) from None
