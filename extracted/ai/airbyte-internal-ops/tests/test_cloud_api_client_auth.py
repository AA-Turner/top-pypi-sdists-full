# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for Cloud API client authentication root selection."""

import pytest
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from requests import Response

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


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (
            403,
            "Authenticated principal lacks Config API administrator permissions",
        ),
        (401, "Config API authentication failed"),
    ],
)
def test_config_api_error_distinguishes_authentication_from_authorization(
    status_code: int,
    expected: str,
) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"message":"Forbidden"}'

    with pytest.raises(PyAirbyteInputError, match=expected):
        api_client._raise_config_api_error(
            response,
            operation="get scoped configuration context",
            endpoint="https://cloud.airbyte.com/api/v1/scoped_configuration/get_context",
        )


def test_config_api_error_preserves_extra_context() -> None:
    response = Response()
    response.status_code = 500
    response._content = b'{"message":"Internal Server Error"}'

    with pytest.raises(PyAirbyteInputError) as error:
        api_client._raise_config_api_error(
            response,
            operation="resolve connector version",
            endpoint="https://cloud.airbyte.com/api/v1/actor_definition_versions/resolve",
            extra_context={"payload": {"actorType": "source"}},
        )

    assert error.value.context["payload"] == {"actorType": "source"}


def test_connector_rollout_403_uses_config_api_error_mapping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Response()
    response.status_code = 403
    response._content = b'{"message":"Forbidden"}'
    monkeypatch.setattr(api_client, "_get_access_token", lambda **_: "token")
    monkeypatch.setattr(api_client.requests, "post", lambda *_, **__: response)

    with pytest.raises(
        PyAirbyteInputError,
        match="Authenticated principal lacks Config API administrator permissions",
    ) as error:
        api_client.start_connector_rollout(
            docker_repository="airbyte/source-test",
            docker_image_tag="1.0.0",
            actor_definition_id="definition-id",
            updated_by="user-id",
            rollout_strategy="manual",
            config_api_root="https://cloud.airbyte.com/api/v1",
            bearer_token="token",
        )

    assert error.value.context["payload"]["docker_repository"] == "airbyte/source-test"
