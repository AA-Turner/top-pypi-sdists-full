# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the EU runner guard at the connection retriever's call sites."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock, Mock

import pytest
import sqlalchemy

from airbyte_ops_mcp.connection_config_retriever import audit_logging, retrieval
from airbyte_ops_mcp.connection_config_retriever.retrieval import (
    SELECT_ON_CONNECTION,
    SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU,
    SELECT_ON_CONNECTION_NOT_EU,
    RetrievalMetadata,
    get_connection,
    retrieve_objects,
)
from airbyte_ops_mcp.constants import ConnectionObject

pytestmark = pytest.mark.unit

CONNECTION_ID = "00000000-0000-0000-0000-000000000123"
CONNECTION_ROW = ("source-id", "destination-id", "catalog-id", {"streams": []})


def _db_conn(is_eu: bool) -> MagicMock:
    """A DB connection that answers the residency and connection queries."""

    def execute(query: sqlalchemy.TextClause, parameters: dict) -> Mock:
        row = (
            (is_eu,)
            if query is SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU
            else CONNECTION_ROW
        )
        return Mock(first=Mock(return_value=row))

    db_conn = MagicMock()
    db_conn.execute.side_effect = execute
    return db_conn


def _queries(db_conn: MagicMock) -> list[sqlalchemy.TextClause]:
    return [call.args[0] for call in db_conn.execute.call_args_list]


@pytest.fixture
def eu_runner_check(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Stub the GCE metadata check; tests set its return value."""
    check = Mock(return_value=False)
    monkeypatch.setattr(retrieval, "is_running_on_eu_runner", check)
    return check


@pytest.fixture(autouse=True)
def _no_audit_logging(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit_logging, "get_user_email", lambda: "tester@example.com")
    monkeypatch.setattr(audit_logging, "_get_logger", Mock())


def _patch_prod_db(monkeypatch: pytest.MonkeyPatch, db_conn: MagicMock) -> None:
    pool = MagicMock()
    pool.connect.return_value.__enter__.return_value = db_conn
    monkeypatch.setattr(retrieval, "get_secret_manager_client", Mock())
    monkeypatch.setattr(retrieval, "get_pool", Mock(return_value=pool))


def test_eu_connection_is_dropped_off_the_eu_runner(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    eu_runner_check: Mock,
) -> None:
    """Off the EU runner, an EU connection is removed before any object is read."""
    db_conn = _db_conn(is_eu=True)
    _patch_prod_db(monkeypatch, db_conn)
    eu_runner_check.return_value = False

    with caplog.at_level(logging.WARNING, logger=retrieval.LOGGER.name):
        candidates = retrieve_objects(
            [ConnectionObject.SOURCE_ID, ConnectionObject.CONFIGURED_CATALOG],
            "test",
            CONNECTION_ID,
        )

    assert candidates == []
    eu_runner_check.assert_called_once_with()
    assert _queries(db_conn) == [SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU]
    assert "only permitted on the EU regression runner" in caplog.text
    assert CONNECTION_ID in caplog.text


def test_us_connection_is_dropped_on_the_eu_runner(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    eu_runner_check: Mock,
) -> None:
    """On the EU runner, a US connection is removed before any object is read."""
    db_conn = _db_conn(is_eu=False)
    _patch_prod_db(monkeypatch, db_conn)
    eu_runner_check.return_value = True

    with caplog.at_level(logging.WARNING, logger=retrieval.LOGGER.name):
        candidates = retrieve_objects(
            [ConnectionObject.SOURCE_ID, ConnectionObject.SOURCE_CONFIG],
            "test",
            CONNECTION_ID,
        )

    assert candidates == []
    eu_runner_check.assert_called_once_with()
    assert _queries(db_conn) == [SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU]
    assert "only retrieves EU connections" in caplog.text
    assert CONNECTION_ID in caplog.text


def test_us_connection_off_the_eu_runner_uses_the_eu_filtered_query(
    monkeypatch: pytest.MonkeyPatch,
    eu_runner_check: Mock,
) -> None:
    """Off the EU runner, a US connection is read with the EU-filtered query."""
    db_conn = _db_conn(is_eu=False)
    _patch_prod_db(monkeypatch, db_conn)

    candidates = retrieve_objects([ConnectionObject.SOURCE_ID], "test", CONNECTION_ID)

    assert [candidate.source_id for candidate in candidates] == ["source-id"]
    eu_runner_check.assert_called_once_with()
    assert _queries(db_conn) == [
        SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU,
        SELECT_ON_CONNECTION_NOT_EU,
    ]


def test_eu_connection_on_the_eu_runner_uses_the_unfiltered_query(
    monkeypatch: pytest.MonkeyPatch,
    eu_runner_check: Mock,
) -> None:
    """On the EU runner, an EU connection is kept and read without the EU filter."""
    db_conn = _db_conn(is_eu=True)
    _patch_prod_db(monkeypatch, db_conn)
    eu_runner_check.return_value = True

    candidates = retrieve_objects([ConnectionObject.SOURCE_ID], "test", CONNECTION_ID)

    assert [candidate.source_id for candidate in candidates] == ["source-id"]
    assert _queries(db_conn) == [
        SELECT_ON_CONNECTION_DATAPLANE_GROUP_IS_EU,
        SELECT_ON_CONNECTION,
    ]


@pytest.mark.parametrize(
    ("is_eu_connection", "on_eu_runner", "expected_query"),
    [
        pytest.param(True, True, SELECT_ON_CONNECTION, id="eu-on-eu-runner"),
        pytest.param(True, False, SELECT_ON_CONNECTION_NOT_EU, id="eu-off-eu-runner"),
        pytest.param(False, True, SELECT_ON_CONNECTION_NOT_EU, id="us-on-eu-runner"),
        pytest.param(False, False, SELECT_ON_CONNECTION_NOT_EU, id="us-off-eu-runner"),
    ],
)
def test_get_connection_uses_the_unfiltered_query_only_for_eu_on_the_eu_runner(
    eu_runner_check: Mock,
    is_eu_connection: bool,
    on_eu_runner: bool,
    expected_query: sqlalchemy.TextClause,
) -> None:
    """Only an EU connection on the EU runner drops the `!= 'EU'` filter."""
    db_conn = _db_conn(is_eu=is_eu_connection)
    eu_runner_check.return_value = on_eu_runner

    get_connection(
        RetrievalMetadata(CONNECTION_ID, ConnectionObject.SOURCE_ID, "test"),
        CONNECTION_ID,
        db_conn,
        is_eu_connection=is_eu_connection,
    )

    assert _queries(db_conn) == [expected_query]
    if not is_eu_connection:
        eu_runner_check.assert_not_called()
