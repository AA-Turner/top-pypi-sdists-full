# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for GCE residency detection."""

from __future__ import annotations

from unittest.mock import MagicMock, Mock

import pytest
import requests

from airbyte_ops_mcp.connection_config_retriever import residency, retrieval
from airbyte_ops_mcp.connection_config_retriever.retrieval import (
    SELECT_ON_CONNECTION_DATAPLANE_GROUP_NAME,
    ConnectionNotFoundError,
    get_connection_residency,
    residency_for_dataplane_group,
)

CONNECTION_ID = "00000000-0000-0000-0000-000000000123"


def _mock_metadata_session(
    monkeypatch: pytest.MonkeyPatch,
    responses: list[Mock] | None = None,
    side_effect: Exception | None = None,
) -> MagicMock:
    """Replace the metadata HTTP session with a context-managed mock."""
    session = MagicMock()
    session.__enter__.return_value = session
    if responses is not None:
        session.get.side_effect = responses
    if side_effect is not None:
        session.get.side_effect = side_effect
    monkeypatch.setattr(residency.requests, "Session", Mock(return_value=session))
    return session


def _metadata_response(status_code: int, text: str) -> Mock:
    return Mock(
        status_code=status_code,
        text=text,
        headers={"Metadata-Flavor": "Google"},
    )


@pytest.mark.unit
def test_metadata_request_error_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    """A missing metadata server cannot authorize EU retrieval."""
    session = _mock_metadata_session(monkeypatch, side_effect=requests.ConnectionError)

    assert residency.is_running_on_eu_runner() is False
    session.get.assert_called_once()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("zone", "service_account", "expected"),
    [
        (
            "projects/1/zones/europe-west9-b",
            residency.EU_RUNNER_SERVICE_ACCOUNT,
            True,
        ),
        ("projects/1/zones/us-west3-a", residency.EU_RUNNER_SERVICE_ACCOUNT, False),
        (
            "projects/1/zones/europe-west9-a",
            "another-service-account@example.com",
            False,
        ),
        ("projects/1/zones/europe-west1-b", residency.EU_RUNNER_SERVICE_ACCOUNT, False),
    ],
)
def test_metadata_identity_and_zone(
    monkeypatch: pytest.MonkeyPatch,
    zone: str,
    service_account: str,
    expected: bool,
) -> None:
    """Only the configured zone and job service account authorize EU retrieval."""
    responses = [
        _metadata_response(200, zone),
        _metadata_response(200, service_account),
    ]
    session = _mock_metadata_session(monkeypatch, responses=responses)

    assert residency.is_running_on_eu_runner() is expected
    assert session.get.call_count == 2
    assert all(
        call.kwargs["headers"] == {"Metadata-Flavor": "Google"}
        and call.kwargs["timeout"] == 2
        and call.kwargs["allow_redirects"] is False
        for call in session.get.call_args_list
    )


@pytest.mark.unit
def test_non_200_metadata_response_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unavailable metadata field cannot authorize EU retrieval."""
    session = _mock_metadata_session(
        monkeypatch, responses=[_metadata_response(503, "")]
    )

    assert residency.is_running_on_eu_runner() is False
    session.get.assert_called_once()


@pytest.mark.unit
def test_metadata_response_without_flavor_header_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A response without the metadata server header cannot authorize EU access."""
    session = _mock_metadata_session(
        monkeypatch,
        responses=[
            Mock(
                status_code=200,
                text="projects/1/zones/europe-west9-b",
                headers={},
            )
        ],
    )

    assert residency.is_running_on_eu_runner() is False
    session.get.assert_called_once()


@pytest.mark.unit
def test_metadata_redirect_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    """A metadata redirect cannot authorize EU access."""
    session = _mock_metadata_session(
        monkeypatch,
        responses=[_metadata_response(302, "projects/1/zones/europe-west9-b")],
    )

    assert residency.is_running_on_eu_runner() is False
    session.get.assert_called_once()


@pytest.mark.unit
def test_metadata_session_ignores_proxy_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The GCE metadata check bypasses proxy settings and follows no redirects."""
    monkeypatch.setenv("HTTP_PROXY", "http://proxy.example:8080")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example:8080")
    monkeypatch.setenv("ALL_PROXY", "http://proxy.example:8080")
    session = _mock_metadata_session(
        monkeypatch,
        responses=[
            _metadata_response(200, "projects/1/zones/europe-west9-b"),
            _metadata_response(200, residency.EU_RUNNER_SERVICE_ACCOUNT),
        ],
    )

    assert residency.is_running_on_eu_runner() is True
    assert session.trust_env is False
    assert session.get.call_count == 2
    assert all(
        call.kwargs["allow_redirects"] is False for call in session.get.call_args_list
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("dataplane_group", "expected_residency"),
    [("EU", "eu"), ("US", "us"), ("US-Central", "us")],
)
def test_residency_for_dataplane_group(
    dataplane_group: str,
    expected_residency: str,
) -> None:
    """Only the EU dataplane group maps to EU residency."""
    assert residency_for_dataplane_group(dataplane_group) == expected_residency


def _mock_prod_db(monkeypatch: pytest.MonkeyPatch, row: tuple | None) -> MagicMock:
    """Replace the Prod DB pool with one whose single query returns `row`."""
    db_conn = MagicMock()
    db_conn.execute.return_value.first.return_value = row
    pool = MagicMock()
    pool.connect.return_value.__enter__.return_value = db_conn
    monkeypatch.setattr(retrieval, "get_secret_manager_client", Mock())
    monkeypatch.setattr(retrieval, "get_pool", Mock(return_value=pool))
    return db_conn


@pytest.mark.unit
@pytest.mark.parametrize(
    ("dataplane_group", "expected_residency"),
    [("EU", "eu"), ("US", "us"), ("US-Central", "us")],
)
def test_get_connection_residency(
    monkeypatch: pytest.MonkeyPatch,
    dataplane_group: str,
    expected_residency: str,
) -> None:
    """The helper reads the dataplane group once and maps it to a residency."""
    db_conn = _mock_prod_db(monkeypatch, (dataplane_group,))

    assert get_connection_residency(CONNECTION_ID) == expected_residency
    db_conn.execute.assert_called_once_with(
        SELECT_ON_CONNECTION_DATAPLANE_GROUP_NAME,
        parameters={"connection_id": CONNECTION_ID},
    )


@pytest.mark.unit
@pytest.mark.parametrize("dataplane_group", [None, "", "  "])
def test_get_connection_residency_rejects_a_missing_dataplane_group(
    monkeypatch: pytest.MonkeyPatch,
    dataplane_group: str | None,
) -> None:
    """A NULL or empty group name raises instead of defaulting to US."""
    _mock_prod_db(monkeypatch, (dataplane_group,))

    with pytest.raises(ValueError, match="has no dataplane group name"):
        get_connection_residency(CONNECTION_ID)


@pytest.mark.unit
def test_get_connection_residency_raises_when_connection_is_unknown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unknown connection raises rather than resolving to a residency."""
    _mock_prod_db(monkeypatch, None)

    with pytest.raises(ConnectionNotFoundError, match=CONNECTION_ID):
        get_connection_residency(CONNECTION_ID)


@pytest.mark.unit
def test_dataplane_group_lookup_does_not_filter_tombstoned_rows() -> None:
    """A deleted EU connection must still read as EU, so the lookup fails closed."""
    assert "tombstone" not in SELECT_ON_CONNECTION_DATAPLANE_GROUP_NAME.text.lower()


@pytest.mark.unit
def test_get_connection_residency_rejects_a_non_uuid_before_any_lookup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A malformed ID fails before credentials are loaded or the DB is queried."""
    db_conn = _mock_prod_db(monkeypatch, ("EU",))

    with pytest.raises(ValueError, match="is not a valid UUID"):
        get_connection_residency("not-a-uuid")
    retrieval.get_secret_manager_client.assert_not_called()
    db_conn.execute.assert_not_called()
