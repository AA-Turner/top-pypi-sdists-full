from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from airbyte import cloud
from airbyte.cloud.connections import CloudConnectionInfo
from airbyte.cloud.models import CloudJobInfo
from airbyte_cloud_cli import connections, jobs, workspaces


def _workspace() -> cloud.CloudWorkspace:
    return cloud.CloudWorkspace(
        workspace_id="workspace-id",
        client_id="client-id",
        client_secret="client-secret",
        api_root="https://api.example.com/v1",
    )


def _job_response(job_id: int, *, connection_id: str = "connection-id"):
    return SimpleNamespace(
        job_id=job_id,
        connection_id=connection_id,
        status="succeeded",
        bytes_synced=123,
        rows_synced=456,
        start_time="2026-01-01T00:00:00Z",
    )


def test_connection_info_uses_cloud_connection_api() -> None:
    workspace = _workspace()
    connection = cloud.CloudConnection(
        workspace=workspace,
        connection_id="connection-id",
    )
    response = SimpleNamespace(
        connection_id="connection-id",
        workspace_id="workspace-id",
        source_id="source-id",
        destination_id="destination-id",
        name="Connection",
        configurations={},
        prefix=None,
        status="active",
    )

    with patch.object(
        connections.cloud_connections.api_util,
        "get_connection",
        return_value=response,
    ) as get_connection:
        result = connections._connection_info(connection)

    assert isinstance(result, CloudConnectionInfo)
    assert result.connection_id == "connection-id"
    assert get_connection.call_args.kwargs == {
        "workspace_id": "workspace-id",
        "connection_id": "connection-id",
        "api_root": workspace.api_root,
        "client_id": workspace.client_id,
        "client_secret": workspace.client_secret,
        "bearer_token": workspace.bearer_token,
    }


def test_workspace_info_uses_workspace_api_util() -> None:
    workspace = _workspace()
    response = SimpleNamespace(workspace_id="workspace-id", name="Workspace")

    with patch.object(
        workspaces.api_util,
        "get_workspace",
        return_value=response,
    ) as get_workspace:
        result = workspaces._workspace_info(workspace)

    assert result is response
    assert get_workspace.call_args.args == ("workspace-id",)
    assert get_workspace.call_args.kwargs == {
        "api_root": workspace.api_root,
        "client_id": workspace.client_id,
        "client_secret": workspace.client_secret,
        "bearer_token": workspace.bearer_token,
    }


def test_job_info_uses_api_util() -> None:
    workspace = _workspace()
    response = _job_response(123)

    with patch.object(
        jobs.api_util,
        "get_job_info",
        return_value=response,
    ) as get_job_info:
        result = jobs._get_job_info(workspace, 123)

    assert result is response
    assert get_job_info.call_args.kwargs == {
        "job_id": 123,
        "api_root": workspace.api_root,
        "client_id": workspace.client_id,
        "client_secret": workspace.client_secret,
        "bearer_token": workspace.bearer_token,
    }


def test_jobs_list_fetches_info_from_real_sync_results() -> None:
    response = _job_response(123)

    with patch.object(
        jobs.api_util, "get_job_logs", return_value=[response]
    ), patch.object(jobs, "json_output") as output:
        jobs.list_(
            connection_id="connection-id",
            workspace_id="workspace-id",
            client_id="client-id",
            client_secret="client-secret",
        )

    result = output.call_args.args[0]
    assert isinstance(result[0], CloudJobInfo)
    assert result[0].job_id == 123


def test_connections_sync_wait_fetches_latest_job_info() -> None:
    with patch.object(
        connections.cloud_connections.api_util,
        "run_connection",
        return_value=SimpleNamespace(job_id=123),
    ), patch.object(
        connections.cloud_connections.api_util,
        "get_job_info",
        return_value=_job_response(123),
    ), patch.object(connections, "json_output") as output:
        connections.sync(
            "connection-id",
            wait=True,
            workspace_id="workspace-id",
            client_id="client-id",
            client_secret="client-secret",
        )

    result = output.call_args.args[0]
    assert isinstance(result, CloudJobInfo)
    assert result.job_id == 123


def test_jobs_wait_fetches_latest_job_info() -> None:
    with patch.object(
        jobs.api_util,
        "get_job_info",
        return_value=_job_response(123),
    ), patch.object(jobs, "json_output") as output:
        jobs.wait(
            "123",
            workspace_id="workspace-id",
            client_id="client-id",
            client_secret="client-secret",
        )

    result = output.call_args.args[0]
    assert isinstance(result, CloudJobInfo)
    assert result.job_id == 123
