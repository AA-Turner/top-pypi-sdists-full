# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for prod DB access connection behavior."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from google.api_core import exceptions as google_api_exceptions
from google.cloud.sql.connector.enums import IPTypes

from airbyte_ops_mcp.constants import ENV_K_SERVICE
from airbyte_ops_mcp.prod_db_access.db_engine import (
    PG_DRIVER,
    CloudRunProdDbAccessNotConfiguredError,
    ProdDbCloudSqlIamError,
    ProdDbSecretAccessError,
    _cloud_sql_connector_ip_type,
    _get_secret_value,
    get_database_creator,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "env",
    [
        pytest.param({}, id="local"),
        pytest.param({ENV_K_SERVICE: "ops-webapp"}, id="cloud_run"),
    ],
)
def test_cloud_sql_connector_ip_type(
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str],
) -> None:
    """Validate direct Cloud SQL Connector IP type by runtime."""
    monkeypatch.delenv(ENV_K_SERVICE, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    assert _cloud_sql_connector_ip_type() == IPTypes.PUBLIC


@pytest.mark.unit
def test_get_database_creator_uses_public_ip_connector(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate direct connections use the public IP connector path."""
    connection = object()
    connector = Mock()
    connector.connect.return_value = connection
    monkeypatch.setattr(
        "airbyte_ops_mcp.prod_db_access.db_engine._get_connector",
        lambda: connector,
    )

    creator = get_database_creator(
        {
            "database_address": "prod-ab-cloud-proj:us-west3:prod-pgsql-replica",
            "pg_user": "user",
            "pg_password": "password",
            "database_name": "prod-configapi",
        }
    )

    assert creator() is connection
    connector.connect.assert_called_once_with(
        "prod-ab-cloud-proj:us-west3:prod-pgsql-replica",
        PG_DRIVER,
        user="user",
        password="password",
        db="prod-configapi",
        ip_type=IPTypes.PUBLIC,
    )


@pytest.mark.unit
def test_get_secret_value_wraps_secret_manager_permission_denied() -> None:
    """Convert known Secret Manager IAM failure into an actionable error."""
    gsm_client = Mock()
    gsm_client.access_secret_version.side_effect = (
        google_api_exceptions.PermissionDenied("denied")
    )

    with pytest.raises(ProdDbSecretAccessError, match="Secret Manager"):
        _get_secret_value(gsm_client, "projects/123/secrets/db")


@pytest.mark.unit
def test_get_database_creator_wraps_cloud_sql_permission_denied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Convert known Cloud SQL IAM failure into an actionable error."""
    connector = Mock()
    connector.connect.side_effect = google_api_exceptions.PermissionDenied("denied")
    monkeypatch.setattr(
        "airbyte_ops_mcp.prod_db_access.db_engine._get_connector",
        lambda: connector,
    )

    creator = get_database_creator(
        {
            "database_address": "prod-ab-cloud-proj:us-west3:prod-pgsql-replica",
            "pg_user": "user",
            "pg_password": "password",
            "database_name": "prod-configapi",
        }
    )

    with pytest.raises(ProdDbCloudSqlIamError, match="Cloud SQL"):
        creator()


@pytest.mark.unit
def test_get_database_creator_wraps_cloud_run_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Convert Cloud Run connection timeout into an actionable error."""
    connector = Mock()
    connector.connect.side_effect = TimeoutError("timed out")
    monkeypatch.setenv(ENV_K_SERVICE, "ops-webapp")
    monkeypatch.setattr(
        "airbyte_ops_mcp.prod_db_access.db_engine._get_connector",
        lambda: connector,
    )

    creator = get_database_creator(
        {
            "database_address": "prod-ab-cloud-proj:us-west3:prod-pgsql-replica",
            "pg_user": "user",
            "pg_password": "password",
            "database_name": "prod-configapi",
        }
    )

    with pytest.raises(CloudRunProdDbAccessNotConfiguredError, match="public IP"):
        creator()
