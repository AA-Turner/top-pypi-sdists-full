# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Cloud API client authentication root selection."""

from airbyte import constants

from airbyte_ops_mcp.cloud_admin import api_client


def test_auth_root_for_config_api_root_uses_public_cloud_api() -> None:
    assert (
        api_client._auth_root_for_config_api_root(constants.CLOUD_CONFIG_API_ROOT)
        == constants.CLOUD_API_ROOT
    )


def test_auth_root_for_config_api_root_uses_local_config_api() -> None:
    assert (
        api_client._auth_root_for_config_api_root("http://localhost:8000/api/v1")
        == "http://localhost:8000/api/v1"
    )
