# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the fetch_connection_config functionality."""

from __future__ import annotations

import contextlib
import json
import os
import stat
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.cloud_admin.connection_config import (
    fetch_connection_config,
)
from airbyte_ops_mcp.regression_tests.connection_fetcher import ConnectionData

FAKE_CONNECTION_ID = "00000000-0000-0000-0000-000000000001"
FAKE_CONFIG: dict[str, Any] = {"host": "example.com", "port": 5432}

_FETCH_DATA = "airbyte_ops_mcp.cloud_admin.connection_config.fetch_connection_data"
_RETRIEVE_SECRETS = (
    "airbyte_ops_mcp.cloud_admin.connection_config.retrieve_unmasked_config"
)


@pytest.fixture()
def connection_data() -> ConnectionData:
    """Return a minimal `ConnectionData` stub."""
    return ConnectionData(
        connection_id=FAKE_CONNECTION_ID,
        source_id="src-001",
        source_name="Test Source",
        source_definition_id="def-001",
        config=FAKE_CONFIG,
        catalog={"streams": []},
        stream_names=[],
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "output_path_fn,expected_suffix",
    [
        pytest.param(
            lambda tmp: None,
            f"connection-{FAKE_CONNECTION_ID}-config.json",
            id="default_uses_tempdir",
        ),
        pytest.param(
            lambda tmp: tmp / "my-config.json",
            "my-config.json",
            id="explicit_file_path",
        ),
        pytest.param(
            lambda tmp: tmp,
            f"connection-{FAKE_CONNECTION_ID}-config.json",
            id="explicit_directory_path",
        ),
    ],
)
def test_output_path_resolution(
    tmp_path: Path,
    connection_data: ConnectionData,
    output_path_fn: Any,
    expected_suffix: str,
) -> None:
    """Config file lands at the expected location for each `output_path` variant."""
    output_path = output_path_fn(tmp_path)
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch(_FETCH_DATA, return_value=connection_data))
        mock_tmp = stack.enter_context(
            patch("airbyte_ops_mcp.cloud_admin.connection_config.tempfile")
        )
        mock_tmp.gettempdir.return_value = str(tmp_path)
        result = fetch_connection_config(
            connection_id=FAKE_CONNECTION_ID,
            output_path=output_path,
        )

    assert result.success is True
    result_path = Path(result.output_path)
    assert result_path.is_absolute()
    assert result_path.name == expected_suffix.split("/")[-1]
    assert result_path.exists()
    assert json.loads(result_path.read_text()) == FAKE_CONFIG


@pytest.mark.unit
def test_secrets_file_mode_is_600(
    tmp_path: Path,
    connection_data: ConnectionData,
) -> None:
    """When `with_secrets=True` the output file has owner-only permissions."""
    target = tmp_path / "secret-config.json"
    secret_config = {"api_key": "super-secret"}
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch(_FETCH_DATA, return_value=connection_data))
        stack.enter_context(patch(_RETRIEVE_SECRETS, return_value=secret_config))
        result = fetch_connection_config(
            connection_id=FAKE_CONNECTION_ID,
            output_path=target,
            with_secrets=True,
            oc_issue_url="https://github.com/airbytehq/oncall/issues/999",
        )

    assert result.success is True
    assert result.with_secrets is True
    file_mode = stat.S_IMODE(os.stat(target).st_mode)
    assert file_mode == 0o600, f"Expected 0o600 but got {oct(file_mode)}"


@pytest.mark.unit
def test_no_secrets_does_not_restrict_permissions(
    tmp_path: Path,
    connection_data: ConnectionData,
) -> None:
    """Without `--with-secrets` the file permissions are not explicitly restricted."""
    target = tmp_path / "plain-config.json"
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch(_FETCH_DATA, return_value=connection_data))
        mock_os_open = stack.enter_context(
            patch("airbyte_ops_mcp.cloud_admin.connection_config.os.open")
        )
        fetch_connection_config(
            connection_id=FAKE_CONNECTION_ID,
            output_path=target,
        )

    mock_os_open.assert_not_called()


@pytest.mark.unit
def test_secrets_without_oc_issue_url_fails() -> None:
    """Passing `with_secrets=True` without `oc_issue_url` returns failure."""
    result = fetch_connection_config(
        connection_id=FAKE_CONNECTION_ID,
        with_secrets=True,
    )
    assert result.success is False
    assert "oc-issue-url" in result.message.lower()


@pytest.mark.unit
def test_output_path_is_absolute_in_result(
    tmp_path: Path,
    connection_data: ConnectionData,
) -> None:
    """The `output_path` field in the result contains an absolute path."""
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch(_FETCH_DATA, return_value=connection_data))
        mock_tmp = stack.enter_context(
            patch("airbyte_ops_mcp.cloud_admin.connection_config.tempfile")
        )
        mock_tmp.gettempdir.return_value = str(tmp_path)
        result = fetch_connection_config(connection_id=FAKE_CONNECTION_ID)

    assert Path(result.output_path).is_absolute()
    assert str(tmp_path) in result.message
