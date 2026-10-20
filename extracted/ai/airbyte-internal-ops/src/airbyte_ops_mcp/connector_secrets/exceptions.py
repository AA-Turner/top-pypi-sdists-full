# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Exceptions for connector-secret operations."""

from __future__ import annotations

from dataclasses import dataclass

from airbyte_ops_mcp.connector_secrets._gcp_urls import get_gcp_secret_url


@dataclass(kw_only=True)
class InvalidConnectorSecretNameError(ValueError):
    """Raised when a new secret name does not follow the connector naming convention."""

    connector_name: str
    secret_name: str

    def __str__(self) -> str:
        """Describe the required secret-name pattern and provide an example."""
        prefix = f"SECRET_{self.connector_name.upper()}__"
        return (
            f"Invalid secret name '{self.secret_name}' for connector "
            f"'{self.connector_name}'. Expected pattern `{prefix}[A-Z0-9_]+`, "
            f"for example `{prefix}CREDS`."
        )


@dataclass(kw_only=True)
class InvalidConnectorSecretPayloadError(ValueError):
    """Raised when a secret payload is not a non-empty JSON object."""

    is_valid_json: bool

    def __str__(self) -> str:
        """Describe the payload requirement without rendering its contents."""
        if not self.is_valid_json:
            return "Secret payload is not valid JSON."
        return "Secret payload must be a non-empty JSON object."


@dataclass(kw_only=True)
class InvalidConnectorSecretFilenameError(ValueError):
    """Raised when a filename label is not a valid GSM label value."""

    filename: str

    def __str__(self) -> str:
        """Describe the allowed filename-label characters."""
        return (
            f"Invalid connector secret filename '{self.filename}'. Use 1-63 "
            "lowercase letters, digits, underscores, or hyphens."
        )


@dataclass(kw_only=True)
class ConnectorSecretNotFoundError(Exception):
    """Raised when a named connector secret does not exist in GSM."""

    connector_name: str
    secret_name: str
    gcp_project_id: str

    def __str__(self) -> str:
        """Describe the missing secret."""
        return (
            f"Secret '{self.secret_name}' was not found in project "
            f"'{self.gcp_project_id}' for connector '{self.connector_name}'."
        )


@dataclass(kw_only=True)
class ConnectorSecretConnectorMismatchError(Exception):
    """Raised when a secret's connector label does not match the requested connector."""

    connector_name: str
    secret_name: str
    actual_connector_label: str | None
    gcp_project_id: str

    def __str__(self) -> str:
        """Describe the label mismatch and link to the secret in the console."""
        url = get_gcp_secret_url(self.secret_name, self.gcp_project_id)
        return (
            f"Secret '{self.secret_name}' is labeled for connector "
            f"'{self.actual_connector_label}', not '{self.connector_name}'. "
            f"See {url}"
        )


@dataclass(kw_only=True)
class ConnectorSecretAlreadyExistsError(Exception):
    """Raised when creating a secret whose name already exists in GSM."""

    secret_name: str
    gcp_project_id: str

    def __str__(self) -> str:
        """Describe the existing secret and link to it in the console."""
        url = get_gcp_secret_url(self.secret_name, self.gcp_project_id)
        return f"Secret '{self.secret_name}' already exists. See {url}"


@dataclass(kw_only=True)
class ConnectorSecretFilenameConflictError(Exception):
    """Raised when a new secret would overwrite an existing connector config file."""

    existing_secret_name: str
    filename: str
    gcp_project_id: str

    def __str__(self) -> str:
        """Describe the filename conflict and link to the existing secret."""
        url = get_gcp_secret_url(self.existing_secret_name, self.gcp_project_id)
        return (
            f"Secret '{self.existing_secret_name}' already uses the "
            f"'{self.filename}.json' filename. Pass a different `--filename`. "
            f"See {url}"
        )


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


@dataclass(kw_only=True)
class ConnectorSecretVersionDisableError(Exception):
    """Raised when previously enabled versions could not all be disabled."""

    secret_name: str
    new_version_name: str
    failed_version_names: list[str]
    gcp_project_id: str

    def __str__(self) -> str:
        """Report the successful add and versions that still need disabling."""
        url = get_gcp_secret_url(self.secret_name, self.gcp_project_id)
        failed_versions = ", ".join(self.failed_version_names)
        return (
            f"New version '{self.new_version_name}' was added and is now the latest "
            f"version of secret '{self.secret_name}', but these previously enabled "
            f"versions still need disabling: {failed_versions}. See {url}"
        )
