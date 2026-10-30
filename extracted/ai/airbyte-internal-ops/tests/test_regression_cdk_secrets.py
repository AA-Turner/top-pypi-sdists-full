# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the `connector_secrets` wrapper used by regression tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from airbyte_ops_mcp.connector_secrets import (
    DEFAULT_GCP_PROJECT_ID,
    ConnectorSecretConfig,
    ConnectorSecretsUnavailableError,
)
from airbyte_ops_mcp.regression_tests import cdk_secrets

pytestmark = pytest.mark.unit


def test_returns_none_when_client_initialization_fails(monkeypatch) -> None:
    monkeypatch.setattr(
        cdk_secrets,
        "get_gsm_secrets_client",
        MagicMock(side_effect=ValueError("sensitive initialization detail")),
    )

    with pytest.raises(ConnectorSecretsUnavailableError) as excinfo:
        cdk_secrets.get_integration_test_config_from_secrets(
            "source-test", project="test-project"
        )

    assert excinfo.value.error_types == ["ValueError"]
    assert isinstance(excinfo.value.__cause__, ValueError)
    assert "Could not read GSM" in str(excinfo.value)
    assert "sensitive initialization detail" not in str(excinfo.value)


def test_raises_when_secret_listing_fails(monkeypatch) -> None:
    client = MagicMock()
    find_config = MagicMock(side_effect=RuntimeError("sensitive listing detail"))
    monkeypatch.setattr(cdk_secrets, "get_gsm_secrets_client", lambda: client)
    monkeypatch.setattr(cdk_secrets, "find_usable_connector_config", find_config)

    with pytest.raises(ConnectorSecretsUnavailableError) as excinfo:
        cdk_secrets.get_integration_test_config_from_secrets(
            "source-test", project="test-project"
        )

    assert excinfo.value.error_types == ["RuntimeError"]
    assert isinstance(excinfo.value.__cause__, RuntimeError)
    assert "sensitive listing detail" not in str(excinfo.value)


def test_delegates_to_shared_selector(monkeypatch) -> None:
    client = MagicMock()
    config = ConnectorSecretConfig(
        secret_name="SECRET_SOURCE-TEST__CREDS",
        config={"token": "usable"},
    )
    find_config = MagicMock(return_value=config)
    monkeypatch.setattr(cdk_secrets, "get_gsm_secrets_client", lambda: client)
    monkeypatch.setattr(cdk_secrets, "find_usable_connector_config", find_config)

    result = cdk_secrets.get_integration_test_config_from_secrets(
        "source-test", project="custom-project"
    )

    assert result is config
    find_config.assert_called_once_with(
        "source-test",
        "custom-project",
        client=client,
    )


def test_defaults_to_the_shared_gcp_project(monkeypatch) -> None:
    client = MagicMock()
    find_config = MagicMock(return_value=None)
    monkeypatch.setattr(cdk_secrets, "get_gsm_secrets_client", lambda: client)
    monkeypatch.setattr(cdk_secrets, "find_usable_connector_config", find_config)

    assert cdk_secrets.get_integration_test_config_from_secrets("source-test") is None
    find_config.assert_called_once_with(
        "source-test",
        DEFAULT_GCP_PROJECT_ID,
        client=client,
    )


def test_passes_through_finder_availability_error_unchanged(monkeypatch) -> None:
    client = MagicMock()
    unavailable = ConnectorSecretsUnavailableError(
        connector_name="source-test",
        gcp_project_id="test-project",
        error_types=["PermissionDenied"],
    )
    monkeypatch.setattr(cdk_secrets, "get_gsm_secrets_client", lambda: client)
    monkeypatch.setattr(
        cdk_secrets,
        "find_usable_connector_config",
        MagicMock(side_effect=unavailable),
    )

    with pytest.raises(ConnectorSecretsUnavailableError) as excinfo:
        cdk_secrets.get_integration_test_config_from_secrets(
            "source-test", project="test-project"
        )

    assert excinfo.value is unavailable
