# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for `airbyte-ops cloud connection get-region`."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, Mock

import cyclopts
import google.auth.exceptions
import pytest
import sqlalchemy.exc

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.cli.app import app
from airbyte_ops_mcp.connection_config_retriever import retrieval

CONNECTION_ID = "00000000-0000-0000-0000-000000000123"


def invoke_cli(tokens: list[str]) -> int:
    """Run the `airbyte-ops` app and return its exit code."""
    try:
        app(tokens=tokens, exit_on_error=False)
    except cyclopts.exceptions.CycloptsError:
        return 1
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


@pytest.mark.unit
@pytest.mark.parametrize(
    ("dataplane_group", "expected_residency"),
    [("EU", "eu"), ("US", "us"), ("US-Central", "us")],
)
def test_get_region_prints_json_and_writes_github_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    dataplane_group: str,
    expected_residency: str,
) -> None:
    """The command prints both values and exports them for GitHub Actions."""
    connection_id = "connection-123"
    github_output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output))
    monkeypatch.setattr(
        cloud,
        "get_connection_dataplane_group",
        lambda _connection_id: dataplane_group,
    )

    exit_code = invoke_cli(
        [
            "cloud",
            "connection",
            "get-region",
            "--connection-id",
            connection_id,
        ]
    )

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out) == {
        "connection_id": connection_id,
        "dataplane_group": dataplane_group,
        "residency": expected_residency,
    }
    assert github_output.read_text() == (
        f"dataplane_group={dataplane_group}\nresidency={expected_residency}\n"
    )


def _mock_prod_db(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: tuple | None = None,
    connect_error: Exception | None = None,
) -> None:
    """Stub the replica so the lookup returns `row` or fails to connect."""
    pool = MagicMock()
    if connect_error is not None:
        pool.connect.side_effect = connect_error
    else:
        db_conn = pool.connect.return_value.__enter__.return_value
        db_conn.execute.return_value.first.return_value = row
    monkeypatch.setattr(retrieval, "get_secret_manager_client", Mock())
    monkeypatch.setattr(retrieval, "get_pool", Mock(return_value=pool))


def _fail_if_credentials_are_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        retrieval,
        "get_secret_manager_client",
        Mock(side_effect=AssertionError("credentials were loaded")),
    )


def _missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        retrieval,
        "get_secret_manager_client",
        Mock(
            side_effect=google.auth.exceptions.DefaultCredentialsError(
                "Your default credentials were not found."
            )
        ),
    )


def _replica_outage(monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_prod_db(
        monkeypatch,
        connect_error=sqlalchemy.exc.OperationalError(
            "SELECT 1", {}, OSError("connection refused")
        ),
    )


def _unknown_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_prod_db(monkeypatch, row=None)


def _null_dataplane_group(monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_prod_db(monkeypatch, row=(None,))


@pytest.mark.unit
@pytest.mark.parametrize(
    ("connection_id", "arrange", "expected_message"),
    [
        pytest.param(
            CONNECTION_ID,
            _unknown_connection,
            f"Connection {CONNECTION_ID} was not found.",
            id="not-found",
        ),
        pytest.param(
            "not-a-uuid",
            _fail_if_credentials_are_loaded,
            "Connection ID 'not-a-uuid' is not a valid UUID.",
            id="non-uuid",
        ),
        pytest.param(
            CONNECTION_ID,
            _missing_credentials,
            "No usable GCP credentials for the Prod DB replica "
            "(DefaultCredentialsError). Set GCP_PROD_DB_ACCESS_CREDENTIALS or "
            "configure Application Default Credentials.",
            id="missing-credentials",
        ),
        pytest.param(
            CONNECTION_ID,
            _replica_outage,
            "Could not reach the Prod DB replica to read the dataplane group of "
            f"connection {CONNECTION_ID} (OperationalError).",
            id="replica-outage",
        ),
        pytest.param(
            CONNECTION_ID,
            _null_dataplane_group,
            f"Connection {CONNECTION_ID} has no dataplane group name, "
            "so its residency cannot be decided.",
            id="null-dataplane-group",
        ),
    ],
)
def test_get_region_lookup_failure_exits_with_one_line_and_no_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    connection_id: str,
    arrange: Callable[[pytest.MonkeyPatch], None],
    expected_message: str,
) -> None:
    """A failed lookup exits non-zero with a clear message and routes nothing.

    No `GITHUB_OUTPUT` line is written, so the workflow's resolver step sees no
    residency and fails closed.
    """
    github_output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output))
    arrange(monkeypatch)

    exit_code = invoke_cli(
        ["cloud", "connection", "get-region", "--connection-id", connection_id]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert " ".join(captured.err.split()) == f"Error: {expected_message}"
    assert "Traceback" not in captured.err + captured.out
    assert not github_output.exists()
