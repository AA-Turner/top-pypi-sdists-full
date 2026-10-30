# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""The regression-test CLI checks residency before fetching a connection."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

import pytest

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.connection_config_retriever import ConnectionNotFoundError
from airbyte_ops_mcp.regression_tests.models import ComparableOutputs

pytestmark = pytest.mark.unit

CONNECTION_ID = "00000000-0000-0000-0000-000000000123"


class _FetchReachedError(Exception):
    """Stops the run at the public API fetch, once the guard has let it through."""


@pytest.fixture
def cli(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Stub the residency lookup, the metadata check, the fetch and CI outputs."""
    stubs = Mock()
    stubs.github_outputs = {}
    stubs.get_connection_residency = Mock(return_value="us")
    stubs.is_running_on_eu_runner = Mock(return_value=False)
    stubs.fetch_connection_data = Mock(side_effect=_FetchReachedError)

    monkeypatch.setenv("USE_CONNECTION_SECRET_RETRIEVER", "true")
    monkeypatch.setattr(
        cloud, "get_connection_residency", stubs.get_connection_residency
    )
    monkeypatch.setattr(cloud, "is_running_on_eu_runner", stubs.is_running_on_eu_runner)
    monkeypatch.setattr(cloud, "fetch_connection_data", stubs.fetch_connection_data)
    monkeypatch.setattr(
        cloud,
        "write_github_output",
        lambda key, value: stubs.github_outputs.__setitem__(key, value),
    )
    return stubs


def _run(
    tmp_path: Path,
    connection_id: str | None = CONNECTION_ID,
    output_mode: str | None = None,
) -> None:
    cloud.regression_test(
        skip_compare=True,
        test_image="airbyte/source-test:2.0.0",
        command="spec",
        connection_id=connection_id,
        output_dir=str(tmp_path),
        output_mode=output_mode,
    )


def test_eu_connection_is_refused_before_the_fetch_off_the_eu_runner(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    cli: Mock,
) -> None:
    """Off the EU runner, an EU connection's config and catalog are never fetched."""
    cli.get_connection_residency.return_value = "eu"

    with pytest.raises(SystemExit) as exc_info:
        _run(tmp_path)

    assert exc_info.value.code == 1
    cli.get_connection_residency.assert_called_once_with(CONNECTION_ID)
    cli.is_running_on_eu_runner.assert_called_once_with()
    cli.fetch_connection_data.assert_not_called()
    assert cli.github_outputs["success"] is False
    assert cli.github_outputs["error"] == (
        f"{cloud.EU_RUNNER_REQUIRED_MESSAGE}; connection ID {CONNECTION_ID} was "
        "refused before its config or catalog was fetched."
    )
    assert "only permitted on the EU regression runner" in " ".join(
        capsys.readouterr().err.split()
    )


def test_eu_connection_on_the_eu_runner_is_fetched(tmp_path: Path, cli: Mock) -> None:
    """On the EU runner, the guard lets an EU connection through to the fetch."""
    cli.get_connection_residency.return_value = "eu"
    cli.is_running_on_eu_runner.return_value = True

    with pytest.raises(_FetchReachedError):
        _run(tmp_path)

    cli.fetch_connection_data.assert_called_once_with(CONNECTION_ID)


def test_us_connection_off_the_eu_runner_is_fetched(tmp_path: Path, cli: Mock) -> None:
    """Off the EU runner, the guard lets a US connection through to the fetch."""
    with pytest.raises(_FetchReachedError):
        _run(tmp_path)

    cli.get_connection_residency.assert_called_once_with(CONNECTION_ID)
    cli.is_running_on_eu_runner.assert_called_once_with()
    cli.fetch_connection_data.assert_called_once_with(CONNECTION_ID)


def test_us_connection_is_refused_before_the_fetch_on_the_eu_runner(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    cli: Mock,
) -> None:
    """On the EU runner, a US connection's config and catalog are never fetched."""
    cli.is_running_on_eu_runner.return_value = True

    with pytest.raises(SystemExit) as exc_info:
        _run(tmp_path)

    assert exc_info.value.code == 1
    cli.fetch_connection_data.assert_not_called()
    assert cli.github_outputs["success"] is False
    assert cli.github_outputs["error"] == (
        f"{cloud.EU_RUNNER_EU_ONLY_MESSAGE}; connection ID {CONNECTION_ID} was "
        "refused before its config or catalog was fetched."
    )
    assert "only retrieves EU connections" in " ".join(capsys.readouterr().err.split())


def test_failed_residency_lookup_stops_before_the_fetch(
    tmp_path: Path, cli: Mock
) -> None:
    """With the retriever on, a lookup that cannot answer fails closed."""
    cli.get_connection_residency.side_effect = ConnectionNotFoundError(
        f"Connection {CONNECTION_ID} was not found."
    )

    with pytest.raises(SystemExit) as exc_info:
        _run(tmp_path)

    assert exc_info.value.code == 1
    cli.fetch_connection_data.assert_not_called()
    assert cli.github_outputs == {
        "success": False,
        "error": f"Connection {CONNECTION_ID} was not found.",
    }


def test_residency_is_checked_when_the_retriever_is_off(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, cli: Mock
) -> None:
    """Without the secret retriever, the CLI behaves as before."""
    monkeypatch.delenv("USE_CONNECTION_SECRET_RETRIEVER")

    with pytest.raises(_FetchReachedError):
        _run(tmp_path)

    cli.get_connection_residency.assert_called_once_with(CONNECTION_ID)
    cli.fetch_connection_data.assert_called_once_with(CONNECTION_ID)


def test_eu_raw_mode_is_refused_before_fetch_or_metadata_check(
    tmp_path: Path, cli: Mock
) -> None:
    cli.get_connection_residency.return_value = "eu"

    with pytest.raises(SystemExit) as exc_info:
        _run(tmp_path, output_mode="raw")

    assert exc_info.value.code == 1
    cli.get_connection_residency.assert_called_once_with(CONNECTION_ID)
    cli.is_running_on_eu_runner.assert_not_called()
    cli.fetch_connection_data.assert_not_called()
    assert cli.github_outputs == {
        "success": False,
        "error": (
            "EU-resident connections always run masked; output_mode=raw is refused."
        ),
    }


def test_gsm_path_does_not_check_residency(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, cli: Mock
) -> None:
    """With no connection ID there is nothing to route, so no lookup is made."""
    monkeypatch.setattr(cloud, "ensure_image_available", lambda _image: True)
    monkeypatch.setattr(cloud, "track_regression_test", lambda **_kwargs: None)
    monkeypatch.setattr(cloud, "write_github_summary", lambda _summary: None)
    monkeypatch.setattr(cloud, "write_github_outputs", lambda _outputs: None)

    def _fake_run(*, command, output_dir, **_kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        return (
            {
                "command": command.value,
                "success": True,
                "exit_code": 0,
                "message_counts": {},
                "record_counts_per_stream": {},
            },
            ComparableOutputs(),
        )

    monkeypatch.setattr(cloud, "_run_connector_command", _fake_run)

    _run(tmp_path, connection_id=None)

    cli.get_connection_residency.assert_not_called()
    cli.is_running_on_eu_runner.assert_not_called()
    cli.fetch_connection_data.assert_not_called()
