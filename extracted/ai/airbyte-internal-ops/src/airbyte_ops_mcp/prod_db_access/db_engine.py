# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Database engine and connection management for Airbyte Cloud Prod DB Replica.

This module provides connection pooling and engine management for querying
the Airbyte Cloud production database replica.

For SQL query templates and schema documentation, see sql.py.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
from typing import Any, Callable

import sqlalchemy
from google.api_core import exceptions as google_api_exceptions
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector
from google.cloud.sql.connector.enums import IPTypes

from airbyte_ops_mcp.constants import (
    CONNECTION_RETRIEVER_PG_CONNECTION_DETAILS_SECRET_ID,
    ENV_K_SERVICE,
)
from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_prod_db_replica

PG_DRIVER = "pg8000"
DIRECT_CONNECTION_TIMEOUT = 5  # seconds


class CloudRunProdDbAccessNotConfiguredError(Exception):
    """Raised when Cloud Run is missing prod DB access infrastructure."""

    pass


class ProdDbSecretAccessError(Exception):
    """Raised when credentials cannot read prod DB connection details."""

    pass


class ProdDbCloudSqlIamError(Exception):
    """Raised when credentials cannot authorize against the Cloud SQL instance."""

    pass


def is_tailscale_connected() -> bool:
    """Check if Tailscale VPN is likely connected.

    This is a best-effort check that works on Linux and macOS.
    Returns True if Tailscale appears to be connected, False otherwise.

    Detection methods:
    1. Check for tailscale0 network interface (Linux)
    2. Run 'tailscale status --json' and check backend state (cross-platform)
    3. Check macOS-specific Tailscale.app location if tailscale not in PATH
    """
    # Method 1: Check for tailscale0 interface (Linux)
    try:
        interfaces = [name for _, name in socket.if_nameindex()]
        if "tailscale0" in interfaces:
            return True
    except (OSError, AttributeError):
        pass  # if_nameindex not available on this platform

    # Method 2: Check tailscale CLI status
    tailscale_path = shutil.which("tailscale")

    # Method 3: On macOS, check the standard Tailscale.app location if not in PATH
    if not tailscale_path and os.path.exists(
        "/Applications/Tailscale.app/Contents/MacOS/Tailscale"
    ):
        tailscale_path = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"

    if tailscale_path:
        try:
            result = subprocess.run(
                [tailscale_path, "status", "--json"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode == 0:
                status = json.loads(result.stdout)
                # BackendState "Running" indicates connected
                return status.get("BackendState") == "Running"
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            pass

    return False


def _is_cloud_run() -> bool:
    """Return whether the process is running in Cloud Run."""
    return bool(os.getenv(ENV_K_SERVICE))


def _cloud_sql_connector_ip_type() -> IPTypes:
    """Return the Cloud SQL Connector IP type for direct connections."""
    return IPTypes.PUBLIC


# Lazy-initialized to avoid import-time GCP auth
_connector: Connector | None = None


def _get_connector() -> Connector:
    """Get the Cloud SQL connector, initializing lazily on first use."""
    global _connector
    if _connector is None:
        _connector = Connector(credentials=get_gcp_credentials_for_prod_db_replica())
    return _connector


def _get_secret_value(
    gsm_client: secretmanager.SecretManagerServiceClient,
    secret_id: str,
) -> str:
    """Get the value of the latest version of a secret.

    Args:
        gsm_client: GCP Secret Manager client
        secret_id: The full resource ID of the secret
            (e.g., "projects/123/secrets/my-secret")

    Returns:
        The value of the latest version of the secret
    """
    try:
        response = gsm_client.access_secret_version(name=f"{secret_id}/versions/latest")
    except google_api_exceptions.PermissionDenied as e:
        raise ProdDbSecretAccessError(
            "Unable to read prod DB connection details from Secret Manager. "
            "Grant the runtime identity roles/secretmanager.secretAccessor on "
            f"{secret_id}."
        ) from e
    return response.payload.data.decode("UTF-8")


def get_database_creator(pg_connection_details: dict) -> Callable:
    """Create a database connection creator function."""

    def creator() -> Any:
        try:
            return _get_connector().connect(
                pg_connection_details["database_address"],
                PG_DRIVER,
                user=pg_connection_details["pg_user"],
                password=pg_connection_details["pg_password"],
                db=pg_connection_details["database_name"],
                ip_type=_cloud_sql_connector_ip_type(),
            )
        except google_api_exceptions.PermissionDenied as e:
            raise ProdDbCloudSqlIamError(
                "Unable to authorize Cloud SQL access for the prod DB replica. "
                "Grant the runtime identity roles/cloudsql.client on prod-ab-cloud-proj."
            ) from e
        except (OSError, TimeoutError) as e:
            if _is_cloud_run():
                raise CloudRunProdDbAccessNotConfiguredError(
                    "Cloud Run could not reach the prod DB replica public IP. "
                    "Verify Cloud SQL public IP access and egress are available."
                ) from e
            raise

    return creator


# Lazy-initialized engine singleton — reused across queries so pool settings
# (pool_size, max_overflow, etc.) actually take effect.
_engine: sqlalchemy.Engine | None = None


def get_pool(
    gsm_client: secretmanager.SecretManagerServiceClient,
) -> sqlalchemy.Engine:
    """Get a SQLAlchemy connection pool for the Airbyte Cloud database.

    The engine is created once and cached for the lifetime of the process so
    that connection pooling works as intended. Subsequent calls return the
    same engine instance.

    This function connects with the Cloud SQL Python Connector in public IP mode.

    Args:
        gsm_client: GCP Secret Manager client for retrieving credentials

    Returns:
        SQLAlchemy Engine connected to the Prod DB Replica
    """
    global _engine
    if _engine is not None:
        return _engine

    pg_connection_details = json.loads(
        _get_secret_value(
            gsm_client, CONNECTION_RETRIEVER_PG_CONNECTION_DETAILS_SECRET_ID
        )
    )

    _engine = sqlalchemy.create_engine(
        f"postgresql+{PG_DRIVER}://",
        creator=get_database_creator(pg_connection_details),
        connect_args={"timeout": DIRECT_CONNECTION_TIMEOUT},
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return _engine
