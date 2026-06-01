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
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector
from google.cloud.sql.connector.enums import IPTypes

from airbyte_ops_mcp.constants import (
    CONNECTION_RETRIEVER_PG_CONNECTION_DETAILS_SECRET_ID,
    DEFAULT_CLOUD_SQL_PROXY_PORT,
)

PG_DRIVER = "pg8000"
PROXY_CHECK_TIMEOUT = 0.5  # seconds
DIRECT_CONNECTION_TIMEOUT = 5  # seconds - timeout for direct VPC/Tailscale connections


class CloudSqlProxyNotRunningError(Exception):
    """Raised when proxy mode is enabled but the Cloud SQL Proxy is not running."""

    pass


class VpnNotConnectedError(Exception):
    """Raised when direct connection mode requires VPN but it's not connected."""

    pass


def _is_tailscale_connected() -> bool:
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
                import json as json_module

                status = json_module.loads(result.stdout)
                # BackendState "Running" indicates connected
                return status.get("BackendState") == "Running"
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            pass

    return False


def _check_vpn_or_proxy_available() -> None:
    """Check if either VPN or proxy is available for database access.

    This function checks if the environment is properly configured for
    database access. It fails fast with a helpful error message if neither
    Tailscale VPN nor the Cloud SQL Proxy appears to be available.

    Raises:
        VpnNotConnectedError: If no VPN or proxy is detected
    """
    # If proxy mode is explicitly enabled, don't check VPN
    if os.getenv("CI") or os.getenv("USE_CLOUD_SQL_PROXY"):
        return

    # Check if Tailscale is connected
    if _is_tailscale_connected():
        return

    # Neither proxy mode nor Tailscale detected
    raise VpnNotConnectedError(
        "No VPN or proxy detected for database access.\n\n"
        "To connect to the Airbyte Cloud Prod DB Replica, you need either:\n\n"
        "1. Tailscale VPN connected (for direct VPC access)\n"
        "   - Install Tailscale: https://tailscale.com/download\n"
        "   - Connect to the Airbyte network\n\n"
        "2. Cloud SQL Proxy running locally\n"
        "   - Start the proxy:\n"
        "       airbyte-ops cloud db start-proxy\n"
        "       uvx --from=airbyte-internal-ops airbyte-ops cloud db start-proxy\n"
        "   - Set env vars: export USE_CLOUD_SQL_PROXY=1 DB_PORT=15432\n"
    )


def _check_proxy_is_running(host: str, port: int) -> None:
    """Check if the Cloud SQL Proxy is running and accepting connections.

    This performs a quick socket connection check to fail fast if the proxy
    is not running, rather than waiting for a long connection timeout.

    Args:
        host: The host to connect to (typically 127.0.0.1)
        port: The port to connect to

    Raises:
        CloudSqlProxyNotRunningError: If the proxy is not accepting connections
    """
    try:
        with socket.create_connection((host, port), timeout=PROXY_CHECK_TIMEOUT):
            pass  # Connection successful, proxy is running
    except (OSError, TimeoutError, ConnectionRefusedError) as e:
        raise CloudSqlProxyNotRunningError(
            f"Cloud SQL Proxy is not running on {host}:{port}. "
            f"Proxy mode is enabled (CI or USE_CLOUD_SQL_PROXY env var is set), "
            f"but nothing is listening on the expected port.\n\n"
            f"To start the proxy, run:\n"
            f"  airbyte-ops cloud db start-proxy --port {port}\n"
            f"  uvx --from=airbyte-internal-ops airbyte-ops cloud db start-proxy --port {port}\n\n"
            f"Or unset USE_CLOUD_SQL_PROXY to use direct VPC connection.\n\n"
            f"Original error: {e}"
        ) from e


# Lazy-initialized to avoid import-time GCP auth
_connector: Connector | None = None


def _get_connector() -> Connector:
    """Get the Cloud SQL connector, initializing lazily on first use."""
    global _connector
    if _connector is None:
        _connector = Connector()
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
    response = gsm_client.access_secret_version(name=f"{secret_id}/versions/latest")
    return response.payload.data.decode("UTF-8")


def get_database_creator(pg_connection_details: dict) -> Callable:
    """Create a database connection creator function."""

    def creator() -> Any:
        return _get_connector().connect(
            pg_connection_details["database_address"],
            PG_DRIVER,
            user=pg_connection_details["pg_user"],
            password=pg_connection_details["pg_password"],
            db=pg_connection_details["database_name"],
            ip_type=IPTypes.PRIVATE,
        )

    return creator


def get_pool(
    gsm_client: secretmanager.SecretManagerServiceClient,
) -> sqlalchemy.Engine:
    """Get a SQLAlchemy connection pool for the Airbyte Cloud database.

    This function supports two connection modes:
    1. Direct connection via Cloud SQL Python Connector (default, requires VPC/Tailscale)
    2. Connection via Cloud SQL Auth Proxy (when CI or USE_CLOUD_SQL_PROXY env var is set)

    For proxy mode, start the proxy with:
        airbyte-ops cloud db start-proxy

    Environment variables:
        CI: If set, uses proxy connection mode
        USE_CLOUD_SQL_PROXY: If set, uses proxy connection mode
        DB_PORT: Port for proxy connection (default: 15432)

    Raises:
        VpnNotConnectedError: If direct mode is used but no VPN/proxy is detected
        CloudSqlProxyNotRunningError: If proxy mode is enabled but the proxy is not running

    Args:
        gsm_client: GCP Secret Manager client for retrieving credentials

    Returns:
        SQLAlchemy Engine connected to the Prod DB Replica
    """
    # Fail fast if no VPN or proxy is available
    _check_vpn_or_proxy_available()

    pg_connection_details = json.loads(
        _get_secret_value(
            gsm_client, CONNECTION_RETRIEVER_PG_CONNECTION_DETAILS_SECRET_ID
        )
    )

    if os.getenv("CI") or os.getenv("USE_CLOUD_SQL_PROXY"):
        # Connect via Cloud SQL Auth Proxy, running on localhost
        # Port can be configured via DB_PORT env var (default: DEFAULT_CLOUD_SQL_PROXY_PORT)
        host = "127.0.0.1"
        port = int(os.getenv("DB_PORT", str(DEFAULT_CLOUD_SQL_PROXY_PORT)))

        # Fail fast if proxy is not running
        _check_proxy_is_running(host, port)

        return sqlalchemy.create_engine(
            f"postgresql+{PG_DRIVER}://{pg_connection_details['pg_user']}:{pg_connection_details['pg_password']}@{host}:{port}/{pg_connection_details['database_name']}",
        )

    # Default: Connect via Cloud SQL Python Connector (requires VPC/Tailscale access)
    # Use a timeout to fail faster if the connection can't be established
    return sqlalchemy.create_engine(
        f"postgresql+{PG_DRIVER}://",
        creator=get_database_creator(pg_connection_details),
        connect_args={"timeout": DIRECT_CONNECTION_TIMEOUT},
    )
