# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GCP credential resolution."""

from __future__ import annotations

import json
from collections.abc import Iterator
from unittest.mock import Mock

import pytest

from airbyte_ops_mcp import gcp_auth
from airbyte_ops_mcp.constants import (
    ENV_GCP_BIGQUERY_CREDENTIALS,
    ENV_GCP_PROD_DB_ACCESS_CREDENTIALS,
)


@pytest.fixture(autouse=True)
def clear_credential_cache() -> Iterator[None]:
    """Keep credential resolution isolated between tests."""
    with gcp_auth._sa_credentials_lock:
        gcp_auth._cached_sa_credentials.clear()
    yield
    with gcp_auth._sa_credentials_lock:
        gcp_auth._cached_sa_credentials.clear()


def test_bigquery_credentials_prefer_bigquery_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bigquery_info = {"type": "service_account", "client_email": "bigquery@example.com"}
    prod_db_info = {"type": "service_account", "client_email": "prod-db@example.com"}
    expected_credentials = object()
    parse_credentials = Mock(return_value=expected_credentials)
    monkeypatch.setattr(
        gcp_auth.service_account.Credentials,
        "from_service_account_info",
        parse_credentials,
    )
    monkeypatch.setattr(
        gcp_auth.google.auth,
        "default",
        Mock(side_effect=AssertionError("ADC should not be used")),
    )
    monkeypatch.setenv(ENV_GCP_BIGQUERY_CREDENTIALS, json.dumps(bigquery_info))
    monkeypatch.setenv(ENV_GCP_PROD_DB_ACCESS_CREDENTIALS, json.dumps(prod_db_info))

    credentials = gcp_auth.get_gcp_credentials_for_bigquery()

    assert credentials is expected_credentials
    parse_credentials.assert_called_once_with(
        bigquery_info,
        scopes=gcp_auth.DEFAULT_GCP_SCOPES,
    )


def test_bigquery_credentials_ignore_prod_db_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prod_db_info = {"type": "service_account", "client_email": "prod-db@example.com"}
    expected_bigquery_credentials = object()
    expected_prod_db_credentials = object()
    parse_credentials = Mock(return_value=expected_prod_db_credentials)
    load_adc = Mock(return_value=(expected_bigquery_credentials, "project"))
    monkeypatch.setattr(
        gcp_auth.service_account.Credentials,
        "from_service_account_info",
        parse_credentials,
    )
    monkeypatch.setattr(gcp_auth.google.auth, "default", load_adc)
    monkeypatch.delenv(ENV_GCP_BIGQUERY_CREDENTIALS, raising=False)
    monkeypatch.setenv(ENV_GCP_PROD_DB_ACCESS_CREDENTIALS, json.dumps(prod_db_info))

    credentials = gcp_auth.get_gcp_credentials_for_bigquery()

    assert credentials is expected_bigquery_credentials
    parse_credentials.assert_not_called()
    load_adc.assert_called_once_with(scopes=gcp_auth.DEFAULT_GCP_SCOPES)

    prod_db_credentials = gcp_auth.get_gcp_credentials_for_prod_db_replica()

    assert prod_db_credentials is expected_prod_db_credentials
    parse_credentials.assert_called_once_with(
        prod_db_info,
        scopes=gcp_auth.DEFAULT_GCP_SCOPES,
    )


def test_invalid_bigquery_env_var_does_not_fall_back_to_adc(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    load_adc = Mock(side_effect=AssertionError("ADC should not be used"))
    monkeypatch.setattr(gcp_auth.google.auth, "default", load_adc)
    monkeypatch.setenv(ENV_GCP_BIGQUERY_CREDENTIALS, "{invalid-json")

    with pytest.raises(json.JSONDecodeError):
        gcp_auth.get_gcp_credentials_for_bigquery()

    load_adc.assert_not_called()


def test_external_account_credentials_use_google_auth_loader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    external_account_info = {
        "type": "external_account",
        "audience": "//iam.googleapis.com/projects/123/locations/global/workloadIdentityPools/pool/providers/provider",
    }
    expected_credentials = object()
    load_credentials = Mock(return_value=(expected_credentials, "project"))
    monkeypatch.setattr(
        gcp_auth.google.auth, "load_credentials_from_dict", load_credentials
    )
    monkeypatch.setattr(
        gcp_auth.service_account.Credentials,
        "from_service_account_info",
        Mock(side_effect=AssertionError("Service account parser should not be used")),
    )
    monkeypatch.setenv(
        ENV_GCP_BIGQUERY_CREDENTIALS,
        json.dumps(external_account_info),
    )

    credentials = gcp_auth.get_gcp_credentials_for_bigquery()

    assert credentials is expected_credentials
    load_credentials.assert_called_once_with(
        external_account_info,
        scopes=gcp_auth.DEFAULT_GCP_SCOPES,
    )


def test_prod_db_credentials_ignore_bigquery_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bigquery_info = {"type": "service_account", "client_email": "bigquery@example.com"}
    expected_credentials = object()
    load_adc = Mock(return_value=(expected_credentials, "project"))
    monkeypatch.setattr(gcp_auth.google.auth, "default", load_adc)
    monkeypatch.setattr(
        gcp_auth.service_account.Credentials,
        "from_service_account_info",
        Mock(side_effect=AssertionError("BigQuery credentials should be ignored")),
    )
    monkeypatch.setenv(ENV_GCP_BIGQUERY_CREDENTIALS, json.dumps(bigquery_info))
    monkeypatch.delenv(ENV_GCP_PROD_DB_ACCESS_CREDENTIALS, raising=False)

    credentials = gcp_auth.get_gcp_credentials_for_prod_db_replica()

    assert credentials is expected_credentials
    load_adc.assert_called_once_with(scopes=gcp_auth.DEFAULT_GCP_SCOPES)
