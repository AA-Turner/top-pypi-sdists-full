# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the DockerHub API client."""

from unittest.mock import Mock, patch

import pytest
import requests

from airbyte_ops_mcp.docker_hub import (
    DockerHubAnonymousPaginationLimitError,
    get_docker_hub_tags_and_digests,
)


def _response(*, ok: bool, status_code: int = 200, payload: dict | None = None):
    response = Mock(ok=ok, status_code=status_code)
    response.json.return_value = payload or {}
    if not ok:
        response.raise_for_status.side_effect = requests.HTTPError(
            f"{status_code} Client Error"
        )
    return response


@pytest.mark.unit
@patch("airbyte_ops_mcp.docker_hub.time.sleep")
@patch("airbyte_ops_mcp.docker_hub.get_docker_hub_headers", return_value={})
@patch("airbyte_ops_mcp.docker_hub.requests.get")
def test_anonymous_offset_cap_raises(mock_get, mock_headers, mock_sleep):
    mock_get.side_effect = [
        _response(
            ok=True,
            payload={
                "results": [{"name": "1.0.0", "digest": "a"}],
                "next": ".../tags?page=2&page_size=100",
            },
        ),
        _response(
            ok=False,
            status_code=403,
            payload={
                "message": "pagination offset too large for anonymous requests; "
                "sign in to page further",
                "errinfo": {},
            },
        ),
    ]

    with pytest.raises(
        DockerHubAnonymousPaginationLimitError, match="DOCKER_HUB_USERNAME"
    ):
        get_docker_hub_tags_and_digests(
            "airbyte/source-declarative-manifest", retries=2
        )

    assert mock_get.call_count == 2
    assert mock_sleep.call_count == 0
    assert mock_get.call_args_list[0].args[0].endswith("tags?page_size=100")


@pytest.mark.unit
@patch("airbyte_ops_mcp.docker_hub.time.sleep")
@patch("airbyte_ops_mcp.docker_hub.get_docker_hub_headers", return_value={})
@patch("airbyte_ops_mcp.docker_hub.requests.get")
def test_non_cap_403_is_retried_then_raised(mock_get, mock_headers, mock_sleep):
    first_page = _response(
        ok=True,
        payload={
            "results": [{"name": "1.0.0", "digest": "a"}],
            "next": ".../tags?page=2&page_size=100",
        },
    )
    forbidden_responses = [
        _response(ok=False, status_code=403, payload={"message": "forbidden"}),
        _response(ok=False, status_code=403, payload={"message": "forbidden"}),
    ]
    mock_get.side_effect = [first_page, *forbidden_responses]

    with pytest.raises(requests.HTTPError, match="403"):
        get_docker_hub_tags_and_digests(
            "airbyte/source-declarative-manifest", retries=1
        )

    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 2


@pytest.mark.unit
@patch("airbyte_ops_mcp.docker_hub.time.sleep")
@patch("airbyte_ops_mcp.docker_hub.get_docker_hub_headers", return_value={})
@patch("airbyte_ops_mcp.docker_hub.requests.get")
def test_non_cap_403_retry_succeeds(mock_get, mock_headers, mock_sleep):
    mock_get.side_effect = [
        _response(
            ok=True,
            payload={
                "results": [{"name": "1.0.0", "digest": "a"}],
                "next": ".../tags?page=2&page_size=100",
            },
        ),
        _response(ok=False, status_code=403, payload={"message": "forbidden"}),
        _response(
            ok=True,
            payload={"results": [{"name": "0.9.0", "digest": "b"}], "next": None},
        ),
    ]

    result = get_docker_hub_tags_and_digests(
        "airbyte/source-declarative-manifest", retries=1
    )

    assert result == {"1.0.0": "a", "0.9.0": "b"}
    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 1


@pytest.mark.unit
@patch("airbyte_ops_mcp.docker_hub.get_docker_hub_headers", return_value={})
@patch("airbyte_ops_mcp.docker_hub.requests.get")
def test_merges_paginated_tag_results(mock_get, mock_headers):
    mock_get.side_effect = [
        _response(
            ok=True,
            payload={
                "results": [{"name": "1.0.0", "digest": "a"}],
                "next": ".../tags?page=2&page_size=100",
            },
        ),
        _response(
            ok=True,
            payload={"results": [{"name": "0.9.0", "digest": "b"}], "next": None},
        ),
    ]

    result = get_docker_hub_tags_and_digests("airbyte/source-declarative-manifest")

    assert result == {"1.0.0": "a", "0.9.0": "b"}
    assert mock_get.call_args_list[0].args[0].endswith("tags?page_size=100")
    assert mock_get.call_args_list[1].args[0] == ".../tags?page=2&page_size=100"
